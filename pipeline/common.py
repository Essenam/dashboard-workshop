"""Shared paths and the DuckDB connection for the data pipeline."""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SUMMARIES = ROOT / "data" / "summaries"
RAW_TRIPS_DIR = RAW / "2 trip data, all months in one file"
ZONES = (RAW / "taxi_zone_lookup.csv").as_posix()

# The dashboard covers the latest twelve months in the cache. Older files stay where they are,
# so changing this number never means downloading again.
MONTHS_SHOWN = 12


def trip_files():
    files = sorted(RAW_TRIPS_DIR.glob("fhvhv_tripdata_*.parquet"))[-MONTHS_SHOWN:]
    return [f.as_posix() for f in files]


def connect():
    con = duckdb.connect()
    con.sql(rf"""
        create view trips as
        select *, regexp_extract(filename, '(\d{{4}}-\d{{2}})\.parquet$', 1) as file_month
        from read_parquet({trip_files()!r}, filename = true)
    """)
    con.sql(f"create view zones as select * from read_csv('{ZONES}')")
    return con
