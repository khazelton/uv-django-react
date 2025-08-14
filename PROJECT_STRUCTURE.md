# Project Structure and File Connections

## Overview
This document provides a comprehensive overview of the project structure, file relationships, and connections between different components of the UV Django React full-stack application.

## Project Architecture
```
uv-django-react/
├── backend/                 # Django backend application
│   ├── api/                # Custom API app
│   ├── config/             # Django project configuration
│   ├── manage.py           # Django management script
│   ├── pyproject.toml      # Python dependencies
│   └── .venv/              # Python virtual environment
├── frontend/               # React frontend application
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
├── .gitignore              # Git ignore patterns
└── README.md               # Project documentation
```

## Backend File Connections

### Core Django Files
- **manage.py**
  - **Imports**: os, sys, django.core.management
  - **References**: config.settings (Django settings module)
  - **Used by**: All Django management commands
  - **Purpose**: Django's main entry point for administrative tasks

- **pyproject.toml**
  - **Dependencies**: django, djangorestframework, django-cors-headers
  - **Referenced by**: uv.lock (dependency lock file)
  - **Used by**: uv install/uv run commands
  - **Purpose**: Python project dependencies and configuration

- **main.py**
  - **Imports**: None (standalone script)
  - **Referenced by**: pyproject.toml (project entry point)
  - **Related to**: manage.py (Django's main entry point)
  - **Purpose**: Simple test script for project verification

### Django Configuration (config/)
- **config/settings.py**
  - **Imports**: pathlib.Path
  - **Referenced by**: manage.py, wsgi.py, asgi.py
  - **References**: api app, rest_framework, corsheaders
  - **Database**: db.sqlite3 in backend directory
  - **Frontend**: localhost:5173 (Vite dev server)

- **config/urls.py**
  - **Imports**: django.contrib.admin, django.urls (path, include)
  - **References**: api.urls (custom API endpoints)
  - **Referenced by**: wsgi.py, asgi.py (Django entry points)
  - **Frontend**: React app calls /api/* endpoints

- **config/wsgi.py**
  - **Imports**: os, django.core.wsgi
  - **References**: config.settings (Django settings module)
  - **Referenced by**: Production web servers (Gunicorn, uWSGI, etc.)
  - **Related to**: asgi.py (ASGI configuration for async support)

- **config/asgi.py**
  - **Imports**: os, django.core.asgi
  - **References**: config.settings (Django settings module)
  - **Referenced by**: Async web servers (Daphne, Uvicorn, Hypercorn)
  - **Related to**: wsgi.py (WSGI configuration for sync deployment)

- **config/__init__.py**
  - **Purpose**: Makes config/ a Python package
  - **Referenced by**: manage.py, wsgi.py, asgi.py
  - **Part of**: Django project configuration structure

### API App (api/)
- **api/views.py**
  - **Imports**: django.http.JsonResponse
  - **Referenced by**: api/urls.py (URL routing)
  - **Called by**: Frontend React app via HTTP requests
  - **Related to**: config/urls.py (main URL configuration)

- **api/urls.py**
  - **Imports**: django.urls.path, .views.ping
  - **Referenced by**: config/urls.py (main URL configuration)
  - **Routes to**: api/views.py (view functions)
  - **Frontend calls**: React app makes requests to these endpoints

- **api/apps.py**
  - **Imports**: django.apps.AppConfig
  - **Referenced by**: config/settings.py (INSTALLED_APPS)
  - **Part of**: Django app system
  - **Related to**: api/__init__.py, api/models.py, api/views.py, api/urls.py

- **api/models.py**
  - **Imports**: django.db.models
  - **Referenced by**: Django ORM system
  - **Related to**: api/migrations/ (database schema changes)
  - **Part of**: Django app structure

- **api/admin.py**
  - **Imports**: django.contrib.admin
  - **Referenced by**: Django admin system
  - **Related to**: api/models.py (models to register)
  - **Part of**: Django admin interface at /admin/

- **api/tests.py**
  - **Imports**: django.test.TestCase
  - **Referenced by**: Django test runner
  - **Related to**: api/views.py (views to test), api/models.py (models to test)
  - **Part of**: Django testing framework

- **api/__init__.py**
  - **Purpose**: Makes api/ a Python package
  - **Referenced by**: config/settings.py (INSTALLED_APPS)
  - **Part of**: Django app system

- **api/migrations/__init__.py**
  - **Purpose**: Makes migrations/ a Python package
  - **Part of**: Django migration system
  - **Related to**: api/models.py (models that generate migrations)

## Frontend File Connections

### Core Configuration Files
- **package.json**
  - **Dependencies**: react, react-dom, axios
  - **Dev Dependencies**: TypeScript, Vite, ESLint
  - **Scripts**: dev, build, lint, preview
  - **Related to**: package-lock.json, node_modules/

- **vite.config.ts**
  - **Imports**: defineConfig, @vitejs/plugin-react
  - **Configuration**: React plugin, server settings, API proxy
  - **Proxy**: /api/* -> http://127.0.0.1:8000
  - **Used by**: Vite build tool and development server

- **tsconfig.json**
  - **References**: tsconfig.app.json, tsconfig.node.json
  - **Used by**: TypeScript compiler and Vite build process
  - **Purpose**: TypeScript project structure and references

- **tsconfig.app.json**
  - **Target**: ES2022 with React JSX support
  - **Includes**: src/ directory
  - **Used by**: Vite build process and TypeScript compiler

- **tsconfig.node.json**
  - **Target**: ES2022 for Node.js features
  - **Includes**: vite.config.ts
  - **Used by**: TypeScript compiler for build tool files

### React Source Files (src/)
- **main.tsx**
  - **Imports**: React, ReactDOM, index.css, App.tsx
  - **Renders to**: HTML element with id "root"
  - **Entry point**: Called when the page loads
  - **Related to**: index.html (root element), App.tsx (main component)

- **App.tsx**
  - **Imports**: React hooks, config.ts (API configuration), App.css
  - **API Call**: Fetches from Django backend at /api/ping/
  - **State**: Manages message state for API response
  - **Styling**: Uses App.css for component styling

- **config.ts**
  - **Exports**: API_BASE_URL, apiUrl function
  - **Environment**: VITE_API_BASE_URL for production configuration
  - **Development**: Uses Vite proxy at /api
  - **Used by**: App.tsx for API calls

- **index.css**
  - **Imported by**: main.tsx (global styles)
  - **Applied to**: Entire application
  - **Theme**: Supports system preference for light/dark mode
  - **Layout**: Uses flexbox for centering content

- **App.css**
  - **Imported by**: App.tsx (main component)
  - **Styles**: #root container, logo elements, cards
  - **Animations**: Logo spin animation with accessibility support
  - **Layout**: Centered container with max-width and padding

- **vite-env.d.ts**
  - **Purpose**: TypeScript declarations for Vite
  - **Enables**: import.meta.env, Vite-specific globals
  - **Used by**: config.ts (import.meta.env.VITE_API_BASE_URL)
  - **Part of**: Vite TypeScript integration

### HTML and Configuration
- **index.html**
  - **Root Element**: <div id="root"> where React renders
  - **Entry Point**: /src/main.tsx (React application bootstrap)
  - **Styling**: CSS loaded through React components
  - **Build Tool**: Vite processes and serves this file

- **eslint.config.js**
  - **Configuration**: ESLint for React + TypeScript
  - **Integrates**: TypeScript, React, React Hooks, Vite
  - **Targets**: All .ts and .tsx files
  - **Used by**: npm run lint command

- **.gitignore**
  - **Targets**: Frontend-specific files and directories
  - **Excludes**: build outputs, dependencies, development files
  - **Related to**: package.json, build outputs
  - **Part of**: Project-wide version control strategy

## Cross-Component Connections

### API Communication
- **Frontend → Backend**: React components call Django API endpoints
- **Proxy Configuration**: Vite proxies /api/* to Django backend
- **CORS**: Django allows requests from React dev server
- **Environment**: Configurable API base URLs for different environments

### Development Workflow
- **Backend Server**: Django development server on port 8000
- **Frontend Server**: Vite dev server on port 5173
- **Hot Reload**: Both frontend and backend support live reloading
- **Database**: SQLite database with Django ORM

### Build and Deployment
- **Backend Build**: uv for Python dependency management
- **Frontend Build**: Vite for optimized production builds
- **TypeScript**: Compilation and type checking for both environments
- **Linting**: ESLint for code quality and consistency

## File Dependencies Summary

### Backend Dependencies
- Django core framework
- Django REST Framework for API
- django-cors-headers for CORS support
- SQLite database (development)

### Frontend Dependencies
- React 19 with TypeScript
- Vite build tool and dev server
- ESLint for code quality
- CSS for styling and theming

### Development Tools
- uv for Python package management
- npm for Node.js package management
- Git for version control
- TypeScript for type safety

## Usage Patterns

### Development Commands
```bash
# Backend
cd backend && uv run python manage.py runserver

# Frontend
cd frontend && npm run dev

# Linting
cd frontend && npm run lint

# Building
cd frontend && npm run build
```

### File Modification Workflow
1. **Backend Changes**: Modify Django models, views, or URLs
2. **Frontend Changes**: Update React components or styles
3. **API Integration**: Ensure frontend calls correct backend endpoints
4. **Testing**: Verify changes work in both environments

This structure provides a clean separation of concerns while maintaining clear connections between frontend and backend components.
