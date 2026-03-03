# Backend Pogoda (Django)

Тільки API погоди: Vue робить запити сюди, Django проксує на Open-Meteo та Nominatim.

## Ендпоінти

- `GET /api/weather/forecast/?latitude=&longitude=` — прогноз на 7 днів
- `GET /api/weather/search/?q=&only_ukraine=0|1` — пошук міст
- `GET /api/weather/reverse/?lat=&lon=` — назва місця за координатами

## Запуск

```bash
pip install -r requirements.txt
python manage.py runserver
```

Сервер: http://localhost:8000
