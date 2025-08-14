# API Configuration and Utilities
# This file provides configuration for API endpoints and utility functions
# 
# PROJECT OVERVIEW:
# - Centralized API configuration for the React frontend
# - Environment-driven API base URL configuration
# - Utility function for constructing full API URLs
# - Supports both development (proxy) and production (direct) API calls
#
# CONNECTIONS:
# - Used by: App.tsx (main component for API calls)
# - Environment: VITE_API_BASE_URL for production configuration
# - Development: Uses Vite proxy at /api
# - Production: Can be set to full backend URL
#
# CONFIGURATION:
# - Development: API_BASE_URL = "/api" (uses Vite proxy)
# - Production: VITE_API_BASE_URL can be set to full backend URL
# - Fallback: Defaults to "/api" if no environment variable
# - Normalization: Removes trailing slashes for consistency
#
# USAGE:
# - App.tsx calls apiUrl("/api/ping/") -> "/api/api/ping/" (dev) or "https://backend.com/api/ping/" (prod)
# - Environment variable: VITE_API_BASE_URL=https://api.example.com
# - Development proxy: /api/* -> http://127.0.0.1:8000/api/*
#
# NOTE: The double /api in development is handled by Vite's proxy configuration

// Defaults to "/api" so dev uses Vite proxy and prod can be reverse-proxied
export const API_BASE_URL: string = (import.meta.env.VITE_API_BASE_URL ?? "/api").replace(/\/$/, "");

/**
 * Constructs a full API URL from a path
 * 
 * @param path - API endpoint path (e.g., "api/ping/")
 * @returns Full API URL with base URL and path
 * 
 * Examples:
 * - apiUrl("api/ping/") -> "/api/api/ping/" (dev) or "https://backend.com/api/ping/" (prod)
 * - apiUrl("/api/ping/") -> "/api/api/ping/" (dev) or "https://backend.com/api/ping/" (prod)
 */
export function apiUrl(path: string): string {
  // Remove leading slashes from path to avoid double slashes
  const trimmedPath = path.replace(/^\/+/, "");
  // Combine base URL with trimmed path
  return `${API_BASE_URL}/${trimmedPath}`;
}


