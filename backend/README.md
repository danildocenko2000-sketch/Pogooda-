# Backend (Django) — API у форматі JSON

Усі ендпоінти API повертають **JSON** (`Content-Type: application/json`).

## Запуск

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API (JSON)

| Метод | URL | Опис |
|------|-----|------|
| GET | `/api/products/` | Список товарів (JSON-масив) |
| GET | `/api/products/<id>/` | Один товар (JSON-об'єкт) |
| GET | `/api/settings/` | Налаштування сайту (JSON) |
| POST | `/api/auth/login/` | Логін, тіло JSON → у відповіді JSON з полем `token` |
| GET | `/api/auth/me/` | Поточний користувач (заголовок `Authorization: Bearer <token>`) |
| POST | `/api/auth/logout/` | Вихід (інвалідація токена) |
| PATCH | `/api/admin/settings/` | Оновлення налаштувань (JSON body, потрібен Bearer) |
| POST | `/api/admin/products/` | Створення товару (JSON body) |
| PATCH | `/api/admin/products/<id>/` | Оновлення товару (JSON body) |
| DELETE | `/api/admin/products/<id>/delete/` | Видалення товару |

Усі відповіді — JSON; помилки теж у вигляді JSON (наприклад `{"error": "..."}`).
