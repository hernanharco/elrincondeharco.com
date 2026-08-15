/**
 * /api/v1/[...path].ts — Proxy same-origin hacia la API del portfolio.
 *
 * El admin (www.rincom.es) y la API (api.elrincondeharco.com) son dominios
 * distintos. La cookie httpOnly access_token (seteada por OAuth en
 * www.rincom.es) jamás viaja cross-origin, por eso los guardados del admin
 * respondían 401. Este endpoint recibe las llamadas del admin en el MISMO
 * dominio (la cookie viaja normal) y las reenvía a la API conservando el
 * header Cookie, de modo que el backend autentica correctamente.
 */
export const prerender = false;

import type { APIRoute } from 'astro';

const API_URL = process.env.SSR_API_URL || 'https://api.elrincondeharco.com';

export const ALL: APIRoute = async ({ params, request }) => {
  const path = params.path || '';
  const upstreamUrl = `${API_URL}/api/v1/${path}`;

  // Reenviar cookies (incluye access_token httpOnly) y content-type.
  const headers: Record<string, string> = {};
  const cookie = request.headers.get('cookie');
  if (cookie) headers.cookie = cookie;
  const contentType = request.headers.get('content-type');
  if (contentType) headers['content-type'] = contentType;

  // GET/HEAD sin body; el resto (POST/PUT/DELETE con FormData o JSON) se reenvía.
  const method = request.method;
  const body =
    method === 'GET' || method === 'HEAD'
      ? undefined
      : await request.arrayBuffer();

  const upstream = await fetch(upstreamUrl, { method, headers, body });

  // Reenviar content-type y Set-Cookie (para login/logout por el proxy).
  const responseHeaders = new Headers();
  const upContentType = upstream.headers.get('content-type');
  if (upContentType) responseHeaders.set('content-type', upContentType);
  const setCookie = upstream.headers.getSetCookie?.() ?? [];
  for (const sc of setCookie) responseHeaders.append('set-cookie', sc);

  return new Response(upstream.body, {
    status: upstream.status,
    headers: responseHeaders,
  });
};
