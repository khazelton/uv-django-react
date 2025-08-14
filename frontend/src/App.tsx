# Main React Application Component
# This file contains the primary React component that renders the application
# 
# PROJECT OVERVIEW:
# - Main application component that demonstrates backend connectivity
# - Uses React hooks (useState, useEffect) for state management
# - Makes API call to Django backend on component mount
# - Displays the response from the backend API
#
# CONNECTIONS:
# - Imports: React hooks, config.ts (API configuration), App.css (styling)
# - API Call: Fetches from Django backend at /api/ping/
# - State: Manages message state for API response
# - Styling: Uses App.css for component styling
#
# COMPONENT FEATURES:
# - useState: Manages message state (loading, success, error)
# - useEffect: Makes API call when component mounts
# - Error handling: Shows "backend unreachable" on API failure
# - Responsive: Updates UI based on API response
#
# API INTEGRATION:
# - Endpoint: /api/ping/ (Django backend)
# - Method: GET request
# - Response: {"message": "pong"}
# - Error handling: Graceful fallback for connection issues
#
# USAGE:
# - Rendered by main.tsx as the root component
# - Automatically calls backend API on page load
# - Demonstrates full-stack connectivity

import { useEffect, useState } from "react";
import { apiUrl } from "./config";
import "./App.css";

function App() {
  // State to store the API response message
  const [message, setMessage] = useState<string>("loading...");
  
  // Effect hook to call the backend API when component mounts
  useEffect(() => {
    // Fetch from Django backend using the configured API base URL
    fetch(apiUrl("/api/ping/"))
      .then((r) => r.json())                    // Parse JSON response
      .then((data) => setMessage(data.message)) // Update state with response
      .catch(() => setMessage("backend unreachable")); // Handle errors
  }, []); // Empty dependency array means this runs once on mount
  
  return (
    <>
      <h1>uv + Django + React</h1>
      <p>API says: {message}</p>
    </>
  );
}

export default App;
