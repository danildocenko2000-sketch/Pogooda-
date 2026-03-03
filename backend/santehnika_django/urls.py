from django.contrib import admin
from django.urls import path
from store import views, api, api_admin, training_api, weather_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("api/weather/forecast/", weather_api.api_weather_forecast, name="api_weather_forecast"),
    path("api/weather/search/", weather_api.api_weather_search, name="api_weather_search"),
    path("api/weather/reverse/", weather_api.api_weather_reverse, name="api_weather_reverse"),
    path("api/products/", api.api_products, name="api_products"),
    path("api/products/<int:pk>/", api.api_product_detail, name="api_product_detail"),
    path("api/settings/", api_admin.api_settings_get, name="api_settings_get"),
    path("api/auth/login/", api_admin.api_login, name="api_auth_login"),
    path("api/auth/me/", api_admin.api_me, name="api_auth_me"),
    path("api/auth/logout/", api_admin.api_logout, name="api_auth_logout"),
    path("api/admin/settings/", api_admin.api_settings_patch, name="api_admin_settings"),
    path("api/admin/products/", api_admin.api_product_create, name="api_admin_product_create"),
    path("api/admin/products/<int:pk>/", api_admin.api_product_update, name="api_admin_product_update"),
    path("api/admin/products/<int:pk>/delete/", api_admin.api_product_delete, name="api_admin_product_delete"),
    path("api/training/", training_api.api_training, name="api_training"),
    path("api/training/page/", training_api.api_training_page, name="api_training_page"),
    path("store/reviews/", views.get_reviews, name="get_reviews"),
    path("store/review/", views.add_review, name="add_review"),
    path("store/chat/status/", views.chat_status, name="chat_status"),
    path("store/chat/", views.chat_api, name="chat_api"),
]
