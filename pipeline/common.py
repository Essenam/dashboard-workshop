"""Shared paths and the DuckDB connection for the data pipeline."""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SUMMARIES = ROOT / "data" / "summaries"
TRIPS = (RAW / "2 trip data, all months in one file" / "fhvhv_tripdata_*.parquet").as_posix()
ZONES = (RAW / "taxi_zone_lookup.csv").as_posix()


def connect():
    con = duckdb.connect()
    con.sql(rf"""
        create view trips as
        select *, regexp_extract(filename, '(\d{{4}}-\d{{2}})\.parquet$', 1) as file_month
        from read_parquet('{TRIPS}', filename = true)
    """)
    con.sql(f"create view zones as select * from read_csv('{ZONES}')")
    return con
