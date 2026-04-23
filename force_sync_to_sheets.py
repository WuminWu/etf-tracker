"""
Force-sync all ETF holdings from local data_*.json to Google Sheets.

Usage:
  python force_sync_to_sheets.py            # sync all ETFs (skip existing records)
  python force_sync_to_sheets.py --dedup    # also run dedup cleanup after syncing

Reads the actual dataDate from each JSON's meta field (no hardcoded date).
Skips ETFs that already have an entry for that dataDate in Sheets (safe to re-run).
"""

import json
import glob
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

from sheets_helper import append_holdings_to_sheets, delete_duplicate_rows


def main():
    run_dedup = "--dedup" in sys.argv

    files = sorted(f for f in glob.glob("data_*.json") if "index" not in f)
    if not files:
        log.warning("No data_*.json files found.")
        return

    log.info(f"Found {len(files)} ETF data files to sync.")

    for f in files:
        etf_code = f.replace("data_", "").replace(".json", "")
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
        except Exception as e:
            log.error(f"Failed to read {f}: {e}")
            continue

        meta     = data.get("meta", {})
        holdings = data.get("holdings", [])
        data_date = meta.get("dataDate", "")

        if not data_date:
            log.warning(f"{etf_code}: no dataDate in meta, skipping.")
            continue

        log.info(f"Syncing {etf_code} | dataDate={data_date} | holdings={len(holdings)}")
        append_holdings_to_sheets(etf_code, data_date, holdings, meta=meta)

    if run_dedup:
        log.info("Running dedup cleanup...")
        deleted = delete_duplicate_rows()
        log.info(f"Dedup complete — {deleted} rows removed.")

    log.info("Force sync finished.")


if __name__ == "__main__":
    main()
