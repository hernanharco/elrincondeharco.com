import '@testing-library/jest-dom';

// Mock fetch globally
global.fetch = vi.fn();

// Mock environment variables
vi.mock('$app/environment', () => ({
  dev: true,
  browser: true,
  building: false,
  version: '1.0.0'
}));

// Mock import.meta.env
vi.mock('$app/environment', () => ({
  dev: true,
  browser: true,
  building: false,
  version: '1.0.0'
}));

// Setup fetch mock
beforeEach(() => {
  (fetch as any).mockClear();
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
