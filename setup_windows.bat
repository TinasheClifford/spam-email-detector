@echo off
setlocal
cd /d "%~dp0"
set "SPAM_ENV=%USERPROFILE%\spam-env"
if not exist "%SPAM_ENV%\Scripts\python.exe" (
    python -m venv "%SPAM_ENV%"
    if errorlevel 1 goto failed
)
"%SPAM_ENV%\Scripts\python.exe" -m pip install --timeout 120 --retries 10 -r requirements.txt
if errorlevel 1 goto failed
echo Setup complete. Double-click start_windows.bat to open the app.
pause
exit /b 0
:failed
echo Setup failed. Read the error above and README.md. Please share the last error if you need help.
pause
exit /b 1
