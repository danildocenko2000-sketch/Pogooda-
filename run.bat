@echo off
cd /d "%~dp0weather"
echo Installing dependencies...
call npm install
if errorlevel 1 exit /b 1
echo.
echo Starting dev server (Pogoda weather)...
call npm run dev
pause
