import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

// ── URL base de authCore (backend) ──────────────────────────
// En desarrollo local: http://localhost:8000
// En Docker: http://authcore-api:8000
const AUTHCORE_API = process.env.PUBLIC_AUTHCORE_URL || 'http://localhost:8000';

export default defineConfig({
  output: 'server',
  integrations: [svelte()],
  server: {
    port: 4322,
    strictPort: true,
    host: true
  },
  vite: {
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