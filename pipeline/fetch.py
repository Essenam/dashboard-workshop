"""Check TLC for new monthly trip files, and download the ones missing from the cache.

    uv run python pipeline/fetch.py                  # list what TLC has that we do not; downloads nothing
    uv run python pipeline/fetch.py --download       # download those months, one at a time
    uv run python pipeline/fetch.py --check-updates  # also ask whether TLC re-uploaded a month we hold

Source: NYC Taxi and Limousine Commission, TLC Trip Record Data
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

TLC's file server blocks clients that make repeated or parallel requests, so this script asks
about one file at a time with a pause between requests, and never downloads a file that is
already in data/raw/. Each download is checked against the size the server announced, then
saved beside a .headers.json file recording what the server said, as the original copies have.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from common import RAW_TRIPS_DIR

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_{month}.parquet"
PAUSE_SECONDS = 2
USER_AGENT = "dashboard-workshop data pipeline (one request at a time)"


def month_add(month, n):
    y, m = map(int, month.split("-"))
    total = y * 12 + (m - 1) + n
    return f"{total // 12:04d}-{total % 12 + 1:02d}"


def cached_months():
    return sorted(re.search(r"(\d{4}-\d{2})\.parquet$", p.name).group(1)
                  for p in RAW_TRIPS_DIR.glob("fhvhv_tripdata_*.parquet"))


def head(month):
    """Ask TLC about one month's file. Returns its headers, or None if it is not published."""
    req = urllib.request.Request(BASE_URL.format(month=month), method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return dict(resp.headers)
    except urllib.error.HTTPError as e:
        if e.code in (403, 404):  # TLC's server answers 403 for a file that does not exist yet
            return None
        raise
    finally:
        time.sleep(PAUSE_SECONDS)


def download(month, expected_size):
    target = RAW_TRIPS_DIR / f"fhvhv_tripdata_{month}.parquet"
    partial = target.with_suffix(".parquet.part")
    req = urllib.request.Request(BASE_URL.format(month=month), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp, open(partial, "wb") as out:
        headers = dict(resp.headers)
        done = 0
        while chunk := resp.read(1 << 20):
            out.write(chunk)
            done += len(chunk)
            print(f"\r  {month}: {done / 1e6:,.0f} of {expected_size / 1e6:,.0f} MB", end="", flush=True)
    print()
    if done != expected_size:
        partial.unlink()
        raise RuntimeError(f"{month}: got {done} bytes, server announced {expected_size}; nothing saved")
    partial.rename(target)
    (RAW_TRIPS_DIR / f"{target.name}.headers.json").write_text(json.dumps(headers, indent=2))
    time.sleep(PAUSE_SECONDS)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--download", action="store_true", help="download the missing months")
    parser.add_argument("--check-updates", action="store_true", help="check whether TLC re-uploaded a month we hold")
    args = parser.parse_args()

    have = cached_months()
    if not have:
        sys.exit(f"No trip files in {RAW_TRIPS_DIR}. Copy the workshop files in first.")
    print(f"In the cache: {have[0]} to {have[-1]} ({len(have)} months)")

    # Ask about each month after the newest one we hold, up to last month. TLC publishes with a
    # lag of about two months, so the most recent ones are usually not there yet.
    last_month = month_add(date.today().strftime("%Y-%m"), -1)
    new = []
    month = month_add(have[-1], 1)
    while month <= last_month:
        h = head(month)
        if h:
            size = int(h.get("Content-Length", 0))
            print(f"  {month}: published, {size / 1e6:,.0f} MB, last modified {h.get('Last-Modified')}")
            new.append((month, size))
        else:
            print(f"  {month}: not published yet")
        month = month_add(month, 1)

    if args.check_updates:
        print("Checking the months we hold for re-uploads:")
        for month in have:
            saved_file = RAW_TRIPS_DIR / f"fhvhv_tripdata_{month}.parquet.headers.json"
            # Header names are case-insensitive, and some saved files store them in lowercase.
            saved = {k.lower(): v for k, v in json.loads(saved_file.read_text()).items()} if saved_file.exists() else {}
            h = {k.lower(): v for k, v in (head(month) or {}).items()}
            same = h.get("etag") == saved.get("etag") and h.get("content-length") == saved.get("content-length")
            print(f"  {month}: {'unchanged' if same else 'CHANGED on TLC since we downloaded it'}")

    if not new:
        print("Nothing new to download.")
        return
    if not args.download:
        total = sum(s for _, s in new)
        print(f"{len(new)} new month(s), {total / 1e6:,.0f} MB in all. Run again with --download to fetch them.")
        return
    for month, size in new:
        download(month, size)
    print("Downloaded. Next: uv run python pipeline/build_summaries.py")


if __name__ == "__main__":
    main()
