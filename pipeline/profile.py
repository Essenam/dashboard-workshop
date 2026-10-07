"""Profile every row of the trip files: types, null rates, ranges, distinct counts.

Writes data/summaries/profile.json. Run with: uv run python pipeline/profile.py
"""
import json

from common import SUMMARIES, connect

con = connect()
rows = con.sql("summarize select * exclude (filename) from trips").fetchall()
cols = [d[0] for d in con.sql("summarize select 1 as x").description]
profile = [dict(zip(cols, r)) for r in rows]

flags = {}
for c in ["hvfhs_license_num", "shared_request_flag", "shared_match_flag",
          "access_a_ride_flag", "wav_request_flag", "wav_match_flag"]:
    flags[c] = con.sql(f"select {c} as value, count(*) as n from trips group by 1 order by 2 desc").fetchall()

out = {"columns": profile, "categorical": {k: [[v, n] for v, n in vals] for k, vals in flags.items()}}
SUMMARIES.mkdir(parents=True, exist_ok=True)
(SUMMARIES / "profile.json").write_text(json.dumps(out, indent=2, default=str))
for p in profile:
    print(p["column_name"], p["column_type"], "min", p["min"], "max", p["max"], "null%", p["null_percentage"], "approx_unique", p["approx_unique"])
print(json.dumps(out["categorical"], indent=1))
