# Pogoda — все в одному місці

Тут зібрано **бекенд (Django + API JSON)**, **додаток погоди (Vue)** та **адмінку (Vue)**. Усі API віддають **JSON**.

## Структура

| Папка      | Опис |
|------------|------|
| **backend/** | Django-проєкт: сайт, API (товари, налаштування, авторизація). Усі відповіді — JSON. |
| **weather/** | Vue 3 + Vite — додаток погоди (Open-Meteo, геолокація, почасовий прогноз). |
| **admin/**   | Vue 3 + Vite + Router — адмін-панель (логін по токену, товари, налаштування). |

## Як запускати

### 1. Бекенд (Django, API)

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Сервер: **http://localhost:8000**  
Django admin: **http://localhost:8000/admin/**  
API (JSON): **http://localhost:8000/api/**

### 2. Погода (Vue)

```bash
cd weather
npm install
npm run dev
```

Відкрити в браузері URL, який покаже Vite (наприклад **http://localhost:5173**).

### 3. Адмінка (Vue)

```bash
cd admin
npm install
npm run dev
```

Відкрити в браузері (наприклад **http://localhost:5174**). Логін — користувач Django з правами staff (токен у заголовку, усі запити до API — JSON).

## API (JSON)

- **GET** `/api/products/` — список товарів (JSON).
- **GET** `/api/products/<id>/` — один товар (JSON).
- **GET** `/api/settings/` — налаштування сайту (JSON).
- **POST** `/api/auth/login/` — логін (JSON body → JSON з токеном).
- **GET** `/api/auth/me/` — поточний користувач (JSON).
- **POST** `/api/auth/logout/` — вихід.
- **PATCH** `/api/admin/settings/` — оновлення налаштувань (JSON).
- **POST** `/api/admin/products/` — створення товару (JSON).
- **PATCH** `/api/admin/products/<id>/` — оновлення товару (JSON).
- **DELETE** `/api/admin/products/<id>/delete/` — видалення товару.

Усі відповіді мають `Content-Type: application/json`.

## Скрипти

- **run_backend.bat** — запуск Django з папки `backend`.
- **run_weather.bat** — запуск додатку погоди з папки `weather`.
- **run_admin.bat** — запуск адмінки з папки `admin`.
