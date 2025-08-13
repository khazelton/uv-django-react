// Defaults to "/api" so dev uses Vite proxy and prod can be reverse-proxied
export const API_BASE_URL: string = (import.meta.env.VITE_API_BASE_URL ?? "/api").replace(/\/$/, "");

export function apiUrl(path: string): string {
  const trimmedPath = path.replace(/^\/+/, "");
  return `${API_BASE_URL}/${trimmedPath}`;
}


