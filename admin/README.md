# Адмін-панель на Vue (WORLD OF Santehnika)

Окремий фронтенд для керування товарами та налаштуваннями сайту. Працює з API Django (авторизація по токену).

## Що потрібно

- Запущений Django-сервер (наприклад `http://localhost:8000`)
- Користувач з правами персоналу (is_staff) для входу

## Запуск (режим розробки)

1. У корені проєкту Django:
   ```bash
   python manage.py runserver
   ```
2. У папці `admin_panel`:
   ```bash
   npm install
   npm run dev
   ```
3. Відкрити в браузері URL, який покаже Vite (наприклад `http://localhost:5173`).
4. Увійти логіном і паролем Django-адміністратора.

Файл `.env` містить `VITE_API_URL=http://localhost:8000` — усі запити йдуть на цей адрес.

## Збірка для продакшену

```bash
npm run build
```

Файли збираються в `dist/`. Їх можна роздавати окремим веб-сервером або підключити до Django (статичні файли + fallback на `index.html` для SPA).

## API (Django)

- `POST /api/auth/login/` — логін (username, password) → токен
- `GET /api/auth/me/` — поточний користувач (заголовок `Authorization: Bearer <token>`)
- `POST /api/auth/logout/` — вихід (інвалідація токена)
- `GET /api/settings/` — налаштування сайту (публічно)
- `PATCH /api/admin/settings/` — оновлення налаштувань (тільки для staff)
- `GET /api/products/` — список товарів (публічно)
- `GET /api/products/<id>/` — один товар (публічно)
- `POST /api/admin/products/` — створення товару
- `PATCH /api/admin/products/<id>/` — оновлення товару
- `DELETE /api/admin/products/<id>/delete/` — видалення товару
