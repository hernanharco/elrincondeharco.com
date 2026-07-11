export const prerender = false;
import type { APIRoute } from 'astro';
import { createRemoteJWKSet, jwtVerify } from 'jose';

// authCore URLs (fallback a producción si no hay env vars)
const AUTHCORE_URL = process.env.PUBLIC_AUTHCORE_URL || 'https://api-authcore.elrincondeharco.com';
const JWKS_URL = new URL(
  process.env.AUTHCORE_JWKS_URL || `${AUTHCORE_URL}/.well-known/jwks.json`
);

// Cliente JWKS con caché automática
const JWKS = createRemoteJWKSet(JWKS_URL);

export const GET: APIRoute = async ({ params, cookies, redirect }) => {
  const token = params.token;

  if (!token) {
    return redirect('/login?error=no_token', 302);
  }

  try {
    // Validar el JWT directamente contra authCore (JWKS)
    // Esto verifica: firma RS256/ES256, expiración, issuer, audience
    const { payload } = await jwtVerify(token, JWKS, {
      algorithms: ['RS256', 'ES256'],
      // issuer y audience son opcionales — authCore los setea
    });

    // Token válido — extraer exp del payload para el max_age de la cookie
    let maxAge = 86400; // default 24h
    if (payload.exp) {
      maxAge = Number(payload.exp) - Math.floor(Date.now() / 1000);
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
    console.error('❌ Error validando token contra authCore:', error);
    return redirect('/login?error=invalid_token', 302);
  }
};
