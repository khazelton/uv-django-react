export const API_BASE_URL: string = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");

export function apiUrl(path: string): string {
  const trimmedPath = path.replace(/^\/+/, "");
  return `${API_BASE_URL}/${trimmedPath}`;
}

export function getApiUrl(): string {
  return API_BASE_URL || "";
}


