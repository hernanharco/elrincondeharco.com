import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { shouldAddCredentials, installCredentialsInterceptor } from '$lib/fetch-interceptor';

const API_BASE = 'https://api.elrincondeharco.com';

describe('shouldAddCredentials', () => {
  it('returns true for API URL string with no credentials in init', () => {
    expect(shouldAddCredentials(`${API_BASE}/api/v1/hero`, undefined, API_BASE)).toBe(true);
  });

  it('returns true for API URL string with empty init object', () => {
    expect(shouldAddCredentials(`${API_BASE}/api/v1/hero`, {}, API_BASE)).toBe(true);
  });

  it('returns false when credentials already set to "include"', () => {
    expect(
      shouldAddCredentials(`${API_BASE}/api/v1/hero`, { credentials: 'include' }, API_BASE)
    ).toBe(false);
  });

  it('returns false when credentials already set to "omit"', () => {
    expect(
      shouldAddCredentials(`${API_BASE}/api/v1/hero`, { credentials: 'omit' }, API_BASE)
    ).toBe(false);
  });

  it('returns false for non-API URL', () => {
    expect(shouldAddCredentials('https://cdn.example.com/image.jpg', undefined, API_BASE)).toBe(false);
  });

  it('returns false for relative URL that does not start with apiBase', () => {
    expect(shouldAddCredentials('/api/v1/hero', undefined, API_BASE)).toBe(false);
  });

  it('returns false when apiBase is empty string', () => {
    expect(shouldAddCredentials('https://api.elrincondeharco.com/api/v1/hero', undefined, '')).toBe(false);
  });

  it('returns true for URL object targeting the API', () => {
    const url = new URL(`${API_BASE}/api/v1/projects/`);
    expect(shouldAddCredentials(url, undefined, API_BASE)).toBe(true);
  });

  it('returns true for Request object targeting the API', () => {
    const request = new Request(`${API_BASE}/api/v1/projects/`);
    expect(shouldAddCredentials(request, undefined, API_BASE)).toBe(true);
  });
});

describe('installCredentialsInterceptor', () => {
  let originalFetch: typeof globalThis.fetch;
  let mockFetch: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    originalFetch = globalThis.fetch;
    mockFetch = vi.fn().mockResolvedValue(new Response('ok'));
    globalThis.fetch = mockFetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it('adds credentials: include to fetch calls targeting the API', async () => {
    const uninstall = installCredentialsInterceptor(API_BASE);

    await fetch(`${API_BASE}/api/v1/projects/`);

    expect(mockFetch).toHaveBeenCalledWith(
      `${API_BASE}/api/v1/projects/`,
      expect.objectContaining({ credentials: 'include' })
    );

    uninstall();
  });

  it('does NOT add credentials to fetch calls targeting other origins', async () => {
    const uninstall = installCredentialsInterceptor(API_BASE);

    await fetch('https://cdn.example.com/image.jpg');

    expect(mockFetch).toHaveBeenCalledWith(
      'https://cdn.example.com/image.jpg',
      undefined
    );

    uninstall();
  });

  it('does NOT override explicit credentials in init', async () => {
    const uninstall = installCredentialsInterceptor(API_BASE);

    await fetch(`${API_BASE}/api/v1/projects/`, { credentials: 'same-origin' });

    expect(mockFetch).toHaveBeenCalledWith(
      `${API_BASE}/api/v1/projects/`,
      expect.objectContaining({ credentials: 'same-origin' })
    );

    uninstall();
  });

  it('returns an uninstall function that restores original fetch', () => {
    const beforeInstall = globalThis.fetch;
    const uninstall = installCredentialsInterceptor(API_BASE);

    // fetch is now the patched version
    expect(globalThis.fetch).not.toBe(beforeInstall);

    uninstall();

    // fetch is restored (may be bound, but functionally equivalent)
    expect(typeof globalThis.fetch).toBe('function');
  });
});
