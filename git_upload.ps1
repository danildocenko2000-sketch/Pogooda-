# Оновлюємо PATH з реєстру (щоб побачити Git після встановлення)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git не знайдено в PATH. Спробуйте: 1) Закрити і знову відкрити Cursor; 2) Запустити git_first_upload.bat двічі клацанням у провіднику." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path ".git")) {
    Write-Host "Ініціалізую репозиторій..."
    git init
}

$remoteUrl = "https://github.com/danildocenko2000-sketch/Pogooda-.git"
$hasOrigin = git remote get-url origin 2>$null
if (-not $hasOrigin) {
    Write-Host "Додаю віддалений репозиторій..."
    git remote add origin $remoteUrl
}

Write-Host "Додаю файли..."
git add .
Write-Host "Коміт..."
git commit -m "Перше завантаження: Pogoda (backend, weather, admin)" 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "(немає нових змін або коміт вже було зроблено)" }
Write-Host "Відправляю на GitHub (main)..."
git branch -M main
git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Помилка push. Якщо просить логін — використовуйте Personal Access Token замість пароля." -ForegroundColor Yellow
    exit 1
}
Write-Host "Готово. Проєкт завантажено на https://github.com/danildocenko2000-sketch/Pogooda-" -ForegroundColor Green
