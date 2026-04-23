import re

with open("check_and_update_00981A.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replacements
content = content.replace("00981A", "00988A")
content = content.replace("49YTW", "61YTW")
content = content.replace("陳釧瑤", "陳意婷")
content = content.replace("統一台股增長", "主動統一全球創新")

# Button replace
old_btn = 'export_btn = page.locator("button:has-text(\'匯出XLSX\')")\n        if export_btn.count() == 0:\n            export_btn = page.locator("button:has-text(\'匯出\')")\n        if export_btn.count() == 0:\n            export_btn = page.locator("a:has-text(\'匯出XLSX\')")'
new_btn = 'export_btn = page.locator("a:has-text(\'匯出Excel\'), a:has-text(\'匯出xlsx檔\')")\n        if export_btn.count() == 0:\n            export_btn = page.locator("button:has-text(\'匯出Excel\'), button:has-text(\'匯出xlsx檔\')")'

if "button:has-text('匯出XLSX')" in content:
    content = content.replace(old_btn, new_btn)
else:
    # try another way
    old_btn_2 = 'export_btn = page.locator("a:has-text(\'匯出Excel\')")\n        if export_btn.count() == 0:\n            export_btn = page.locator("button:has-text(\'匯出Excel\')")'
    content = content.replace(old_btn_2, new_btn)


# get_price replace
old_get_price = '''def get_price(code):
    """Fetch current stock price from Yahoo Finance."""
    for suffix in [".TW", ".TWO"]:
        try:
            ticker = yf.Ticker(f"{code}{suffix}")
            hist = ticker.history(period="1d", timeout=10)
            if not hist.empty:
                return float(hist["Close"].iloc[-1])
        except Exception:
            pass
    return 0.0'''

new_get_price = '''def get_price(code_str):
    """Fetch current stock price from Yahoo Finance."""
    parts = code_str.strip().split()
    base = parts[0]
    
    if len(parts) == 1:
        # Taiwan stock
        suffixes = [".TW", ".TWO"]
        for suffix in suffixes:
            try:
                hist = yf.Ticker(f"{base}{suffix}").history(period="1d", timeout=10)
                if not hist.empty: return float(hist["Close"].iloc[-1])
            except: pass
    elif len(parts) == 2:
        market = parts[1].upper()
        # Mapping for international markets
        market_map = {
            "US": "", "JP": ".T", "KS": ".KS", "HK": ".HK", 
            "GY": ".DE", "FP": ".PA", "LN": ".L", "SG": ".SI"
        }
        yf_ticker = f"{base}{market_map.get(market, '')}"
        try:
            hist = yf.Ticker(yf_ticker).history(period="1d", timeout=10)
            if not hist.empty: return float(hist["Close"].iloc[-1])
        except: pass
        
    return 0.0'''

content = content.replace(old_get_price, new_get_price)

# update usages of get_price(code) to get_price(code) still works because the arg name doesn't matter for caller

with open("check_and_update_00988A.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement done!")
