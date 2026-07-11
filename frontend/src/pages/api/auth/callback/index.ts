export const prerender = false;
import type { APIRoute } from 'astro';
import { createRemoteJWKSet, jwtVerify } from 'jose';

// authCore URLs
const AUTHCORE_URL = process.env.PUBLIC_AUTHCORE_URL || 'https://api-authcore.elrincondeharco.com';
const JWKS_URL = new URL(
  process.env.AUTHCORE_JWKS_URL || `${AUTHCORE_URL}/.well-known/jwks.json`
);

const JWKS = createRemoteJWKSet(JWKS_URL);

export const GET: APIRoute = async ({ url, cookies, redirect }) => {
  // authCore redirige con: /api/auth/callback?token=JWT_VALUE
  const token = url.searchParams.get('token');

  if (!token) {
    return redirect('/login?error=no_token', 302);
  }

  try {
    // Validar JWT directamente contra authCore JWKS
    const { payload } = await jwtVerify(token, JWKS, {
      algorithms: ['RS256', 'ES256'],
    });

    let maxAge = 86400;
    if (payload.exp) {
      maxAge = Number(payload.exp) - Math.floor(Date.now() / 1000);
    }

    cookies.set('access_token', token, {
      path: '/',
      httpOnly: true,
      sameSite: 'lax',
      maxAge: maxAge,
    });

    return redirect('/admin', 302);

  } catch (error) {
    console.error('Error validando token contra authCore:', error);
    return redirect('/login?error=invalid_token', 302);
  }
};
