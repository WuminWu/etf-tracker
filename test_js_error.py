from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"CONSOLE {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"ERROR: {err.message}"))
        
        page.goto("http://localhost:8000/")
        page.wait_for_timeout(2000)
        # click cross compare tab
        page.locator("button[data-tab='cross']").click()
        page.wait_for_timeout(2000)
        
        browser.close()

if __name__ == "__main__":
    main()
