"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/

PROJECT OVERVIEW:
- ASGI (Asynchronous Server Gateway Interface) configuration for Django
- Modern interface for async-capable web servers and applications
- Supports WebSocket, HTTP/2, and other async protocols
- Alternative to WSGI for modern deployment scenarios

CONNECTIONS:
- Imports: os, django.core.asgi
- References: config.settings (Django settings module)
- Referenced by: Async web servers (Daphne, Uvicorn, Hypercorn)
- Related to: wsgi.py (WSGI configuration for sync deployment)

DEPLOYMENT:
- Production: Web server (nginx) -> ASGI server (Daphne, Uvicorn) -> this file
- Development: python manage.py runserver -> this file (can use either)
- Environment: DJANGO_SETTINGS_MODULE set to "config.settings"

USAGE:
- Production: daphne config.asgi:application
- Production: uvicorn config.asgi:application
- Development: python manage.py runserver (uses this automatically)

NOTE: ASGI is the future of Python web deployment, but WSGI is still widely used
"""

import os

from django.core.asgi import get_asgi_application

# Set Django settings module for ASGI application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# ASGI application object - this is what async web servers call
application = get_asgi_application()
