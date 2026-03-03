# -*- coding: utf-8 -*-
from django.urls import path
from weather import views as weather_views

urlpatterns = [
    path("api/weather/forecast/", weather_views.api_weather_forecast, name="api_weather_forecast"),
    path("api/weather/search/", weather_views.api_weather_search, name="api_weather_search"),
    path("api/weather/reverse/", weather_views.api_weather_reverse, name="api_weather_reverse"),
]
