import re

with open("check_and_update_00988A.py", "r", encoding="utf-8") as f:
    content = f.read()

old_logic = """    if file_date != today:
        log.info(f"File date ({file_date}) != today ({today}). Not yet updated. Will retry next hour.")
        if os.path.exists(xlsx_path):
            os.remove(xlsx_path)
        send_telegram(f"⏳ 00988A 持股尚未更新\\n📅 資料日期：{today_str}\\n🔄 將於下一個小時再次檢查...")
        return"""

new_logic = """    if file_date != today:
        log.info(f"File date ({file_date}) != today ({today}). Bypassing in dev mode!")
        # if os.path.exists(xlsx_path):
        #     os.remove(xlsx_path)
        # send_telegram(f"⏳ 00988A 持股尚未更新\\n📅 資料日期：{today_str}\\n🔄 將於下一個小時再次檢查...")
        # return"""

content = content.replace(old_logic, new_logic)

# Wait, `append_holdings_to_sheets` and git_push will run. Let's comment those out as well.
# Also the send_telegram(msg)
content = content.replace('append_holdings_to_sheets("00981A", wrapper["meta"]["dataDate"], wrapper["holdings"])', '# append_holdings_to_sheets')
content = content.replace('git_push()', '# git_push()')
content = content.replace('msg = build_notification(wrapper, etf_code="00981A", etf_name="統一台股增長")', '# build_notification')

with open("check_and_update_00988A.py", "w", encoding="utf-8") as f:
    f.write(content)
