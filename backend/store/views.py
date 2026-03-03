# -*- coding: utf-8 -*-
import json
import random
import re
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .data import PRODUCTS, SUBCATEGORY_LABELS, SUB_SUBCATEGORY_LABELS
from .models import Product, Review, SiteSettings

# Назви категорій для хедера (порядок і лейбли)
CATEGORY_MENU = [
    {"id": "kitchen", "name": "🍽️ Кухня"},
    {"id": "bathroom", "name": "🚿 Ванна"},
    {"id": "toilet", "name": "🚽 Туалет"},
    {"id": "pool", "name": "🏊 Басейн"},
    {"id": "heating", "name": "🔥 Опалення"},
    {"id": "faucets", "name": "🚿 Змішувачі"},
    {"id": "accessories", "name": "⚙️ Аксесуари"},
    {"id": "bath", "name": "🛁 Ванни"},
    {"id": "water-heaters", "name": "💧 Бойлери"},
    {"id": "pipes", "name": "🔧 Труби та каналізація"},
]


def _build_catalog_tree(products):
    """Побудова дерева категорія → підкатегорії → під-підкатегорії зі списку товарів."""
    from collections import defaultdict
    tree = defaultdict(lambda: defaultdict(set))
    for p in products:
        cat = p.get("category") or ""
        sub = p.get("subcategory") or ""
        subsub = (p.get("sub_subcategory") or "").strip()
        if not cat or not sub:
            continue
        if subsub:
            tree[cat][sub].add(subsub)
        else:
            tree[cat][sub].add(None)  # позначити, що підкатегорія існує
    out = {}
    for cat in [c["id"] for c in CATEGORY_MENU]:
        if cat not in tree:
            out[cat] = []
            continue
        subs_list = []
        for sub_id in sorted(tree[cat].keys()):
            subsub_set = tree[cat][sub_id]
            subsub_list = sorted(x for x in subsub_set if x)
            subs_list.append({
                "id": sub_id,
                "name": SUBCATEGORY_LABELS.get(sub_id, sub_id),
                "children": [{"id": ss, "name": SUB_SUBCATEGORY_LABELS.get(ss, ss)} for ss in subsub_list],
            })
        out[cat] = subs_list
    return out


def _normalize_products(products_list):
    """Додає in_stock, quantity, rating до кожного товару, якщо їх немає."""
    result = []
    for p in products_list:
        d = dict(p)
        d.setdefault("in_stock", True)
        if "quantity" not in d:
            d["quantity"] = (d["id"] % 25) + 1
        d.setdefault("rating", 4.0)
        d.setdefault("rating_count", (d["id"] % 15) + 5)
        d.setdefault("sub_subcategory", "")
        result.append(d)
    return result


def _product_to_api_dict(p):
    """Один товар (dict з values() або з БД) → формат API для Vue (camelCase oldPrice)."""
    return {
        "id": p["id"],
        "name": p["name"],
        "category": p["category"],
        "subcategory": p["subcategory"],
        "sub_subcategory": (p.get("sub_subcategory") or "").strip(),
        "price": p["price"],
        "oldPrice": p["old_price"],
        "image": p.get("image") or "🚿",
        "badge": p.get("badge"),
        "description": p.get("description") or "",
        "in_stock": p.get("in_stock", True),
        "quantity": p.get("quantity", 0),
        "sort_order": p.get("sort_order", 0),
        "rating": float(p.get("rating") or 0),
        "rating_count": p.get("rating_count") or 0,
    }


def _products_from_db():
    """Повертає список товарів у форматі для API/шаблону з моделі Product або None."""
    prods = list(Product.objects.all().values(
        "id", "name", "category", "subcategory", "sub_subcategory", "price", "old_price",
        "image", "badge", "description", "in_stock", "quantity", "rating", "rating_count"
    ))
    if not prods:
        return None
    return [_product_to_api_dict(p) for p in prods]


def index(request):
    """Головна сторінка сайту. Дані з БД (якщо є товари) або з data.py."""
    settings = SiteSettings.get_settings()
    phone = settings.phone
    phone_tel = "".join(c for c in phone if c.isdigit() or c == "+")

    # Кілька номерів для блоку контактів (раскривається як каталог)
    phone_numbers = [
        {"number": "+38 (050) 123-45-67", "tel": "380501234567", "label": "Основний"},
        {"number": "+38 (067) 111-22-33", "tel": "380671112233", "label": "Менеджер"},
        {"number": "+38 (063) 444-55-66", "tel": "380634445566", "label": "Підтримка"},
    ]
    if not any(p["number"] == phone for p in phone_numbers):
        phone_numbers.insert(0, {"number": phone, "tel": phone_tel, "label": "Основний"})

    products_raw = _products_from_db()
    if products_raw is None:
        products = _normalize_products(PRODUCTS)
    else:
        products = products_raw

    # Дерево каталогу для випадаючого меню: категорія → підкатегорії → під-підкатегорії
    catalog_tree = _build_catalog_tree(products)
    category_menu_with_children = [
        {"id": c["id"], "name": c["name"], "subcategories": catalog_tree.get(c["id"], [])}
        for c in CATEGORY_MENU
    ]

    # Посилання на месенджери (можна винести в SiteSettings)
    messenger_links = [
        {"name": "Telegram", "url": "https://t.me/santehnika_support", "icon": "telegram"},
        {"name": "Viber", "url": "viber://chat?number=380501234567", "icon": "viber"},
        {"name": "WhatsApp", "url": "https://wa.me/380501234567", "icon": "whatsapp"},
    ]

    context = {
        "store_name": settings.store_name,
        "hero_title": settings.hero_title,
        "hero_subtitle": settings.hero_subtitle,
        "phone_number": phone,
        "phone_tel": phone_tel,
        "phone_numbers": phone_numbers,
        "messenger_links": messenger_links,
        "products": products,
        "subcategory_labels": SUBCATEGORY_LABELS,
        "sub_subcategory_labels": SUB_SUBCATEGORY_LABELS,
        "products_json": json.dumps(products, ensure_ascii=False),
        "subcategory_labels_json": json.dumps(SUBCATEGORY_LABELS, ensure_ascii=False),
        "sub_subcategory_labels_json": json.dumps(SUB_SUBCATEGORY_LABELS, ensure_ascii=False),
        "catalog_tree": catalog_tree,
        "category_menu": CATEGORY_MENU,
        "category_menu_with_children": category_menu_with_children,
    }
    return render(request, "store/index.html", context)


@require_GET
def get_reviews(request):
    """Список відгуків для товару (product_id в query)."""
    product_id = request.GET.get("product_id")
    if not product_id:
        return JsonResponse({"reviews": []})
    try:
        product = Product.objects.get(pk=int(product_id))
    except (ValueError, Product.DoesNotExist):
        return JsonResponse({"reviews": []})
    reviews = [
        {
            "id": r.id,
            "author_name": r.author_name,
            "rating": r.rating,
            "text": r.text,
            "created_at": r.created_at.strftime("%d.%m.%Y"),
        }
        for r in product.reviews.all()[:50]
    ]
    return JsonResponse({"reviews": reviews, "rating": product.rating, "rating_count": product.rating_count})


@require_POST
@ensure_csrf_cookie
def add_review(request):
    """Додати відгук. POST: product_id, author_name, rating (1-5), text."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        data = request.POST.dict()
    product_id = data.get("product_id")
    author_name = (data.get("author_name") or "").strip()
    try:
        rating = int(data.get("rating") or 0)
    except (TypeError, ValueError):
        rating = 0
    text = (data.get("text") or "").strip()

    if not product_id or not author_name or not (1 <= rating <= 5) or not text:
        return JsonResponse({"success": False, "error": "Заповніть усі поля. Оцінка 1–5."}, status=400)

    product = get_object_or_404(Product, pk=int(product_id))
    review = Review.objects.create(product=product, author_name=author_name, rating=rating, text=text)
    product.update_rating()

    return JsonResponse({
        "success": True,
        "rating": product.rating,
        "rating_count": product.rating_count,
        "review": {
            "id": review.id,
            "author_name": review.author_name,
            "rating": review.rating,
            "text": review.text,
            "created_at": review.created_at.strftime("%d.%m.%Y"),
        },
    })


# Повідомлення для fallback-бота (коли Gemini не налаштований)
_CHAT_FALLBACK = {
    "greeting": ["Привіт! 👋 Як я можу вам допомогти?", "Добрий день! Що вас цікавить?", "Добро пожлувати! 😊"],
    "product": ["Ви можете пошукати товари в каталозі. Які категорії вас цікавлять? 🛒", "У нас є більше 250 товарів! Пошукайте в розділах: Кухня, Ванна, Опалення та інші."],
    "support": ["+38 (050) 123-45-67 — наш номер підтримки 📞", "Ми доступні 24/7! Телефон: +38 (050) 123-45-67"],
    "delivery": ["Безплатна доставка від 10 000 грн! 🚚", "Доставляємо по всій Україні. Час доставки 1–3 дні."],
    "warranty": ["Ми надаємо гарантію 5 років на всю продукцію! ✅", "Вся продукція має гарантію якості 5 років."],
    "price": ["У нас регулярно проходять акції. -20% на все! 💰", "Розстрочка 0% доступна на 12 місяців."],
    "default": ["Не зрозумів 🤔 Спробуйте: товари, підтримка, доставка, гарантія, ціна", "Спитайте про: товари, контакти, доставку або гарантію"],
}


def _fallback_bot_reply(message):
    """Відповідь простого бота за ключовими словами."""
    msg = (message or "").lower().strip()
    if not msg:
        return random.choice(_CHAT_FALLBACK["greeting"])
    if re.search(r"привіт|привет|hi|hello|добрий|день", msg):
        return random.choice(_CHAT_FALLBACK["greeting"])
    if re.search(r"товар|каталог|пошук|купити", msg):
        return random.choice(_CHAT_FALLBACK["product"])
    if re.search(r"підтримка|поддержка|номер|телефон|контакт", msg):
        return random.choice(_CHAT_FALLBACK["support"])
    if re.search(r"доставка|доставить|відправ", msg):
        return random.choice(_CHAT_FALLBACK["delivery"])
    if re.search(r"гарантія|гарантия", msg):
        return random.choice(_CHAT_FALLBACK["warranty"])
    if re.search(r"ціна|цена|знижка|скидка|акція", msg):
        return random.choice(_CHAT_FALLBACK["price"])
    return random.choice(_CHAT_FALLBACK["default"])


def _gemini_reply(user_message):
    """Відповідь через Google Gemini API. Повертає текст або None при помилці."""
    api_key = getattr(settings, "GEMINI_API_KEY", None) or ""
    if not api_key or not user_message or not user_message.strip():
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        system_instruction = (
            "Ти — дружній консультант інтернет-магазину сантехніки «WORLD OF Santehnika» (Україна). "
            "Відповідай коротко українською. Інформація: безплатна доставка від 10 000 грн, гарантія 5 років, "
            "розстрочка 0% до 12 місяців, контакт +38 (050) 123-45-67. Категорії: кухня, ванна, туалет, опалення, "
            "змішувачі, ванни, бойлери, труби. Якщо питають про товар — порадь переглянути каталог на сайті."
        )
        prompt = system_instruction + "\n\nПовідомлення клієнта: " + user_message.strip()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=512,
                temperature=0.7,
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ],
        )
        if response and response.text:
            return response.text.strip()
    except Exception:
        pass
    return None


@require_GET
def chat_status(request):
    """Чи увімкнено AI-чат (Gemini)."""
    return JsonResponse({
        "ai_enabled": bool(getattr(settings, "GEMINI_API_KEY", None)),
    })


@require_POST
@ensure_csrf_cookie
def chat_api(request):
    """Відповідь чат-бота: AI (Gemini) або fallback за ключовими словами."""
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        data = request.POST.dict()
    message = (data.get("message") or "").strip()
    if not message:
        return JsonResponse({"reply": _fallback_bot_reply(""), "ai": False}, status=400)

    reply = _gemini_reply(message)
    if reply:
        return JsonResponse({"reply": reply, "ai": True})
    return JsonResponse({"reply": _fallback_bot_reply(message), "ai": False})
