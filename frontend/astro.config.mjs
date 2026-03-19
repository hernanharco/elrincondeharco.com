import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

export default defineConfig({
  // Solo dejamos Svelte, Tailwind se encargará mediante PostCSS/Vite
  integrations: [svelte()],
});