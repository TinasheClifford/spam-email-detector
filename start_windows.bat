@echo off
setlocal
cd /d "%~dp0"
set "SPAM_ENV=%USERPROFILE%\spam-env"
if not exist "%SPAM_ENV%\Scripts\python.exe" (
    echo Run setup_windows.bat first.
    pause
    exit /b 1
)
"%SPAM_ENV%\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 pause
