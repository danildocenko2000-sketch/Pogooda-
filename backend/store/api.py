# -*- coding: utf-8 -*-
"""
Окремий модуль API: товари для Vue.
Роути підключаються в santehnika_django/urls.py.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Product
from . import views as store_views


def parse_id_filter(value):
    """Парсить id з GET: '1', '1,2,3' → [1, 2, 3]. Невалідні — пропускає."""
    if not value or not value.strip():
        return None
    ids = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            continue
    return ids if ids else None


@require_GET
def api_products(request):
    """
    Список товарів. Фільтр: ?id=1 або ?id=1,2,3 — один/кілька; без id — всі.

    ---
    request (django.http.HttpRequest)
    --------------------------------
    Об'єкт HTTP-запиту. Основні атрибути й методи:

    • request.method — рядок методу: "GET", "POST", "PUT", "DELETE" тощо.
      Для цього view завжди "GET" (обмежено @require_GET).

    • request.GET — django.http.QueryDict, мультизначний словник GET-параметрів.
      Доступ: request.GET.get("key"), request.GET.get("key", default),
      request.GET.getlist("key") — список усіх значень для ключа,
      request.GET.keys(), request.GET.items(), "key" in request.GET.

    • request.POST — QueryDict для тіла форми (POST). Для GET-запитів не використовується.

    • request.body — bytes тіла запиту (для GET зазвичай порожній).

    • request.path — шлях URL без домену й query: "/api/products/".

    • request.get_full_path() — path + query: "/api/products/?id=1,2".

    • request.META — словник HTTP-заголовків і серверних змінних:
      CONTENT_TYPE, HTTP_ACCEPT, HTTP_HOST, REMOTE_ADDR, REQUEST_METHOD тощо.

    • request.headers — об'єкт з доступом до заголовків (request.headers.get("Accept")).

    • request.content_type — MIME-тип тіла (для GET зазвичай порожній).

    • request.user — django.contrib.auth.models.AnonymousUser або User (якщо є авторизація).

    • request.session — об'єкт сесії (якщо сесії увімкнені).

    • request.resolver_match — інформація про збіг URL (name, args, kwargs, url_name).

    • request.COOKIES — словник cookies з запиту.

    • request.FILES — файли, завантажені у запиті (для multipart/form-data).

    • request.scheme — "http" або "https".

    • request.get_host() — хост з заголовка Host.

    • request.is_secure() — True якщо scheme == "https".

    • request.is_ajax() — застаріло; замість нього перевіряти заголовок X-Requested-With.

    Параметри запиту (query string) для /api/products/
    -------------------------------------------------
    • id (optional, str) — один або кілька id товарів через кому.
      Приклади: "1", "1,2,5". Нечислові частини ігноруються.
      Відсутній або порожній — повертаються всі товари.

    Відповідь (response)
    --------------------
    • Тип: django.http.JsonResponse (підклас HttpResponse).
    • Content-Type: application/json.
    • Тіло: JSON-масив об'єктів товарів (див. формат нижче).
    • Код статусу: 200.

    Формат одного елемента масиву (товар):
    • id (int), name (str), category (str), subcategory (str), sub_subcategory (str),
    • price (number), oldPrice (number), image (str), badge (str | null), description (str),
    • in_stock (bool), quantity (int), rating (float), rating_count (int).
    """
    products_raw = store_views._products_from_db()
    if products_raw is None:
        products = store_views._normalize_products(store_views.PRODUCTS)
    else:
        products = products_raw

    id_param = request.GET.get("id")
    ids = parse_id_filter(id_param) if id_param is not None else None
    if ids is not None:
        id_set = set(ids)
        products = [p for p in products if p.get("id") in id_set]
        # зберегти порядок як в запиті
        order = {pk: i for i, pk in enumerate(ids)}
        products.sort(key=lambda p: order.get(p.get("id"), 999))

    return JsonResponse(products, safe=False)


@require_GET
def api_product_detail(request, pk):
    """Один товар по id (з моделі Product або з data.PRODUCTS)."""
    try:
        product = Product.objects.filter(pk=pk).values(
            "id", "name", "category", "subcategory", "sub_subcategory", "price", "old_price",
            "image", "badge", "description", "in_stock", "quantity", "sort_order", "rating", "rating_count"
        ).first()
        if product:
            return JsonResponse(store_views._product_to_api_dict(product))
    except (ValueError, TypeError):
        pass
    for p in store_views._normalize_products(store_views.PRODUCTS):
        if p.get("id") == pk:
            return JsonResponse(p)
    return JsonResponse({"error": "Товар не знайдено"}, status=404)
