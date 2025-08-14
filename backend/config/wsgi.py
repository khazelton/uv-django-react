"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/

PROJECT OVERVIEW:
- WSGI (Web Server Gateway Interface) configuration for Django
- Standard interface between web servers and Python web applications
- Used for production deployment with servers like Gunicorn, uWSGI
- Development server (runserver) also uses this configuration

CONNECTIONS:
- Imports: os, django.core.wsgi
- References: config.settings (Django settings module)
- Referenced by: Production web servers (Gunicorn, uWSGI, etc.)
- Related to: asgi.py (ASGI configuration for async support)

DEPLOYMENT:
- Production: Web server (nginx) -> WSGI server (Gunicorn) -> this file
- Development: python manage.py runserver -> this file
- Environment: DJANGO_SETTINGS_MODULE set to "config.settings"

USAGE:
- Production: gunicorn config.wsgi:application
- Development: python manage.py runserver (uses this automatically)
"""

import os

from django.core.wsgi import get_wsgi_application

# Set Django settings module for WSGI application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# WSGI application object - this is what web servers call
application = get_wsgi_application()
