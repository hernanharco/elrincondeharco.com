import { defineConfig } from 'vitest/config';
import path from 'path';

/**
 * Stub plugin to handle .svelte imports in test environment.
 * Returns a minimal mock component so Svelte compilation isn't needed.
 */
function svelteStubPlugin() {
  return {
    name: 'svelte-stub',
    enforce: 'pre' as const,
    resolveId(id: string) {
      if (id.endsWith('.svelte')) {
        return { id: id.replace(/\.svelte$/, '.svelte.js'), external: false };
      }
      return null;
    },
    load(id: string) {
      if (id.endsWith('.svelte.js')) {
        return 'export default { render: () => "" };';
      }
      return null;
    },
  };
}

export default defineConfig({
  plugins: [svelteStubPlugin()],
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
    exclude: [
      'tests/e2e/**',
      'tests/integration/**',
      'node_modules/**',
    ],
    // Component tests migrated to Playwright (E2E)
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
