// src/middleware.ts — SSR Middleware para Portfolio
// Valida la cookie access_token (seteada por authCore vía Google OAuth)
// en rutas protegidas /admin/*
//
// Validación REAL del JWT contra JWKS de authCore (no solo base64 decode).
// Usa createRemoteJWKSet que cachea las claves automáticamente (HTTP Cache-Control).

import { defineMiddleware } from 'astro:middleware';
import { createRemoteJWKSet, jwtVerify } from 'jose';

// ── Configuración ─────────────────────────────────────────────
const SITE_ORIGIN = process.env.SITE_ORIGIN;

const AUTHCORE_URL = process.env.PUBLIC_AUTHCORE_URL || 'https://api-authcore.elrincondeharco.com';
const JWKS_URL = new URL(
  process.env.AUTHCORE_JWKS_URL || `${AUTHCORE_URL}/.well-known/jwks.json`
);

const JWKS = createRemoteJWKSet(JWKS_URL);

// Tenant slug esperado para este servicio
const EXPECTED_TENANT = process.env.TENANT_SLUG || 'rincom';

// En desarrollo, la API está en SSR_API_URL (definida en el compose)
const API_URL = process.env.SSR_API_URL || 'http://localhost:8001';

// ── Middleware ─────────────────────────────────────────────────
export const onRequest = defineMiddleware(async (context, next) => {
  const { url, cookies } = context;

  // ── Desarrollo: bypassear auth completamente ───────────────
  // En NODE_ENV=development el backend también bypassea auth,
  // así que no tiene sentido validar contra authCore acá.
  if (process.env.NODE_ENV === 'development' || process.env.DEV) {
    context.locals.user = {
      id: '1',
      username: 'dev',
      role: 'SUPERADMIN',
      tenant: { id: 'dev-tenant', slug: 'rincom', name: 'Dev Tenant' },
      modules: { radar: { enabled: true }, inventory: { enabled: true, providers: ['vinted', 'micolet'] } },
    };
    return next();
  }

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
      // Intentar validar contra authCore (JWKS)
      const { payload } = await jwtVerify(sessionCookie.value, JWKS);
      const userRole = (payload as any).role || '';
      const userTenant = (payload as any).tenant;

      // Validar tenant: SUPERADMIN bypass, otros solo su tenant
      if (userRole.toUpperCase() !== 'SUPERADMIN' && userTenant) {
        const userSlug = userTenant.slug;
        if (userSlug && userSlug !== EXPECTED_TENANT) {
          // Tenant no coincide — redirigir a login con error
          const errUrl = new URL('/login', SITE_ORIGIN || url.origin);
          errUrl.searchParams.set('error', 'wrong_tenant');
          errUrl.searchParams.set('detail', `Acceso denegado: tu empresa es '${userSlug}', no '${EXPECTED_TENANT}'`);
          return context.redirect(errUrl.toString(), 302);
        }
      }

      context.locals.user = {
        id: String(payload.sub || payload.id || ''),
        username: (payload as any).username || (payload as any).email,
        role: userRole,
        tenant: userTenant || null,
        modules: (payload as any).modules || {},
        ...payload,
      };
    } catch (error: any) {
      // ── Fallback: si authCore no está disponible ────────────
      // En lugar de fallar inmediatamente, consultamos al backend local
      // que tiene su propio fallback (HS256 con SECRET_KEY en debug).
      const isConnError = error?.message?.includes('fetch') || error?.message?.includes('connect');

      if (isConnError) {
        console.warn('⚠️ Middleware: authCore no disponible, consultando backend local...');
        try {
          const meResp = await fetch(`${API_URL}/api/v1/auth/me`, {
            headers: { Cookie: `access_token=${sessionCookie.value}` },
            signal: AbortSignal.timeout(5000),
          });

          if (!meResp.ok) throw new Error(`Backend respondió ${meResp.status}`);

          const userData = await meResp.json();
          context.locals.user = {
            id: String(userData.id || ''),
            username: userData.username || '',
            role: userData.role || '',
            ...userData,
          };
          console.info('✅ Middleware: sesión validada por backend local');
          return next();
        } catch (meError) {
          console.error('❌ Middleware: fallback a backend también falló:', (meError as Error).message);
          // Si el fallback también falla, redirigir a login con error
          cookies.delete('access_token', { path: '/' });
          const errUrl = new URL('/login', SITE_ORIGIN || url.origin);
          errUrl.searchParams.set('error', 'auth_unavailable');
          errUrl.searchParams.set('redirect', url.pathname + url.search);
          return context.redirect(errUrl.toString(), 302);
        }
      }

      // ── Error de firma/expiración — token inválido ──────────
      const errorCode = error?.code || 'invalid_token';
      let errorParam = 'invalid_token';

      if (errorCode === 'ERR_JWT_EXPIRED') errorParam = 'expired_token';
      else if (errorCode === 'ERR_JWS_INVALID') errorParam = 'invalid_signature';

      console.error(`❌ Middleware Portfolio [${errorParam}]:`, error?.message);

      cookies.delete('access_token', { path: '/' });
      const errorUrl = new URL('/login', SITE_ORIGIN || url.origin);
      errorUrl.searchParams.set('error', errorParam);
      errorUrl.searchParams.set('redirect', url.pathname + url.search);
      return context.redirect(errorUrl.toString(), 302);
    }
  }

  return next();
});
