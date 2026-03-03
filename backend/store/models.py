# -*- coding: utf-8 -*-
"""
Моделі для сайту WORLD OF Santehnika.
Структура готова для подальшої інтеграції з Django (API, фільтри, замовлення).
"""
import secrets
from django.db import models
from django.conf import settings


class SiteSettings(models.Model):
    """Один запис: назва магазину, телефон, hero-текст (для головної)."""
    store_name = models.CharField("Назва магазину", max_length=200, default="WORLD OF Santehnika")
    phone = models.CharField("Телефон", max_length=50, default="+38 (050) 123-45-67")
    hero_title = models.CharField("Заголовок hero", max_length=300, default="Преміальна сантехніка для вашого дому")
    hero_subtitle = models.CharField("Підзаголовок hero", max_length=500, default="Італійський дизайн, німецька якість. Безплатна доставка при замовленні від 10 000 грн")

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def save(self, *args, **kwargs):
        # Зберігаємо лише один запис
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            "store_name": "WORLD OF Santehnika",
            "phone": "+38 (050) 123-45-67",
            "hero_title": "Преміальна сантехніка для вашого дому",
            "hero_subtitle": "Італійський дизайн, німецька якість. Безплатна доставка при замовленні від 10 000 грн",
        })
        return obj


class AuthToken(models.Model):
    """Токен для API адмінки (Vue). Один токен на користувача, перезаписується при логіні."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="store_api_token"
    )
    key = models.CharField("Ключ", max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField("Створено", auto_now=True)

    class Meta:
        verbose_name = "API токен"
        verbose_name_plural = "API токени"

    @classmethod
    def create_for_user(cls, user):
        key = secrets.token_urlsafe(40)
        token, _ = cls.objects.update_or_create(user=user, defaults={"key": key})
        return token.key


class Product(models.Model):
    """Товар каталогу."""
    name = models.CharField("Назва", max_length=300)
    category = models.CharField("Категорія (slug)", max_length=80, db_index=True)
    subcategory = models.CharField("Підкатегорія (slug)", max_length=80, db_index=True)
    sub_subcategory = models.CharField("Під-підкатегорія (slug)", max_length=80, blank=True, default="", db_index=True)
    price = models.PositiveIntegerField("Ціна (грн)")
    old_price = models.PositiveIntegerField("Стара ціна (грн)", null=True, blank=True)
    image = models.CharField("Зображення (emoji або URL)", max_length=500, default="🚿")
    badge = models.CharField("Бейдж (Хіт, Знижка тощо)", max_length=50, null=True, blank=True)
    description = models.TextField("Опис", blank=True)
    in_stock = models.BooleanField("В наявності", default=True)
    quantity = models.PositiveIntegerField("Кількість", default=0)
    sort_order = models.PositiveIntegerField("Порядок сортування", default=0, db_index=True)
    rating = models.FloatField("Рейтинг (середній)", default=0)
    rating_count = models.PositiveIntegerField("Кількість відгуків", default=0)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.name

    def update_rating(self):
        """Перерахувати рейтинг з відгуків."""
        from django.db.models import Avg, Count
        agg = self.reviews.aggregate(avg=Avg("rating"), count=Count("id"))
        self.rating = round(agg["avg"] or 0, 1)
        self.rating_count = agg["count"] or 0
        self.save(update_fields=["rating", "rating_count"])


class Review(models.Model):
    """Відгук на товар."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField("Ім'я", max_length=120)
    rating = models.PositiveSmallIntegerField("Оцінка (1-5)", choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField("Текст відгуку")
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["-created_at"]
