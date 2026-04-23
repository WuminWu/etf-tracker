import re

with open("check_and_update_00988A.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the click part
old_click = """        with page.expect_download(timeout=30000) as download_info:
            export_btn.first.click()
            log.info("Clicked export button, waiting for download...")"""

old_click_force = """        with page.expect_download(timeout=30000) as download_info:
            export_btn.first.click(force=True)
            log.info("Clicked export button, waiting for download...")"""

new_click = """        with page.expect_download(timeout=30000) as download_info:
            export_btn.first.evaluate("el => el.click()")
            log.info("Evaluated click on export button, waiting for download...")"""

if old_click_force in content:
    content = content.replace(old_click_force, new_click)
elif old_click in content:
    content = content.replace(old_click, new_click)

with open("check_and_update_00988A.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Replaced click with evaluate.")
