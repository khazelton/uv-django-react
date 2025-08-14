# Django API App Migrations Package
# This empty __init__.py file makes the migrations directory a Python package
# 
# PURPOSE:
# - Marks migrations/ as a Python package
# - Allows Django to import migration files
# - Required for Django's migration system
#
# CONNECTIONS:
# - Part of: Django migration system
# - Related to: api/models.py (models that generate migrations)
# - Used by: python manage.py makemigrations and migrate
#
# NOTE: This file is intentionally empty - Django only needs it to exist
# Migration files will be created here when models are added or modified
