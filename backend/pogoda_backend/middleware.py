# -*- coding: utf-8 -*-
"""CORS: дозволити запити з Vue (інший порт)."""


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "OPTIONS":
            from django.http import HttpResponse
            r = HttpResponse()
            r["Access-Control-Allow-Origin"] = "*"
            r["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            r["Access-Control-Allow-Headers"] = "Content-Type"
            return r
        response = self.get_response(request)
        if request.path.startswith("/api/"):
            response["Access-Control-Allow-Origin"] = "*"
        return response
