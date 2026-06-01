import type { APIRoute } from 'astro';

// En SSR (server-side dentro del contenedor Docker), usamos la URL interna
const API_BASE = import.meta.env.SSR
  ? (process.env.SSR_API_URL || 'http://portfolio-api:8000')
  : (import.meta.env.PUBLIC_API_URL || 'http://localhost:8001');

export const GET: APIRoute = async ({ params, cookies, redirect }) => {
  const token = params.token;

  if (!token) {
    return redirect('/login?error=no_token', 302);
  }

  try {
    // Validar el token contra el backend de Portfolio
    const response = await fetch(`${API_BASE}/api/v1/auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      console.error('❌ Token inválido en callback:', response.status);
      return redirect('/login?error=invalid_token', 302);
    }

    // Token válido — extraer exp del payload para el max_age de la cookie
    let maxAge = 86400; // default 24h
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      if (payload.exp) {
        maxAge = payload.exp - Math.floor(Date.now() / 1000);
      }
    } catch {
      // ignorar, usar default
    }

    // Setear cookie httpOnly desde Astro (SSR)
    cookies.set('access_token', token, {
      path: '/',
      httpOnly: true,
      sameSite: 'lax',
      maxAge: maxAge,
    });

    return redirect('/admin', 302);

  } catch (error) {
    console.error('❌ Error en callback Google OAuth:', error);
    return redirect('/login?error=server_error', 302);
  }
};
