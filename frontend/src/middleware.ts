// src/middleware.ts — SSR Middleware para Portfolio
// Valida la cookie access_token (seteada por authCore vía Google OAuth)
// en rutas protegidas /admin/*
//
// Validación REAL del JWT contra JWKS de authCore (no solo base64 decode).
// Usa createRemoteJWKSet que cachea las claves automáticamente (HTTP Cache-Control).

import { defineMiddleware } from 'astro:middleware';
import { createRemoteJWKSet, jwtVerify } from 'jose';

// ── Configuración ─────────────────────────────────────────────
const SITE_ORIGIN = process.env.SITE_ORIGIN; // Opcional, fallback a context.url.origin

// URL del JWKS de authCore (para validar la firma del JWT)
// Fallback: http://localhost:8000 (desarrollo local sin Docker)
const AUTHCORE_URL = process.env.PUBLIC_AUTHCORE_URL || 'http://localhost:8000';
const JWKS_URL = new URL(
  process.env.AUTHCORE_JWKS_URL || `${AUTHCORE_URL}/.well-known/jwks.json`
);

// Cliente JWKS con caché automática (createRemoteJWKSet maneja el caching)
const JWKS = createRemoteJWKSet(JWKS_URL);

// ── Middleware ─────────────────────────────────────────────────
export const onRequest = defineMiddleware(async (context, next) => {
  const { url, cookies } = context;

  // ── Rutas públicas ──────────────────────────────────────────
  const publicRoutes = ['/login', '/api/auth', '/_astro', '/favicon.ico', '/public'];
  const isPublicRoute = publicRoutes.some(route => url.pathname.startsWith(route));
  if (isPublicRoute) return next();

  // ── Proteger rutas /admin ──────────────────────────────────
  const isProtectedRoute = url.pathname.startsWith('/admin');

  if (isProtectedRoute) {
    const sessionCookie = cookies.get('access_token');

    // Sin cookie → redirect a login
    if (!sessionCookie || !sessionCookie.value) {
      const loginUrl = new URL('/login', SITE_ORIGIN || url.origin);
      loginUrl.searchParams.set('error', 'no_session');
      loginUrl.searchParams.set('redirect', url.pathname + url.search);
      return context.redirect(loginUrl.toString(), 302);
    }

    try {
      // Validar el JWT contra el JWKS de authCore
      // jose.jwtVerify verifica: firma (RS256/ES256), exp, iss, aud
      const { payload } = await jwtVerify(sessionCookie.value, JWKS, {
        // Opcional: validar issuer si authCore lo setea
        // issuer: 'authcore',
        // Opcional: validar audience
        // audience: 'portfolio',
      });

      // El token es VÁLIDO — guardamos info del usuario
      context.locals.user = {
        id: payload.sub || payload.id,
        username: (payload as any).username || (payload as any).email,
        role: (payload as any).role,
        ...payload,
      };
    } catch (error: any) {
      // ── Manejo de errores específicos ───────────────────────
      const errorCode = error?.code || 'invalid_token';
      let errorParam = 'invalid_token';

      if (errorCode === 'ERR_JWT_EXPIRED') {
        errorParam = 'expired_token';
      } else if (errorCode === 'ERR_JWS_INVALID') {
        errorParam = 'invalid_signature';
      } else if (errorCode === 'ERR_JWK_MULTIPLE_MATCHING_KEYS') {
        errorParam = 'invalid_token';
      }

      // Si authCore está caído, no podemos verificar — fail closed
      if (error?.message?.includes('fetch') || error?.message?.includes('connect')) {
        console.error('❌ Middleware: authCore no disponible:', error.message);
        errorParam = 'auth_unavailable';
      }

      console.error(`❌ Middleware Portfolio [${errorParam}]:`, error?.message);

      // Limpiar cookie inválida y redirigir
      cookies.delete('access_token', { path: '/' });
      const errorUrl = new URL('/login', SITE_ORIGIN || url.origin);
      errorUrl.searchParams.set('error', errorParam);
      errorUrl.searchParams.set('redirect', url.pathname + url.search);
      return context.redirect(errorUrl.toString(), 302);
    }
  }

  return next();
});
