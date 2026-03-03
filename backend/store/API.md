# API бекенду (Vue + Django)

API тільки по продуктах (2 запити). Дані віддаються з моделі **Product** (таблиця товарів); якщо БД порожня — fallback на `store/data.PRODUCTS`.

## Ендпоінти

| Метод | URL | Опис |
|-------|-----|------|
| GET | `/api/products/` | Список товарів. Фільтр: `?id=1` — один, `?id=1,2,3` — кілька, без `id` — всі |
| GET | `/api/products/<id>/` | Один товар по `id` |

## Формат товару (JSON)

- `id`, `name`, `category`, `subcategory`, `sub_subcategory`
- `price`, `oldPrice`, `image`, `badge`, `description`
- `in_stock`, `quantity`, `rating`, `rating_count`

## Модель Product (Django)

У `store/models.py`: товар з полями name, category, subcategory, sub_subcategory, price, old_price, image, badge, description, in_stock, quantity, sort_order, rating, rating_count. Адмінка: `/admin/` → Товари.

## CORS

Для запитів з Vue (інший порт) увімкнено CORS: заголовок `Access-Control-Allow-Origin: *` для шляхів `/api/`.
