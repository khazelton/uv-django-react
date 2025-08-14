"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

PROJECT OVERVIEW:
- Main URL configuration for Django backend
- Routes API requests to custom api app
- Provides Django admin interface
- Serves as entry point for all HTTP requests

CONNECTIONS:
- Imports: django.contrib.admin, django.urls (path, include)
- References: api.urls (custom API endpoints)
- Referenced by: wsgi.py, asgi.py (Django entry points)
- Frontend: React app calls /api/* endpoints

URL STRUCTURE:
- /api/* -> api.urls (custom API endpoints)
- /admin/ -> Django admin interface
- / -> No root route defined (API-only backend)

API ENDPOINTS (via api.urls):
- /api/ping/ -> ping view (GET request)
- Future endpoints can be added to api/urls.py
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # API routes - all /api/* requests go to the api app
    path('api/', include('api.urls')),

    # Django admin interface
    path("admin/", admin.site.urls),
]
