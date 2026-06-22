/**
 * ──────────────────────────────────────────────────────────────
 * config.ts — Re-export desde api.ts
 * ──────────────────────────────────────────────────────────────
 * Mantenido por compatibilidad con imports existentes.
 * Toda la lógica nueva va en api.ts.
 *
 * Antiguo:
 *   import { fetchApi } from '$lib/config';
 * Sigue funcionando:
 *   import { fetchApi } from '$lib/config';
 * Nuevo (recomendado):
 *   import { fetchApi, fetchSSR } from '$lib/api';
 * ──────────────────────────────────────────────────────────────
 */
export { fetchApi, fetchSSR } from '$lib/api';
