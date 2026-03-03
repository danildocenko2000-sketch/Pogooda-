# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Review, SiteSettings, AuthToken


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "key_preview", "created_at")
    list_filter = ("created_at",)

    @admin.display(description="Ключ")
    def key_preview(self, obj):
        return (obj.key[:16] + "…") if obj.key and len(obj.key) > 16 else (obj.key or "—")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("store_name", "phone")
    fieldsets = (
        (None, {"fields": ("store_name", "phone")}),
        ("Головна сторінка", {"fields": ("hero_title", "hero_subtitle")}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "subcategory", "price", "image_preview", "rating", "in_stock", "quantity")
    list_filter = ("category", "in_stock")
    search_fields = ("name", "description")
    list_editable = ("price", "in_stock", "quantity")
    ordering = ("sort_order", "pk")
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("name", "category", "subcategory", "sub_subcategory", "price", "old_price", "image", "badge", "description")}),
        ("Склад та рейтинг", {"fields": ("in_stock", "quantity", "sort_order", "rating", "rating_count")}),
    )

    @admin.display(description="Фото")
    def image_preview(self, obj):
        if not obj.image:
            return "—"
        if obj.image.startswith("http") or obj.image.startswith("/"):
            return format_html('<img src="{}" alt="" style="max-height:36px; max-width:48px; object-fit:contain;" />', obj.image)
        return obj.image


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "author_name", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("author_name", "text")
    ordering = ("-created_at",)
