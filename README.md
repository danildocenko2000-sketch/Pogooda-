# Pogoda — додаток погоди (Weather App)

Vue 3 + Vite. Прогноз по Open-Meteo, геолокація, пошук міст. **Запити можуть йти через Django:** Vue → Django → Open-Meteo / Nominatim.

## Зв’язок Vue ↔ Django

- У `weather/.env` задано **VITE_API_URL=http://localhost:8000**.
- Vue (додаток погоди) робить запити на Django: `/api/weather/forecast/`, `/api/weather/search/`, `/api/weather/reverse/`.
- Django (backend) проксує їх на Open-Meteo та Nominatim і повертає JSON у відповідь.

## Запуск (Django + Vue разом)

**1. Запустити Django (backend):**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Сервер: http://localhost:8000

**2. Запустити Vue (погода):**
```bash
cd weather
npm install
npm run dev
```
Відкрити в браузері URL від Vite (наприклад http://localhost:5173). Запити погоди підуть на Django.

Якщо Django не запущено — у `weather/.env` можна закоментувати або прибрати `VITE_API_URL`; тоді Vue буде звертатися напряму до Open-Meteo та Nominatim.

## Збірка

```bash
cd weather
npm run build
```

Файли збираються в `weather/dist/`.
