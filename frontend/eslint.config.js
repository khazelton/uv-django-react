# ESLint Configuration for React TypeScript Project
# This file configures code linting and quality checks for the frontend
# 
# PROJECT OVERVIEW:
# - ESLint configuration for React + TypeScript code quality
# - Modern flat config format (ESLint 9+)
# - Integrates TypeScript, React, and Vite-specific rules
# - Ensures consistent code style and catches common errors
#
# CONNECTIONS:
# - Used by: npm run lint command
# - Integrates: TypeScript, React, React Hooks, Vite
# - Targets: All .ts and .tsx files in the project
# - Related to: package.json (lint script), tsconfig files
#
# LINTING FEATURES:
# - TypeScript: Type-aware linting with tseslint
# - React: React-specific rules and best practices
# - React Hooks: Hook usage rules and dependencies
# - React Refresh: Vite HMR compatibility rules
# - Browser: Browser globals and environment
#
# CONFIGURATION:
# - Flat config: Modern ESLint configuration format
# - Global ignores: Excludes dist/ directory from linting
# - File targeting: Applies to TypeScript and TSX files
# - Rule sets: Recommended configurations from all plugins
#
# USAGE:
# - npm run lint: Run linting on all files
# - IDE integration: Most editors show linting errors in real-time
# - CI/CD: Can be run in automated pipelines

import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import { globalIgnores } from 'eslint/config'

export default tseslint.config([
  // Ignore build output directory
  globalIgnores(['dist']),
  
  // Main configuration for TypeScript and React files
  {
    files: ['**/*.{ts,tsx}'],  // Target TypeScript and TSX files
    extends: [
      js.configs.recommended,                    // JavaScript recommended rules
      tseslint.configs.recommended,              // TypeScript recommended rules
      reactHooks.configs['recommended-latest'],  // React Hooks best practices
      reactRefresh.configs.vite,                 // Vite HMR compatibility
    ],
    languageOptions: {
      ecmaVersion: 2020,           // Modern JavaScript features
      globals: globals.browser,    // Browser environment globals
    },
  },
])
