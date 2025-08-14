#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This file is Django's main entry point for running management commands like:
- runserver: Start the development server
- migrate: Apply database migrations
- createsuperuser: Create admin user
- collectstatic: Collect static files
- shell: Open Django shell

CONNECTIONS:
- Imports: os, sys, django.core.management
- References: config.settings (Django settings module)
- Used by: All Django management commands

USAGE:
- cd backend && python manage.py <command>
- cd backend && uv run python manage.py <command> (with uv)
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
