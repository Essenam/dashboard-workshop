"""Run every data quality rule over every row, and build the operating summaries.

Reads the raw trip files in data/raw/ and writes small files to data/summaries/.
The dashboard reads only those summaries, never the raw rows.

Run with: uv run python pipeline/build_summaries.py
"""
import json
import time

from common import SUMMARIES, connect
from rules import DIMENSIONS, RULES

EXAMPLES_PER_RULE = 3
# Columns shown in example rows. The data holds no rider or driver identifiers; base numbers
# (company dispatch offices) are left out too, since they add nothing to an example.
EXAMPLE_COLUMNS = """company, request_datetime, on_scene_datetime, pickup_datetime, dropoff_datetime,
    PULocationID, DOLocationID, trip_miles, trip_time, base_passenger_fare, tips, tolls, driver_pay"""
DUP_KEY = """hvfhs_license_num, dispatching_base_num, request_datetime, on_scene_datetime,
    pickup_datetime, dropoff_datetime, PULocationID, DOLocationID, trip_miles, trip_time,
    base_passenger_fare, driver_pay, tips"""

con = connect()
con.sql("""
    create view t as
    select *,
        case hvfhs_license_num when 'HV0003' then 'Uber' when 'HV0005' then 'Lyft'
            else hvfhs_license_num end as company,
        date_diff('second', request_datetime, pickup_datetime) / 60.0 as wait_min,
        -- A wait is usable only when the times run in order (rules CON-02, CON-03) and it is
        -- under two hours.
        (request_datetime <= pickup_datetime
            and (on_scene_datetime is null or on_scene_datetime >= request_datetime)
            and date_diff('minute', request_datetime, pickup_datetime) <= 120) as wait_ok
    from trips
""")
SUMMARIES.mkdir(parents=True, exist_ok=True)


def step(label, fn):
    start = time.time()
    fn()
    print(f"{label}: {time.time() - start:.0f}s", flush=True)


def write_csv(sql, name):
    con.sql(sql).write_csv((SUMMARIES / name).as_posix())


# 1. Data quality: failing rows per rule per month, in one pass over every row.
def dq_monthly():
    row_rules = [r for r in RULES if r["id"] != "UNQ-01"]
    counts = ",\n".join(f'count(*) filter (where {r["fails"]}) as "{r["id"]}"' for r in row_rules)
    wide = con.sql(f"select file_month as month, count(*) as rows, {counts} from t group by 1").df()
    # Uniqueness: every copy of a trip beyond the first counts as a failing row.
    dups = con.sql(f"""
        select file_month as month, sum(n - 1) as failing
        from (select file_month, hash({DUP_KEY}) as h, count(*) as n from trips group by 1, 2 having n > 1)
        group by 1
    """).df().set_index("month")["failing"]
    wide["UNQ-01"] = wide["month"].map(dups).fillna(0).astype(int)
    long = wide.melt(id_vars=["month", "rows"], var_name="rule", value_name="failing")
    long.sort_values(["rule", "month"]).to_csv(SUMMARIES / "dq_monthly.csv", index=False)
    global DQ
    DQ = long


def dq_rules():
    total_rows = int(DQ.groupby("month")["rows"].first().sum())
    out = []
    for r in RULES:
        failing = int(DQ.loc[DQ.rule == r["id"], "failing"].sum())
        if r["id"] == "UNQ-01":
            ex_sql = f"""
                select {EXAMPLE_COLUMNS} from t
                where hash({DUP_KEY}) in (
                    select hash({DUP_KEY}) from trips group by 1 having count(*) > 1 limit {EXAMPLES_PER_RULE})
                limit {EXAMPLES_PER_RULE}"""
        else:
            ex_sql = f"select {EXAMPLE_COLUMNS} from t where {r['fails']} limit {EXAMPLES_PER_RULE}"
        examples = [{k: (None if v is None else str(v)) for k, v in row.items()}
                    for row in con.sql(ex_sql).df().astype(object).where(lambda d: d.notna(), None).to_dict("records")] if failing else []
        out.append({**r, "failing": failing, "rows": total_rows, "rate": failing / total_rows,
                    "examples": examples})
    (SUMMARIES / "dq_rules.json").write_text(json.dumps(
        {"dimensions": DIMENSIONS, "rows_checked": total_rows, "rules": out}, indent=1))


# 2. Operating numbers.
def daily():
    write_csv("""
        select cast(pickup_datetime as date) as date, company,
            count(*) as trips,
            round(sum(base_passenger_fare) filter (where base_passenger_fare >= 0), 2) as fares,
            round(sum(driver_pay) filter (where base_passenger_fare >= 0), 2) as driver_pay,
            round(sum(tips), 2) as tips,
            count(*) filter (where wait_ok) as wait_trips,
            round(approx_quantile(wait_min, 0.5) filter (where wait_ok), 2) as wait_median,
            round(approx_quantile(wait_min, 0.9) filter (where wait_ok), 2) as wait_p90
        from t group by 1, 2 order by 1, 2
    """, "daily.csv")


def zone_week():
    write_csv("""
        select cast(date_trunc('week', pickup_datetime) as date) as week, PULocationID as zone,
            count(*) as trips,
            round(sum(base_passenger_fare) filter (where base_passenger_fare >= 0), 0) as fares,
            round(approx_quantile(wait_min, 0.5) filter (where wait_ok), 2) as wait_median,
            round(approx_quantile(wait_min, 0.9) filter (where wait_ok), 2) as wait_p90,
            round(avg(case when wait_min > 15 then 1.0 else 0.0 end) filter (where wait_ok), 4) as long_wait_share
        from t group by 1, 2 order by 1, 2
    """, "zone_week.csv")


# The latest four weeks drive the "when" views: hour of day by zone, and day by hour citywide.
RECENT = "pickup_datetime >= (select max(pickup_datetime) from trips) - interval 28 day"


def zone_hour():
    write_csv(f"""
        select PULocationID as zone, hour(pickup_datetime) as hour, count(*) as trips,
            round(approx_quantile(wait_min, 0.5) filter (where wait_ok), 2) as wait_median
        from t where {RECENT} group by 1, 2 order by 1, 2
    """, "zone_hour.csv")


def week_hour():
    write_csv(f"""
        select isodow(pickup_datetime) as dow, hour(pickup_datetime) as hour, count(*) as trips,
            round(approx_quantile(wait_min, 0.5) filter (where wait_ok), 2) as wait_median
        from t where {RECENT} group by 1, 2 order by 1, 2
    """, "week_hour.csv")


def pay_month():
    write_csv("""
        select file_month as month, company, count(*) as trips,
            round(sum(base_passenger_fare) filter (where base_passenger_fare >= 0), 0) as fares,
            round(sum(driver_pay) filter (where base_passenger_fare >= 0), 0) as driver_pay,
            round(sum(tips), 0) as tips,
            count(*) filter (where driver_pay > base_passenger_fare + tips + tolls + 1) as pay_above_fare
        from t group by 1, 2 order by 1, 2
    """, "pay_month.csv")


def zones():
    write_csv('select LocationID as zone, Borough as borough, Zone as name from zones order by 1', "zones.csv")


for label, fn in [("data quality, every rule over every row", dq_monthly), ("rule cards", dq_rules),
                  ("daily", daily), ("zone by week", zone_week), ("zone by hour", zone_hour),
                  ("day by hour", week_hour), ("pay by month", pay_month), ("zones", zones)]:
    step(label, fn)
print("done")
