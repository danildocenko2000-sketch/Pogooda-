#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Стабільний тренувальний API (не чіпай руками).

Ідея: `training.py` можна редагувати як "пісочницю", а цей модуль завжди лишається валідним,
щоб сервер не падав від експериментів.

Ендпоінти (підключені в urls.py):
- GET /api/training/        → JSON-масив TRAINING_PRODUCT (UTF-8, без \\uXXXX)
- GET /api/training/page/   → HTML-сторінка з виводом атрибутів (не падає при відсутніх ключах)
"""

import html as html_module

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET


TRAINING_PRODUCT = [
    {
        "id": 1,
        "name": "Змішувач Grohe Essence Chrome",
        "category": "faucets",
        "subcategory": "kitchen-faucet",
        "sub_subcategory": "chrome",
        "price": 4490,
        "oldPrice": 5620,
        "image": "🚿",
        "badge": "Хіт",
        "description": (
            "Змішувач Grohe Essence Chrome - найбільш популярний вибір для сучасної кухні. "
            "Хромована латунь, керамічний картридж. Гарантія 5 років."
        ),
        "in_stock": True,
        "quantity": 2,
        "rating": 4.0,
        "rating_count": 6,
    },
]


def _get(obj: dict, key: str):
    return obj.get(key, f"(missing: {key})")


def _esc(value) -> str:
    return html_module.escape(str(value))


@require_GET
def api_training(request):
    return JsonResponse(
        TRAINING_PRODUCT,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


@require_GET
def api_training_page(request):
    obj = TRAINING_PRODUCT[0]
    html_content = (
        "<!DOCTYPE html>\n"
        "<html><head><meta charset='utf-8'><title>Тренування JSON</title></head><body>\n"
        "<h1>Атрибути об'єкта товару (UTF-8)</h1>\n"
        "<ul>\n"
        f"<li><strong>id</strong>: {_esc(_get(obj, 'id'))}</li>\n"
        f"<li><strong>name</strong>: {_esc(_get(obj, 'name'))}</li>\n"
        f"<li><strong>category</strong>: {_esc(_get(obj, 'category'))}</li>\n"
        f"<li><strong>subcategory</strong>: {_esc(_get(obj, 'subcategory'))}</li>\n"
        f"<li><strong>sub_subcategory</strong>: {_esc(_get(obj, 'sub_subcategory'))}</li>\n"
        f"<li><strong>price</strong>: {_esc(_get(obj, 'price'))}</li>\n"
        f"<li><strong>oldPrice</strong>: {_esc(_get(obj, 'oldPrice'))}</li>\n"
        f"<li><strong>image</strong>: {_esc(_get(obj, 'image'))}</li>\n"
        f"<li><strong>badge</strong>: {_esc(_get(obj, 'badge'))}</li>\n"
        f"<li><strong>description</strong>: {_esc(_get(obj, 'description'))}</li>\n"
        f"<li><strong>in_stock</strong>: {_esc(_get(obj, 'in_stock'))}</li>\n"
        f"<li><strong>quantity</strong>: {_esc(_get(obj, 'quantity'))}</li>\n"
        f"<li><strong>rating</strong>: {_esc(_get(obj, 'rating'))}</li>\n"
        f"<li><strong>rating_count</strong>: {_esc(_get(obj, 'rating_count'))}</li>\n"
        "</ul>\n"
        "</body></html>"
    )
    return HttpResponse(html_content, content_type="text/html; charset=utf-8")

