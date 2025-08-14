# Django API URL Configuration
# This file defines the URL patterns for the API app endpoints
# 
# PROJECT OVERVIEW:
# - Routes HTTP requests to specific API view functions
# - Part of the Django URL routing system
# - Included by the main config/urls.py under the /api/ prefix
# - Currently has one endpoint: ping
#
# CONNECTIONS:
# - Imports: django.urls.path, .views.ping
# - Referenced by: config/urls.py (main URL configuration)
# - Routes to: api/views.py (view functions)
# - Frontend calls: React app makes requests to these endpoints
#
# URL STRUCTURE:
# - Base path: /api/ (defined in config/urls.py)
# - Full endpoint: /api/ping/
# - View function: ping (from api/views.py)
# - Name: "ping" (for reverse URL lookup)
#
# API ENDPOINTS:
# - GET /api/ping/ -> ping view -> {"message": "pong"}
#
# USAGE:
# - Frontend: fetch('/api/ping/') or fetch('http://localhost:8000/api/ping/')
# - Backend: config/urls.py includes this file under /api/ prefix
# - Testing: curl http://localhost:8000/api/ping/

from django.urls import path
from .views import ping

urlpatterns = [
    # Health check endpoint - returns {"message": "pong"}
    path("ping/", ping, name="ping"),
]
