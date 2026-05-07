import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

export default defineConfig({
  // Solo dejamos Svelte, Tailwind se encargará mediante PostCSS/Vite
  integrations: [svelte()],
  server: {
    port: 4322,
    strictPort: true, // Evita que Astro salte a otro puerto si el 4322 está ocupado
    host: true       // Útil si necesitas acceder desde otros dispositivos en tu red local
  }
});