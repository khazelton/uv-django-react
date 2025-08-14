# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Codebase Overview

This is a modern full-stack web application with Django REST Framework backend and React TypeScript frontend, using UV for Python package management and Vite for frontend development.

## Common Development Commands

### Backend (Django)

```bash
# Install dependencies
cd backend
uv sync --all-extras

# Run development server
uv run python manage.py runserver

# Database migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Run tests
uv run python manage.py test

# Django shell
uv run python manage.py shell
```

### Frontend (React)

```bash
# Install dependencies
cd frontend
npm install

# Development server (http://127.0.0.1:5173)
npm run dev

# Production build
npm run build

# Run linting
npm run lint

# Preview production build
npm run preview
```

### Running Full Stack

Start both servers in separate terminals:
1. Backend: `cd backend && uv run python manage.py runserver`
2. Frontend: `cd frontend && npm run dev`

The frontend proxies API requests to the backend automatically in development.

## Architecture & Structure

### Backend Architecture

- **Django Project**: `backend/config/` contains project settings
- **API App**: `backend/api/` handles REST API endpoints
- **Package Management**: UV with `pyproject.toml` and `uv.lock`
- **Current Endpoints**: `/api/ping/` (health check)
- **CORS Configuration**: Allows requests from `localhost:5173` and `127.0.0.1:5173`

### Frontend Architecture

- **React + TypeScript**: Modern React 19 with strict TypeScript
- **Build Tool**: Vite for fast development and optimized builds
- **API Communication**: Axios for HTTP requests, environment-based API URLs
- **Development Proxy**: Vite proxies `/api/*` to Django backend
- **Configuration**: `src/config.ts` manages API base URLs

### Key Files

- **Backend Settings**: `backend/config/settings.py` - Django configuration
- **Frontend Entry**: `frontend/src/App.tsx` - Main React component
- **API Config**: `frontend/src/config.ts` - API URL configuration
- **Vite Config**: `frontend/vite.config.ts` - Build and proxy settings

## Development Workflow

### Adding New API Endpoints

1. Create view in `backend/api/views.py`
2. Add URL pattern in `backend/api/urls.py`
3. Update frontend to consume the endpoint using the configured API base URL

### Environment Variables

Frontend uses `VITE_API_BASE_URL` for production API endpoint configuration. In development, the Vite proxy handles routing.

### Database Operations

Default SQLite database. For new models:
1. Define in `backend/api/models.py`
2. Run `uv run python manage.py makemigrations`
3. Run `uv run python manage.py migrate`

## Important Notes

- **Python Version**: Requires Python 3.13+
- **Node Version**: Works with Node.js 18+
- **CORS**: Already configured for local development
- **TypeScript**: Strict mode enabled, always type your code
- **API Proxy**: Frontend development server automatically proxies `/api/*` requests to backend
- **Hot Reload**: Both backend and frontend support hot reloading in development