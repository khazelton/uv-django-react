# Django API Views
# This file contains the view functions that handle HTTP requests for the API app
# 
# PROJECT OVERVIEW:
# - Simple API endpoints for the React frontend
# - Uses Django's JsonResponse for JSON API responses
# - Currently has a ping endpoint for testing connectivity
# - Can be extended with more complex API views as needed
#
# CONNECTIONS:
# - Imports: django.http.JsonResponse
# - Referenced by: api/urls.py (URL routing)
# - Called by: Frontend React app via HTTP requests
# - Related to: config/urls.py (main URL configuration)
#
# API ENDPOINTS:
# - ping: Simple health check endpoint that returns {"message": "pong"}
#   - Method: GET
#   - URL: /api/ping/
#   - Purpose: Test backend connectivity from frontend
#
# USAGE:
# - Frontend calls: fetch('/api/ping/') or fetch('http://localhost:8000/api/ping/')
# - Returns: JSON response with message field
# - Used by: React App.tsx component for testing API connection

from django.http import JsonResponse

def ping(_request):
    """
    Simple ping endpoint for testing API connectivity.
    
    Args:
        _request: Django HttpRequest object (unused, prefixed with _)
        
    Returns:
        JsonResponse: {"message": "pong"}
        
    Purpose:
        - Health check endpoint
        - Test backend connectivity
        - Verify CORS configuration
    """
    return JsonResponse({"message": "pong"})
