/**
 * fetch-interceptor.ts — Pure credentials interceptor for fetch.
 *
 * Extracted from AdminLayout.astro inline <script> (REQ-TS-EXTRACTION).
 *
 * The admin panel (www.rincom.es) and the API (api.elrincondeharco.com) are
 * cross-origin. Raw fetch() calls in editors (PUT/POST/DELETE) omitted
 * credentials: 'include', so the httpOnly access_token cookie never traveled
 * and the backend responded 401.
 *
 * This module provides:
 * - shouldAddCredentials: pure predicate (testable without DOM)
 * - installCredentialsInterceptor: patches window.fetch to inject credentials
 *   for API-targeted calls that don't already specify them.
 */

/**
 * Resolve a RequestInfo | URL input to a string URL.
 */
function resolveUrl(input: RequestInfo | URL): string {
  if (typeof input === 'string') return input;
  if (input instanceof URL) return input.toString();
  return input.url;
}

/**
 * Pure predicate: should the interceptor add credentials: 'include'?
 *
 * Returns true when ALL of these hold:
 * 1. init.credentials is undefined (not already set by caller)
 * 2. apiBase is non-empty
 * 3. The resolved URL starts with apiBase (targets the API)
 */
export function shouldAddCredentials(
  input: RequestInfo | URL,
  init: RequestInit | undefined,
  apiBase: string,
): boolean {
  if (init?.credentials !== undefined) return false;
  if (!apiBase) return false;
  const url = resolveUrl(input);
  return url.startsWith(apiBase);
}

/**
 * Install a credentials interceptor on window.fetch.
 * Returns an uninstall function that restores the original fetch.
 */
export function installCredentialsInterceptor(apiBase: string): () => void {
  const originalFetch = window.fetch.bind(window);

  window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
    if (shouldAddCredentials(input, init, apiBase)) {
      init = { ...init, credentials: 'include' };
    }
    return originalFetch(input, init);
  };

  return () => {
    window.fetch = originalFetch;
  };
}
