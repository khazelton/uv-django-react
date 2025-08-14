# Vite Configuration for React Frontend
# This file configures the Vite build tool and development server
# 
# PROJECT OVERVIEW:
# - Vite configuration for React + TypeScript frontend
# - Development server with hot module replacement (HMR)
# - API proxy configuration for backend communication
# - Production build optimization
#
# CONNECTIONS:
# - Backend: Django API server at http://127.0.0.1:8000
# - Frontend: React app served on http://127.0.0.1:5173
# - Build Tool: Vite for fast development and optimized builds
# - Related to: package.json (scripts), tsconfig.json (TypeScript)
#
# SERVER CONFIGURATION:
# - Host: 127.0.0.1 (IPv4 localhost)
# - Port: 5173 (Vite default)
# - HMR: Hot module replacement for development
#
# PROXY CONFIGURATION:
# - /api/* requests are proxied to Django backend
# - Enables frontend to call /api/ping/ without CORS issues
# - changeOrigin: true for proper host header handling
#
# USAGE:
# - Development: npm run dev (starts Vite dev server)
# - Production: npm run build (creates optimized build)
# - Preview: npm run preview (serves production build)

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  // React plugin for JSX/TSX support
  plugins: [react()],
  
  // Development server configuration
  server: {
    // Bind to IPv4 localhost for consistent access
    host: "127.0.0.1",
    
    // API proxy configuration
    proxy: {
      // Proxy all /api/* requests to Django backend
      "/api": {
        target: "http://127.0.0.1:8000",  // Django server
        changeOrigin: true,                 // Handle host headers properly
      },
    },
  },
})
