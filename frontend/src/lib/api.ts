/**
 * ──────────────────────────────────────────────────────────────
 * api.ts — Funciones de fetch para el Portfolio
 * ──────────────────────────────────────────────────────────────
 *
 * fetchSSR:   Usada en frontmatter de .astro (server-side).
 *             En Docker usa SSR_API_URL (red interna).
 *             En dev local usa PUBLIC_API_URL o fallback.
 *
 * fetchApi:   Usada en componentes Svelte (client-side).
 *             Envía cookies httpOnly con credentials: 'include'.
 * ──────────────────────────────────────────────────────────────
 */

// ── Server-Side Rendering (SSR) ─────────────────────────────
// Se ejecuta en el frontmatter de los .astro (servidor)
const SSR_BASE_URL: string =
  (typeof import.meta !== 'undefined' && (import.meta as any).env?.SSR_API_URL) ||
  (typeof process !== 'undefined' && process.env?.SSR_API_URL) ||
  (typeof import.meta !== 'undefined' && (import.meta as any).env?.PUBLIC_API_URL) ||
  'http://localhost:8000';

/**
 * fetchSSR — fetch desde el servidor (SSR) hacia la API.
 * Retorna los datos tipados o null si falla.
 * Ideal para usarlo en el frontmatter de componentes .astro:
 *
 *   ---
 *   const data = await fetchSSR<HeroResponse>('/heroes/latest/');
 *   ---
 */
export async function fetchSSR<T>(endpoint: string): Promise<T | null> {
  try {
    const url = `${SSR_BASE_URL}/api/v1${endpoint}`;
    const res = await fetch(url, { next: { revalidate: 60 } });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch (err) {
    console.error(`[fetchSSR] Error fetching ${endpoint}:`, err);
    return null;
  }
}

// ── Client-Side Fetch ────────────────────────────────────────
// Usada en componentes Svelte (con credentials para cookies)
const CLIENT_API_URL = (typeof import.meta !== 'undefined' && (import.meta as any).env?.PUBLIC_API_URL) || 'http://localhost:8000';

export async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${CLIENT_API_URL}${endpoint}`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string>),
  };

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
