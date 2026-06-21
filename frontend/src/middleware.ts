// src/middleware.ts — SSR Middleware para Portfolio
// Valida la cookie access_token (seteada por authCore vía Google OAuth)
// en rutas protegidas /admin/*

import { defineMiddleware } from 'astro:middleware';

const SITE_ORIGIN = process.env.SITE_ORIGIN || 'http://localhost:4322';

export const onRequest = defineMiddleware((context, next) => {
  const { url, cookies } = context;

  // Rutas públicas — no requieren autenticación
  const publicRoutes = ['/login', '/api/auth', '/_astro', '/favicon.ico', '/public'];
  const isPublicRoute = publicRoutes.some(route => url.pathname.startsWith(route));
  if (isPublicRoute) return next();

  // Proteger rutas /admin
  const isProtectedRoute = url.pathname.startsWith('/admin');

  if (isProtectedRoute) {
    const sessionCookie = cookies.get('access_token');

    if (!sessionCookie || !sessionCookie.value) {
      const loginUrl = new URL('/login', SITE_ORIGIN);
      loginUrl.searchParams.set('error', 'no_session');
      loginUrl.searchParams.set('redirect', url.pathname + url.search);
      return context.redirect(loginUrl.toString(), 302);
    }

    try {
      const parts = sessionCookie.value.split('.');
      if (parts.length !== 3) throw new Error('JWT format invalid');

      // Solo decodificamos el payload para lectura — la firma la valida el backend
      const payload = JSON.parse(atob(parts[1]));
      const now = Math.floor(Date.now() / 1000);

      if (payload.exp && payload.exp < now) {
        cookies.delete('access_token', { path: '/' });
        const expiredUrl = new URL('/login', SITE_ORIGIN);
        expiredUrl.searchParams.set('error', 'expired_token');
        return context.redirect(expiredUrl.toString(), 302);
      }

      // Guardamos info del usuario para usar en layouts/páginas
      context.locals.user = {
        id: payload.sub || payload.id,
        username: payload.username || payload.email,
        role: payload.role,
        ...payload,
      };
    } catch (error) {
      console.error('❌ Error en Middleware Portfolio:', error);
      cookies.delete('access_token', { path: '/' });
      const errorUrl = new URL('/login', SITE_ORIGIN);
      errorUrl.searchParams.set('error', 'invalid_token');
      return context.redirect(errorUrl.toString(), 302);
    }
  }

  return next();
});
