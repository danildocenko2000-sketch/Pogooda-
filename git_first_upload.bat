@echo off
chcp 65001 >nul
cd /d "%~dp0"

where git >nul 2>&1
if errorlevel 1 (
    echo [Помилка] Git не знайдено. Встановіть: https://git-scm.com/download/win
    pause
    exit /b 1
)

if not exist ".git" (
    echo Ініціалізую репозиторій...
    git init
)

git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Додаю віддалений репозиторій...
    git remote add origin https://github.com/danildocenko2000-sketch/Pogooda-.git
)

echo.
echo Додаю всі файли...
git add .
echo.
echo Створюю перший коміт...
git commit -m "Перше завантаження: Pogoda (backend, weather, admin)"
if errorlevel 1 (
    echo Немає змін для коміту або коміт вже було зроблено.
)

echo.
echo Відправляю на GitHub (гілка main)...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo Якщо просить логін: використовуйте Personal Access Token замість пароля.
    echo Створити: GitHub - Settings - Developer settings - Personal access tokens
)
echo.
pause
