# -*- coding: utf-8 -*-
"""
Проксі API погоди: Vue → Django → Open-Meteo / Nominatim.
"""
import json
import urllib.error
import urllib.parse
import urllib.request

from django.http import JsonResponse
from django.views.decorators.http import require_GET

OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEO = "https://geocoding-api.open-meteo.com/v1/search"
NOMINATIM_REVERSE = "https://nominatim.openstreetmap.org/reverse"


def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PogodaWeatherApp/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


@require_GET
def api_weather_forecast(request):
    """GET ?latitude=&longitude= → проксі до Open-Meteo forecast."""
    lat = request.GET.get("latitude")
    lon = request.GET.get("longitude")
    if not lat or not lon:
        return JsonResponse({"error": "Потрібні latitude та longitude"}, status=400)
    try:
        params = urllib.parse.urlencode({
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto",
            "forecast_days": "7",
        })
        data = _fetch(f"{OPEN_METEO_FORECAST}?{params}")
        return JsonResponse(data)
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as e:
        return JsonResponse({"error": str(e)}, status=502)


@require_GET
def api_weather_search(request):
    """GET ?q=&only_ukraine=0|1 → проксі до Open-Meteo Geocoding."""
    q = (request.GET.get("q") or "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})
    only_ukraine = request.GET.get("only_ukraine", "").lower() in ("1", "true", "yes")
    try:
        params = {
            "name": q,
            "count": "10",
            "language": "uk" if only_ukraine else "ru",
            "format": "json",
        }
        if only_ukraine:
            params["countryCode"] = "UA"
        query = urllib.parse.urlencode(params)
        data = _fetch(f"{OPEN_METEO_GEO}?{query}")
        results = data.get("results") or []
        out = [
            {
                "name": c.get("name"),
                "admin1": c.get("admin1"),
                "country": c.get("country"),
                "lat": c.get("latitude"),
                "lon": c.get("longitude"),
                "displayName": f"{c.get('name', '')}{', ' + c['admin1'] if c.get('admin1') else ''}{', ' + c['country'] if c.get('country') else ''}",
            }
            for c in results
        ]
        return JsonResponse({"results": out})
    except (urllib.error.URLError, json.JSONDecodeError, OSError) as e:
        return JsonResponse({"error": str(e), "results": []}, status=502)


@require_GET
def api_weather_reverse(request):
    """GET ?lat=&lon= → проксі до Nominatim reverse."""
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    if not lat or not lon:
        return JsonResponse({"name": "Поточна локація"})
    try:
        params = urllib.parse.urlencode({
            "format": "json",
            "lat": lat,
            "lon": lon,
            "accept-language": "uk",
            "addressdetails": "1",
        })
        data = _fetch(f"{NOMINATIM_REVERSE}?{params}")
        a = data.get("address") or {}
        name = (
            a.get("city")
            or a.get("town")
            or a.get("village")
            or a.get("municipality")
            or a.get("hamlet")
            or a.get("county")
            or (f"{a.get('state', '')}, {a.get('country', '')}".strip(", ") if (a.get("state") and a.get("country")) else a.get("country"))
            or "Поточна локація"
        )
        return JsonResponse({"name": name})
    except (urllib.error.URLError, json.JSONDecodeError, OSError):
        return JsonResponse({"name": "Поточна локація"})
