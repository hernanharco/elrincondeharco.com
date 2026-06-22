import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: [
      { find: '$lib/components', replacement: path.resolve(__dirname, './src/components') },
      { find: '$lib', replacement: path.resolve(__dirname, './src/lib') },
    ],
    conditions: ['import', 'svelte'],
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/**/*.test.ts'],
    exclude: ['tests/e2e/**', 'tests/integration/**', 'node_modules/**'],
    env: {
      PUBLIC_API_URL: 'http://localhost:8000',
    },
    coverage: {
      reporter: ['text', 'html', 'json'],
      exclude: [
        'node_modules/**',
        'tests/**',
        '**/*.d.ts',
        '**/*.config.*'
      ]
    },
    globals: true,
  }
});
