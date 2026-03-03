@echo off
chcp 65001 >nul
cd /d "%~dp0"

where git >nul 2>&1
if errorlevel 1 (
    echo [Помилка] Git не знайдено. Встановіть: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Додаю зміни...
git add .
echo.
echo Статус:
git status
echo.
set /p MSG="Введіть опис змін (коміт): "
git commit -m "%MSG%"
if errorlevel 1 (
    echo Немає змін для коміту.
    pause
    exit /b 0
)
echo.
echo Відправляю на GitHub...
git push
if errorlevel 1 (
    echo Помилка push. Перевірте підключення та логін/токен.
)
echo.
pause
