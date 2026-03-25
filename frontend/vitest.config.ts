import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      reporter: ['text', 'html', 'json'],
      exclude: [
        'node_modules/**',
        '.svelte-kit/**',
        'tests/**',
        '**/*.d.ts',
        '**/*.config.*'
      ]
    },
    globals: true
  }
});
