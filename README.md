# Pogoda

Усе в одній папці: **Django (API погоди)** + **Vue (додаток погоди)**. Без сантехніки/store — тільки погода.

- **backend/** — Django, тільки ендпоінти `/api/weather/forecast/`, `search/`, `reverse/` (проксі на Open-Meteo та Nominatim).
- **weather/** — Vue 3 + Vite, фронт погоди; запити йдуть на backend.

## Запуск

**1. Backend (Django):**
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```
→ http://localhost:8000

**2. Frontend (Vue):**
```bash
cd weather
npm install
npm run dev
```
→ відкрити URL Vite (наприклад http://localhost:5173). У `weather/.env` задано `VITE_API_URL=http://localhost:8000` — запити погоди йдуть на Django.

## Збірка фронту

```bash
cd weather
npm run build
```
→ `weather/dist/`
