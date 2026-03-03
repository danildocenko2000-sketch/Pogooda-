# -*- coding: utf-8 -*-
"""
API для Vue-адмінки: авторизація по токену, налаштування, CRUD товарів.
"""
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import AuthToken, Product, SiteSettings
from . import views as store_views


def get_user_from_request(request):
    """Повертає User за заголовком Authorization: Bearer <token> або None."""
    auth = request.headers.get("Authorization") or ""
    if not auth.startswith("Bearer "):
        return None
    key = auth[7:].strip()
    if not key:
        return None
    try:
        token = AuthToken.objects.select_related("user").get(key=key)
        return token.user
    except AuthToken.DoesNotExist:
        return None


def require_staff(fn):
    """Декоратор: лише is_authenticated та is_staff."""
    def wrapped(request, *args, **kwargs):
        user = get_user_from_request(request)
        if not user or not user.is_authenticated or not user.is_staff:
            return JsonResponse({"error": "Потрібна авторизація адміністратора"}, status=401)
        request.api_user = user
        return fn(request, *args, **kwargs)
    return wrapped


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """POST { "username": "...", "password": "..." } -> { "token": "..." } або 401."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Невалідний JSON"}, status=400)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return JsonResponse({"error": "Вкажіть username та password"}, status=400)
    from django.contrib.auth import authenticate
    user = authenticate(request, username=username, password=password)
    if not user or not user.is_staff:
        return JsonResponse({"error": "Невірний логін або пароль"}, status=401)
    token = AuthToken.create_for_user(user)
    return JsonResponse({"token": token, "username": user.username})


@require_GET
def api_me(request):
    """GET з заголовком Authorization: Bearer <token> -> { "username": "..." } або 401."""
    user = get_user_from_request(request)
    if not user or not user.is_authenticated:
        return JsonResponse({"error": "Не авторизовано"}, status=401)
    return JsonResponse({"username": user.username, "is_staff": user.is_staff})


@csrf_exempt
@require_http_methods(["POST"])
@require_staff
def api_logout(request):
    """Видалити токен поточного користувача (Bearer в заголовку)."""
    user = request.api_user
    AuthToken.objects.filter(user=user).delete()
    return JsonResponse({"success": True})


# --- Settings ---

@require_GET
def api_settings_get(request):
    """Публічний GET налаштувань сайту."""
    s = SiteSettings.get_settings()
    return JsonResponse({
        "store_name": s.store_name,
        "phone": s.phone,
        "hero_title": s.hero_title,
        "hero_subtitle": s.hero_subtitle,
    })


@csrf_exempt
@require_http_methods(["PATCH", "PUT"])
@require_staff
def api_settings_patch(request):
    """Оновлення налаштувань (часткове)."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Невалідний JSON"}, status=400)
    s = SiteSettings.get_settings()
    for key in ("store_name", "phone", "hero_title", "hero_subtitle"):
        if key in data and data[key] is not None:
            setattr(s, key, str(data[key])[: getattr(SiteSettings._meta.get_field(key), "max_length", 500)])
    s.save()
    return JsonResponse({
        "store_name": s.store_name,
        "phone": s.phone,
        "hero_title": s.hero_title,
        "hero_subtitle": s.hero_subtitle,
    })


# --- Products CRUD (admin) ---

def _product_to_api_dict(p):
    """Dict з БД (snake_case) -> API (camelCase oldPrice)."""
    if isinstance(p, dict):
        return store_views._product_to_api_dict(p)
    return store_views._product_to_api_dict({
        "id": p.id, "name": p.name, "category": p.category, "subcategory": p.subcategory,
        "sub_subcategory": getattr(p, "sub_subcategory", "") or "",
        "price": p.price, "old_price": p.old_price, "image": p.image or "🚿", "badge": p.badge,
        "description": p.description or "", "in_stock": p.in_stock, "quantity": p.quantity,
        "sort_order": getattr(p, "sort_order", 0), "rating": float(p.rating or 0), "rating_count": p.rating_count or 0,
    })


@csrf_exempt
@require_http_methods(["POST"])
@require_staff
def api_product_create(request):
    """POST JSON -> створення товару."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Невалідний JSON"}, status=400)
    name = (data.get("name") or "").strip()
    if not name:
        return JsonResponse({"error": "Назва обов'язкова"}, status=400)
    product = Product(
        name=name,
        category=(data.get("category") or "").strip() or "other",
        subcategory=(data.get("subcategory") or "").strip() or "other",
        sub_subcategory=(data.get("sub_subcategory") or "").strip(),
        price=int(data.get("price") or 0),
        old_price=int(data["oldPrice"]) if data.get("oldPrice") is not None else None,
        image=(data.get("image") or "🚿")[:500],
        badge=(data.get("badge") or "").strip()[:50] or None,
        description=(data.get("description") or "")[:50000],
        in_stock=bool(data.get("in_stock", True)),
        quantity=int(data.get("quantity") or 0),
        sort_order=int(data.get("sort_order") or 0),
    )
    product.save()
    return JsonResponse(_product_to_api_dict(product), status=201)


@csrf_exempt
@require_http_methods(["PATCH", "PUT"])
@require_staff
def api_product_update(request, pk):
    """PATCH /api/admin/products/<id>/ — оновлення товару."""
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Товар не знайдено"}, status=404)
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Невалідний JSON"}, status=400)
    if "name" in data and data["name"] is not None:
        product.name = str(data["name"])[:300]
    if "category" in data and data["category"] is not None:
        product.category = str(data["category"])[:80]
    if "subcategory" in data and data["subcategory"] is not None:
        product.subcategory = str(data["subcategory"])[:80]
    if "sub_subcategory" in data:
        product.sub_subcategory = (data["sub_subcategory"] or "")[:80]
    if "price" in data and data["price"] is not None:
        product.price = int(data["price"])
    if "oldPrice" in data:
        product.old_price = int(data["oldPrice"]) if data["oldPrice"] is not None else None
    if "image" in data and data["image"] is not None:
        product.image = str(data["image"])[:500] or "🚿"
    if "badge" in data:
        product.badge = (data["badge"] or "").strip()[:50] or None
    if "description" in data:
        product.description = (data["description"] or "")[:50000]
    if "in_stock" in data:
        product.in_stock = bool(data["in_stock"])
    if "quantity" in data and data["quantity"] is not None:
        product.quantity = int(data["quantity"])
    if "sort_order" in data and data["sort_order"] is not None:
        product.sort_order = int(data["sort_order"])
    product.save()
    return JsonResponse(_product_to_api_dict(product))


@csrf_exempt
@require_http_methods(["DELETE"])
@require_staff
def api_product_delete(request, pk):
    """DELETE /api/admin/products/<id>/."""
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Товар не знайдено"}, status=404)
    product.delete()
    return HttpResponse(status=204)
