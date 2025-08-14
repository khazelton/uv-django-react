# UV Entry Point Script
# This file serves as a simple entry point for the uv project
# 
# PURPOSE:
# - Simple test script to verify the project is working
# - Can be used as an alternative entry point for testing
# - Demonstrates basic Python script structure
#
# CONNECTIONS:
# - Imports: None (standalone script)
# - Referenced by: pyproject.toml (project entry point)
# - Related to: manage.py (Django's main entry point)
#
# USAGE:
# - uv run python main.py: Run this script
# - uv run python -m main: Alternative execution method
#
# NOTE: This is not the main Django entry point - use manage.py for Django operations

def main():
    print("Hello from uv-django-react!")


if __name__ == "__main__":
    main()
