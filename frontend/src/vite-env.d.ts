# Vite Environment Type Definitions
# This file provides TypeScript type definitions for Vite-specific features
# 
# PROJECT OVERVIEW:
# - TypeScript declaration file for Vite build tool
# - Provides types for Vite-specific globals and APIs
# - Enables TypeScript support for import.meta.env
# - Required for proper TypeScript integration with Vite
#
# CONNECTIONS:
# - Referenced by: TypeScript compiler
# - Used by: config.ts (import.meta.env.VITE_API_BASE_URL)
# - Part of: Vite TypeScript integration
# - Related to: tsconfig.app.json (TypeScript configuration)
#
# VITE FEATURES ENABLED:
# - import.meta.env: Access to environment variables
# - VITE_* variables: Frontend environment variables
# - Build-time constants: Vite-specific globals
# - Hot module replacement: Development server types
#
# USAGE:
# - import.meta.env.VITE_API_BASE_URL: Access environment variables
# - import.meta.env.MODE: Current build mode (development/production)
# - import.meta.env.DEV: Boolean for development mode
# - import.meta.env.PROD: Boolean for production mode
#
# NOTE: This file is automatically included by Vite and TypeScript

/// <reference types="vite/client" />
