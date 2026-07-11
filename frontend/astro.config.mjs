import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

// ── URL base de authCore (backend) ──────────────────────────
// En desarrollo local: http://localhost:8000
// En Docker: http://authcore-api:8000
const AUTHCORE_API = process.env.PUBLIC_AUTHCORE_URL || 'http://localhost:8000';

// ── Adaptador Vercel (solo en producción) ───────────────────
// Vercel setea automáticamente la variable VERCEL=1 durante el build.
// En desarrollo local no se necesita ni se importa.
let adapter;
if (process.env.VERCEL) {
  const { default: vercel } = await import('@astrojs/vercel');
  adapter = vercel({ isr: false });
}

export default defineConfig({
  output: 'static',
  ...(adapter ? { adapter } : {}),
  integrations: [svelte()],
  server: {
    port: 4322,
    strictPort: true,
    host: true
  },
  vite: {
    optimizeDeps: {
      include: ['@iconify/svelte'],
    },
    ssr: {
      noExternal: ['@iconify/svelte'],
    },
    server: {
      proxy: {
        // Proxy para llamadas a authCore desde el frontend
        '/auth-proxy': {
          target: AUTHCORE_API,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/auth-proxy/, ''),
        },
      },
    },
  }
});