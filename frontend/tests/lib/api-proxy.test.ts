// @vitest-environment node
/**
 * Unit tests for the Astro API proxy: src/pages/api/v1/[...path].ts
 *
 * The proxy is NOT modified — these tests verify its behavior as-is.
 *
 * Why node environment: jsdom's Headers doesn't implement getSetCookie(),
 * which the proxy uses to propagate Set-Cookie from upstream.
 *
 * Strategy (D5):
 *   1. vi.stubEnv('SSR_API_URL', ...) BEFORE dynamic import
 *      → the proxy captures API_URL at module scope
 *   2. vi.stubGlobal('fetch', ...) per test
 *      → captures the upstream URL, headers, body the proxy sends
 *   3. vi.resetModules() in afterEach
 *      → forces re-evaluation so each test gets a fresh API_URL
 */
import { describe, it, expect, vi, afterEach } from 'vitest';
import type { APIRoute } from 'astro';

const TEST_API = 'https://api.test.example.com';

/**
 * Load the proxy module fresh after stubbing SSR_API_URL.
 * vi.resetModules() must be called BEFORE this to bust the module cache.
 */
async function loadProxy(): Promise<{ ALL: APIRoute }> {
  return await import('../../src/pages/api/v1/[...path]');
}

/** Build a minimal APIRoute context from a Request. */
function ctx(request: Request): { request: Request } {
  return { request };
}

/**
 * Stub global fetch to return the given Response and
 * return a spy that records how it was called.
 */
function stubFetch(response: Response) {
  const fetchSpy = vi.fn().mockResolvedValue(response);
  vi.stubGlobal('fetch', fetchSpy);
  return fetchSpy;
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
  vi.resetModules();
});

describe('API proxy — REQ-PROXY', () => {
  // ── Slash preservation (bug-4 regression) ─────────────────────

  it('preserves trailing slash in upstream URL', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(new Response('{}', { status: 200 }));

    const request = new Request('http://localhost/api/v1/heroes/latest/');
    const response = await ALL(ctx(request) as any);

    expect(response.status).toBe(200);
    expect(fetchSpy).toHaveBeenCalledOnce();
    const [url] = fetchSpy.mock.calls[0];
    expect(url).toBe(`${TEST_API}/api/v1/heroes/latest/`);
  });

  it('does NOT add a trailing slash when the client omits it', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(new Response('{}', { status: 200 }));

    const request = new Request('http://localhost/api/v1/heroes/latest');
    await ALL(ctx(request) as any);

    const [url] = fetchSpy.mock.calls[0];
    expect(url).toBe(`${TEST_API}/api/v1/heroes/latest`);
  });

  // ── Query string preservation ─────────────────────────────────

  it('preserves query string in upstream URL', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(new Response('{}', { status: 200 }));

    const request = new Request('http://localhost/api/v1/heroes/latest/?page=2&limit=10');
    await ALL(ctx(request) as any);

    const [url] = fetchSpy.mock.calls[0];
    expect(url).toBe(`${TEST_API}/api/v1/heroes/latest/?page=2&limit=10`);
  });

  // ── Cookie forwarding ─────────────────────────────────────────

  it('forwards Cookie header to upstream', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(new Response('{}', { status: 200 }));

    const request = new Request('http://localhost/api/v1/heroes/latest/', {
      headers: { Cookie: 'session=abc; access_token=xyz' },
    });
    await ALL(ctx(request) as any);

    const [, options] = fetchSpy.mock.calls[0];
    expect(options.headers.cookie).toBe('session=abc; access_token=xyz');
  });

  it('omits cookie header when request has no cookies', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(new Response('{}', { status: 200 }));

    const request = new Request('http://localhost/api/v1/heroes/latest/');
    await ALL(ctx(request) as any);

    const [, options] = fetchSpy.mock.calls[0];
    expect(options.headers.cookie).toBeUndefined();
  });

  // ── Set-Cookie propagation ────────────────────────────────────

  it('propagates Set-Cookie from upstream to the client response', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const upstreamResponse = new Response('{}', { status: 200 });
    upstreamResponse.headers.set('set-cookie', 'new=value; Path=/');

    const fetchSpy = stubFetch(upstreamResponse);

    const request = new Request('http://localhost/api/v1/heroes/latest/');
    const response = await ALL(ctx(request) as any);

    const setCookieValues = response.headers.getSetCookie();
    expect(setCookieValues).toHaveLength(1);
    expect(setCookieValues[0]).toBe('new=value; Path=/');
  });

  // ── Status propagation (422/405) ──────────────────────────────

  it('propagates 422 status from upstream', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(
      new Response(JSON.stringify({ detail: 'Validation error' }), { status: 422 }),
    );

    const request = new Request('http://localhost/api/v1/heroes/latest/');
    const response = await ALL(ctx(request) as any);

    expect(response.status).toBe(422);
  });

  it('propagates 405 status from upstream', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(
      new Response(JSON.stringify({ detail: 'Method Not Allowed' }), { status: 405 }),
    );

    const request = new Request('http://localhost/api/v1/heroes/latest/');
    const response = await ALL(ctx(request) as any);

    expect(response.status).toBe(405);
  });

  // ── POST with body ────────────────────────────────────────────

  it('forwards POST method and body to upstream', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(new Response('{}', { status: 200 }));

    const payload = JSON.stringify({ title: 'Test Project' });
    const request = new Request('http://localhost/api/v1/projects/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload,
    });
    await ALL(ctx(request) as any);

    const [url, options] = fetchSpy.mock.calls[0];
    expect(url).toBe(`${TEST_API}/api/v1/projects/`);
    expect(options.method).toBe('POST');
    expect(options.headers['content-type']).toBe('application/json');

    // Body is forwarded as ArrayBuffer — decode and compare
    const bodyText = new TextDecoder().decode(options.body as ArrayBuffer);
    expect(bodyText).toBe(payload);
  });

  it('does NOT forward body for GET requests', async () => {
    vi.stubEnv('SSR_API_URL', TEST_API);
    vi.resetModules();
    const { ALL } = await loadProxy();

    const fetchSpy = stubFetch(new Response('{}', { status: 200 }));

    const request = new Request('http://localhost/api/v1/heroes/latest/');
    await ALL(ctx(request) as any);

    const [, options] = fetchSpy.mock.calls[0];
    expect(options.body).toBeUndefined();
  });
});
