import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import yfinance as yf


def update_twii_ytd():
    twii_ytd = "0.00"
    try:
        hist = yf.Ticker("^TWII").history(period="ytd", timeout=10)
        if len(hist) >= 2:
            first = hist["Close"].iloc[0]
            last = hist["Close"].iloc[-1]
            twii_ytd = f"{((last - first) / first) * 100:.2f}"
            print(f"TWII YTD: {twii_ytd}%")
        else:
            print("Not enough historical data for ^TWII")
    except Exception as e:
        print(f"Error fetching ^TWII: {e}", file=sys.stderr)

    data = {
        "twii_ytd": twii_ytd,
        "lastUpdate": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M"),
    }
    with open("data_index.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved data_index.json: twii_ytd={twii_ytd}%")


if __name__ == "__main__":
    update_twii_ytd()
