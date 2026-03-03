# -*- coding: utf-8 -*-
"""Завантажити товари з store.data.PRODUCTS у БД."""
from django.core.management.base import BaseCommand
from store.data import PRODUCTS
from store.models import Product


class Command(BaseCommand):
    help = "Завантажити товари з data.PRODUCTS у базу даних (для подальшого редагування в адмінці)"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Спочатку видалити всі товари з БД")

    def handle(self, *args, **options):
        if options["clear"]:
            n = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING("Видалено товарів: %s" % n))

        created = 0
        for i, p in enumerate(PRODUCTS):
            _, is_new = Product.objects.update_or_create(
                id=p["id"],
                defaults={
                    "name": p["name"],
                    "category": p["category"],
                    "subcategory": p["subcategory"],
                    "sub_subcategory": (p.get("sub_subcategory") or "").strip(),
                    "price": p["price"],
                    "old_price": p.get("oldPrice"),
                    "image": p.get("image") or "🚿",
                    "badge": p.get("badge"),
                    "description": p.get("description") or "",
                    "in_stock": p.get("in_stock", True),
                    "quantity": p.get("quantity", (p["id"] % 25) + 1),
                    "sort_order": i,
                    "rating": p.get("rating", 4.0),
                    "rating_count": p.get("rating_count", (p["id"] % 15) + 5),
                },
            )
            if is_new:
                created += 1

        self.stdout.write(self.style.SUCCESS("Оброблено товарів: %s, створено нових: %s" % (len(PRODUCTS), created)))
