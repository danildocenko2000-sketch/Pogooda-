#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Тренувальний модуль для роботи з JSON-об'єктом.

Ендпоінти:
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
        "<p>Можеш міняти ключі/значення в <code>TRAINING_PRODUCT[0]</code> — сторінка не впаде.</p>\n"
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Тренувальний модуль для роботи з JSON-об'єктом.

Ендпоінти:
- GET /api/training/        → JSON-масив TRAINING_PRODUCT (UTF-8, без \\uXXXX)
- GET /api/training/page/   → HTML-сторінка з виводом атрибутів (без падінь при відсутніх ключах)
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
    """Безпечно читає ключ: якщо нема — повертає (missing: key)."""
    return obj.get(key, f"(missing: {key})")


def _esc(value) -> str:
    """Екранує значення для HTML (в UTF-8)."""
    return html_module.escape(str(value))


@require_GET
def api_training(request):
    """Повертає TRAINING_PRODUCT як JSON у UTF-8 (без escape \\uXXXX)."""
    return JsonResponse(
        TRAINING_PRODUCT,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


@require_GET
def api_training_page(request):
    """HTML-сторінка: виводить атрибути об'єкта (не падає, якщо ключа нема)."""
    obj = TRAINING_PRODUCT[0]

    html_content = (
        "<!DOCTYPE html>\n"
        "<html><head><meta charset='utf-8'><title>Тренування JSON</title></head><body>\n"
        "<h1>Атрибути об'єкта товару (UTF-8)</h1>\n"
        "<p>Можеш міняти ключі/значення в <code>TRAINING_PRODUCT[0]</code> — сторінка не впаде.</p>\n"
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Окремий модуль для тренування:
  - GET /api/training/        → JSON-масив TRAINING_PRODUCT
  - GET /api/training/page/   → HTML зі списком атрибутів
"""

import html as html_module

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET


TRAINING_PRODUCT = [
    {
        "id": 1821,
        "name": "Змішувач Grohe Essence Chrome",
        "category": "faucets",
        "subcategory": "kitchen-faucet",
        "sub_subcategory": "chrome",
        "price": 1000,
        "oldPrice": 3000,
        "image": "333",
        "badge": "Хіт",
        "description": (
            "Змішувач Grohe Essence Chrome - найбільш популярний вибір для сучасної кухні. "
            "Хромована латунь, керамічний картридж. Гарантія 5 років."
        ),
        "in_stock": True,
        "quantity": 1,
        "rating": 1.0,
        "rating_count": 1,
    },
]
sisi_Ani = [
    {
        "id": 2,
        "kiska": "Змішувач Grohe Essence Chrome",
        "klitor": "faucets",
        "1": "kitchen-faucet",
        "2": "chrome",
        "3": 1000,
        "4": 3000,
        "5": "333",
        "6": "Хіт",
        "description": (
            "Змішувач Grohe Essence Chrome - найбільш популярний вибір для сучасної кухні. "
            "Хромована латунь, керамічний картридж. Гарантія 5 років."
        ),
        "in_stock": True,
        "quantity": 1,
        "rating": 1.0,
        "rating_count": 1,
    },
]

      

@require_GET
def api_training(request):
    """Повертає TRAINING_PRODUCT як JSON (UTF-8, без escape \\uXXXX)."""
    return JsonResponse(
        TRAINING_PRODUCT,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
    )


@require_GET
def api_training_page(request):
    """Проста HTML-сторінка, яка показує атрибути першого елемента TRAINING_PRODUCT."""
    obj = TRAINING_PRODUCT[0]
    obj2 = sisi_Ani[0]
    html_content = (
        "<!DOCTYPE html>\n"
        "<html><head><meta charset='utf-8'><title>Тренування JSON</title></head><body>\n"
        "<h1>Атрибути об'єкта товару (UTF-8)</h1>\n"
        "<ul>\n"
        f"<li><strong>id</strong>: {obj['id']}</li>\n"
        f"<li><strong>kiska</strong>: {html_module.escape(obj['kiska'])}</li>\n"obj2
        f"<li><strong>kiska</strong>: {html_module.escape(obj2['kiska'])}</li>\n"
        f"<li><strong>klitor</strong>: {html_module.escape(obj2['klitor'])}</li>\n"
        f"<li><strong>klitor</strong>: {html_module.escape(obj['klitor'])}</li>\n"
        f"<li><strong>1</strong>: {html_module.escape(obj2['1'])}</li>\n"
        f"<li><strong>1</strong>: {html_module.escape(obj['1'])}</li>\n"
        f"<li><strong>2</strong>: {html_module.escape(obj2['2'])}</li>\n"
        f"<li><strong>2</strong>: {html_module.escape(obj['2'])}</li>\n"
        f"<li><strong>3</strong>: {html_module.escape(obj2['3'])}</li>\n"
        f"<li><strong>3</strong>: {obj['3']}</li>\n"
        f"<li><strong>3</strong>: {obj2['3']}</li>\n"
        f"<li><strong>4</strong>: {obj['4']}</li>\n"
        f"<li><strong>4</strong>: {obj2['4']}</li>\n"
        f"<li><strong>5</strong>: {html_module.escape(obj['5'])}</li>\n"
        f"<li><strong>5</strong>: {html_module.escape(obj2['5'])}</li>\n"
        f"<li><strong>6</strong>: {html_module.escape(obj['6'])}</li>\n"
        f"<li><strong>6</strong>: {html_module.escape(obj2['6'])}</li>\n"
        f"<li><strong>description</strong>: {html_module.escape(obj['description'])}</li>\n"
        f"<li><strong>in_stock</strong>: {obj['in_stock']}</li>\n"
        f"<li><strong>quantity</strong>: {obj['quantity']}</li>\n"
        f"<li><strong>rating</strong>: {obj['rating']}</li>\n"
        f"<li><strong>rating_count</strong>: {obj['rating_count']}</li>\n"
        "</ul>\n"
        "</body></html>"
    )
    return HttpResponse(html_content, content_type="text/html; charset=utf-8")

