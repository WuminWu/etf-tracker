@echo off
echo 設定 ETF 00981A 每日下午 6:00 自動更新爬蟲...

set TASKNAME="ETF_00981A_Daily_Update"
set SCRIPT_DIR=d:\Gemini\ETF_00981A
set PYTHON_EXE=%SCRIPT_DIR%\venv\Scripts\python.exe
set SCRIPT_FILE=%SCRIPT_DIR%\scraper.py

:: Create the scheduled task
schtasks /create /tn %TASKNAME% /tr "\"%PYTHON_EXE%\" \"%SCRIPT_FILE%\"" /sc daily /st 18:00 /f

if %errorlevel% equ 0 (
    echo.
    echo [成功] 系統排程已建立！每天 18:00 將自動在背景執行更新程式。
) else (
    echo.
    echo [失敗] 無法建立排程，請對此 bat 檔案點擊「右鍵 - 以系統管理員身分執行」。
)

pause
