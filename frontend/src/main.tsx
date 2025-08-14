# React Application Entry Point
# This file is the main entry point for the React application
# 
# PROJECT OVERVIEW:
# - Initializes the React application and renders it to the DOM
# - Sets up React 18+ createRoot API for concurrent features
# - Wraps the app in StrictMode for development checks
# - Imports global CSS and main App component
#
# CONNECTIONS:
# - Imports: React, ReactDOM, index.css, App.tsx
# - Renders to: HTML element with id "root"
# - Entry point: Called when the page loads
# - Related to: index.html (root element), App.tsx (main component)
#
# REACT 18+ FEATURES:
# - createRoot: Modern React 18+ rendering API
# - StrictMode: Development-time checks and warnings
# - Concurrent features: Automatic batching and suspense
#
# USAGE:
# - This file is automatically called when the app starts
# - No manual invocation needed
# - Entry point for the entire React application

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Create the root container and render the React app
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
