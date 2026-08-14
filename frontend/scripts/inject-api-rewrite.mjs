/**
 * inject-api-rewrite.mjs — Inyecta el rewrite /api/v1 → API backend en el
 * output de Vercel (Build Output API v3).
 *
 * El adapter de Astro (@astrojs/vercel v10) NO lee "rewrites" de
 * vercel.json (los hardcodea vacíos), así que este script agrega la ruta
 * directamente al config.json generado por el build.
 *
 * Motivo: el admin (www.rincom.es) y la API (api.elrincondeharco.com) son
 * dominios distintos; la cookie httpOnly access_token (seteada por OAuth en
 * www.rincom.es) jamás viaja cross-origin. Con el rewrite las llamadas del
 * admin a /api/v1/* son same-origin: la cookie viaja y Vercel reenvía a la
 * API (que lee access_token de la cookie).
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const configPath = join(root, '.vercel', 'output', 'config.json');

const DEST = 'https://api.elrincondeharco.com/api/v1/$1';
const ROUTE = { src: '^/api/v1/(.*)$', dest: DEST };

const raw = readFileSync(configPath, 'utf8');
const config = JSON.parse(raw);
const routes = config.routes ?? [];

// No duplicar si ya existe
const already = routes.some((r) => r.dest === DEST);
if (!already) {
  // Insertar después del handler de filesystem (primera entrada) o al inicio.
  const idx = routes.findIndex((r) => r.handle === 'filesystem');
  routes.splice(idx >= 0 ? idx + 1 : 0, 0, ROUTE);
  config.routes = routes;
  writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
  console.log('[inject-api-rewrite] rewrite /api/v1/* inyectado en config.json');
} else {
  console.log('[inject-api-rewrite] rewrite ya presente, sin cambios');
}
