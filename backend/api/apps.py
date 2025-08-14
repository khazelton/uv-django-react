# Django API App Configuration
# This file configures the API app for Django
# 
# PROJECT OVERVIEW:
# - Defines the API app configuration and metadata
# - Registers the app with Django's app registry
# - Sets default database field type for models
# - Required for Django to recognize this as a valid app
#
# CONNECTIONS:
# - Imports: django.apps.AppConfig
# - Referenced by: config/settings.py (INSTALLED_APPS)
# - Part of: Django app system
# - Related to: api/__init__.py, api/models.py, api/views.py, api/urls.py
#
# APP CONFIGURATION:
# - Name: "api" (matches directory name)
# - Default auto field: BigAutoField (64-bit integer primary keys)
# - Purpose: Handle API endpoints for React frontend
#
# USAGE:
# - Django automatically loads this when the app is in INSTALLED_APPS
# - No manual instantiation needed
# - Can be extended with custom app configuration if needed

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration class for the API app.
    
    This class defines how Django should handle the API app,
    including database field types and app metadata.
    """
    # Use 64-bit integer primary keys for models
    default_auto_field = "django.db.models.BigAutoField"
    
    # App name - must match the directory name
    name = "api"
