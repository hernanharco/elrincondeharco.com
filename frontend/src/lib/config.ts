/**
 * Configuración de API para Portfolio.
 * El JWT viaja en cookie httpOnly (HTTP Only Cookie) en vez de localStorage.
 * La cookie la setea authCore (Google OAuth) o el backend de Portfolio (login con credenciales).
 */

 const API_BASE_URL = import.meta.env.PUBLIC_API_URL;

export async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string>),
  };

  // La cookie httpOnly se envía automáticamente con credentials: 'include'
  const config: RequestInit = {
    ...options,
    headers,
    credentials: 'include',
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    let errorMessage = 'Error desconocido del servidor';
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // usar mensaje por defecto
    }
    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}
