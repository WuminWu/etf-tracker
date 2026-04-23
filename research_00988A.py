from playwright.sync_api import sync_playwright
import time
import os

def main():
    FUND_URL = "https://www.ezmoney.com.tw/ETF/Fund/Info?fundCode=61YTW"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print(f"Navigating to {FUND_URL} ...")
        page.goto(FUND_URL, wait_until="networkidle")
        time.sleep(3)

        # Click 基金投資組合 tab
        portfolio_link = page.locator("a:has-text('基金投資組合')")
        if portfolio_link.count() > 0:
            portfolio_link.first.click()
            print("Clicked 基金投資組合 tab")
            page.wait_for_timeout(5000)
        else:
            print("基金投資組合 tab not found, trying anchor link")
            page.goto(FUND_URL + "#asset", wait_until="networkidle")
            page.wait_for_timeout(5000)

        page.screenshot(path="d:\\Self_Tools\\ETF_Tracker\\00988A_screenshot.png")
        print("Saved screenshot to 00988A_screenshot.png")

        # Dump some HTML
        html = page.locator("body").inner_html()
        with open("d:\\Self_Tools\\ETF_Tracker\\00988A_html.txt", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved HTML to 00988A_html.txt")

        browser.close()

if __name__ == "__main__":
    main()
