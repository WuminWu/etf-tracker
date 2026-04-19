import json
import time
import os
import pandas as pd
from playwright.sync_api import sync_playwright
import yfinance as yf
from datetime import datetime, timedelta

FUND_CODE = "49YTW"
HISTORY_DIR = "history"

# Change to script directory to allow Windows Task Scheduler relative paths
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

def is_valid_stock_code(code):
    return len(code) >= 4 and any(c.isdigit() for c in code)

def fetch_pcf_for_date(page, date_minguo):
    print(f"Fetching PCF for date {date_minguo}...")
    page.goto(f"https://www.ezmoney.com.tw/ETF/Transaction/PCF?fundCode={FUND_CODE}")
    
    if date_minguo:
        # Force set the Minguo date into the input field #ED and submit
        page.evaluate(f"document.getElementById('ED').value = '{date_minguo}'")
        # Click the search button, assuming it has class btn-primary next to it
        page.locator("button.btn-primary").first.click()
        page.wait_for_timeout(4000) # give it time to load dynamic data
    else:
        # Wait for default table load
        try:
            page.wait_for_selector("table", timeout=15000)
            time.sleep(3)
        except:
            pass

    holdings = []
    rows = page.query_selector_all("table tbody tr")
    for row in rows:
        tds = row.query_selector_all("td")
        if len(tds) >= 4:
            code_text = tds[0].inner_text().strip()
            name_text = tds[1].inner_text().strip()
            shares_text = tds[2].inner_text().strip().replace(',', '')
            weight_text = tds[3].inner_text().strip()
            
            if is_valid_stock_code(code_text) and shares_text.isdigit():
                w_val = 0.0
                if '%' in weight_text:
                    try:
                        w_val = float(weight_text.replace('%',''))
                    except:
                        pass
                
                holdings.append({
                    "code": code_text,
                    "name": name_text,
                    "shares": int(shares_text),
                    "weight": w_val
                })
    return holdings

def get_price(code):
    for suffix in [".TW", ".TWO"]:
        try:
            ticker = yf.Ticker(f"{code}{suffix}")
            hist = ticker.history(period="1d")
            if not hist.empty:
                return float(hist['Close'].iloc[-1])
        except:
            pass
    return 0.0

def load_history(date_str):
    filepath = os.path.join(HISTORY_DIR, f"{date_str}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_history(date_str, data):
    filepath = os.path.join(HISTORY_DIR, f"{date_str}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    print("Initiating Scraper for Daily Diff...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Hardcoded requirement: 4/17 and 4/16 logic
        # Ideally, we should dynamically find the last 2 trading dates, 
        # but for this specific instruction, we'll fetch them precisely to bootstrap.
        date_today = "2026-04-17"
        date_yest = "2026-04-16"
        minguo_today = "115/04/17"
        minguo_yest = "115/04/16"
        
        # In a real daily cron, we'd do: minguo_today = f"{datetime.now().year-1911}/{datetime.now().strftime('%m/%d')}"

        # 1. Get Yesterday's PCF
        holdings_yest = load_history(date_yest)
        if not holdings_yest:
            holdings_yest = fetch_pcf_for_date(page, minguo_yest)
            if holdings_yest:
                save_history(date_yest, holdings_yest)

        # 2. Get Today's PCF
        holdings_today = load_history(date_today)
        if not holdings_today:
            holdings_today = fetch_pcf_for_date(page, minguo_today)
            if holdings_today:
                save_history(date_today, holdings_today)
                
        browser.close()

    if not holdings_today or not holdings_yest:
        print("Error: Could not retrieve data for comparison.")
        return

    # Convert yesterday's holdings to a lookup dict for both shares and weight
    dict_yest = {h['code']: h for h in holdings_yest}
    
    # Generate diffs
    final_output = []
    print(f"Calculating diffs for {len(holdings_today)} holdings...")
    
    for h in holdings_today:
        code = h['code']
        name = h['name']
        shares_today = h['shares']
        weight_today = h.get('weight', 0.0)
        
        yest_data = dict_yest.get(code, {})
        shares_yest = yest_data.get('shares', 0)
        weight_yest = yest_data.get('weight', 0.0)
        
        diff_shares = shares_today - shares_yest
        
        # We fetch for all to show the current price even if diff is 0, optional.
        price = get_price(code)
        diff_amount = diff_shares * price
        
        final_output.append({
            "code": code,
            "name": name,
            "shares": shares_today,
            "price": round(price, 2),
            "yestWeight": weight_yest,
            "todayWeight": weight_today,
            "diffShares": diff_shares,
            "diffAmount": round(diff_amount, 2)
        })

    # Sort primarily by todayWeight descending (user requirement)
    final_output = sorted(final_output, key=lambda x: x['todayWeight'], reverse=True)
    
    # Assign ranks based on todayWeight
    for idx, item in enumerate(final_output):
        item['rank'] = idx + 1
        
    # Calculate YTD performance for 00981A
    ytd_val = "0.0"
    try:
        ytd_hist = yf.Ticker("00981A.TW").history(period="ytd")
        if len(ytd_hist) >= 2:
            first_price = ytd_hist['Close'].iloc[0]
            last_price = ytd_hist['Close'].iloc[-1]
            ytd_calc = ((last_price - first_price) / first_price) * 100
            ytd_val = f"{ytd_calc:.2f}"
    except:
        pass
        
    wrapper = {
        "meta": {
            "manager": "陳釧瑤",
            "ytd": ytd_val
        },
        "holdings": final_output
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(wrapper, f, ensure_ascii=False, indent=4)
        
    print(f"Diff calculation complete! Saved to data.json")

if __name__ == "__main__":
    main()
