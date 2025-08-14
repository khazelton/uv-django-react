# React + TypeScript + Vite Frontend

<!-- 
  PROJECT OVERVIEW:
  This is the frontend portion of a full-stack Django + React application.
  The frontend is built with modern React 19, TypeScript, and Vite for fast development.
  
  CONNECTIONS:
  - Backend: Django API server at http://localhost:8000
  - API: Communicates with Django backend via /api/* endpoints
  - Build Tool: Vite for development and production builds
  - Package Manager: npm with package-lock.json
  
  ARCHITECTURE:
  - React 19 with TypeScript for type safety
  - Vite for fast development server and optimized builds
  - ESLint for code quality and consistency
  - CSS modules and global styles for styling
  
  DEVELOPMENT:
  - Hot Module Replacement (HMR) for fast development
  - TypeScript compilation and type checking
  - ESLint rules for React and TypeScript best practices
  - Proxy configuration for API calls to Django backend
  
  USAGE:
  - Development: npm run dev (starts Vite dev server)
  - Build: npm run build (creates production build)
  - Lint: npm run lint (runs ESLint checks)
  - Preview: npm run preview (serves production build)
-->

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      ...tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      ...tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      ...tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
