import '@testing-library/jest-dom';
import { vi, beforeEach } from 'vitest';

// Mock all .svelte component imports — no compile needed in tests
vi.mock('$lib/components/sections/Hero.svelte', () => ({
  default: { render: () => '' }
}));
vi.mock('$lib/components/sections/About.svelte', () => ({
  default: { render: () => '' }
}));
vi.mock('$lib/components/sections/Stack.svelte', () => ({
  default: { render: () => '' }
}));
vi.mock('$lib/components/sections/Projects.svelte', () => ({
  default: { render: () => '' }
}));
vi.mock('$lib/components/sections/Passions.svelte', () => ({
  default: { render: () => '' }
}));
vi.mock('$lib/components/layout/Footer.svelte', () => ({
  default: { render: () => '' }
}));
vi.mock('$lib/components/layout/Navbar.svelte', () => ({
  default: { render: () => '' }
}));

// Mock fetch globally
global.fetch = vi.fn();

// Setup fetch mock
beforeEach(() => {
  vi.clearAllMocks();
});

// Mock API responses
const mockApiResponse = (data: any, ok = true) => {
  (fetch as any).mockResolvedValueOnce({
    ok,
    json: async () => data,
    status: ok ? 200 : 400
  });
};

export { mockApiResponse };
