@echo off
chcp 65001 >nul
echo ============================================
echo  設定 ETF 00981A 自動持股更新排程
echo ============================================
echo.

set TASKNAME=ETF_00981A_Holdings_Update
set SCRIPT_DIR=d:\Gemini\ETF_Tracker
set PYTHON_EXE=%SCRIPT_DIR%\venv\Scripts\python.exe
set SCRIPT_FILE=%SCRIPT_DIR%\check_and_update.py

:: Delete existing task if any
schtasks /delete /tn "%TASKNAME%" /f >nul 2>&1

:: Create task with weekly schedule (Mon-Fri), starting at 16:00, repeat every 1 hour for 6 hours
:: This means it runs at: 16:00, 17:00, 18:00, 19:00, 20:00, 21:00, 22:00
schtasks /create ^
  /tn "%TASKNAME%" ^
  /tr "\"%PYTHON_EXE%\" \"%SCRIPT_FILE%\"" ^
  /sc weekly ^
  /d MON,TUE,WED,THU,FRI ^
  /st 16:00 ^
  /ri 60 ^
  /du 06:30 ^
  /f

if %errorlevel% equ 0 (
    echo.
    echo [成功] 排程已建立！
    echo   - 任務名稱: %TASKNAME%
    echo   - 執行時間: 週一~週五 16:00 起，每小時檢查一次
    echo   - 持續時間: 6.5 小時 (16:00 ~ 22:30)
    echo   - 腳本會自動判斷：
    echo     * 今天已更新 → 直接跳過
    echo     * 尚未更新   → 下個小時再試
    echo     * 更新完成   → 比對持股、產出 JSON、推送 GitHub
    echo.
) else (
    echo.
    echo [失敗] 無法建立排程，請以「系統管理員身分」執行此 bat 檔。
    echo.
)

pause
