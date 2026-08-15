import { describe, it, expect } from 'vitest';
import { DASHBOARD_ENDPOINTS } from '$lib/dashboard';

describe('DASHBOARD_ENDPOINTS', () => {
  it('exports exactly 8 canonical endpoint URLs', () => {
    expect(DASHBOARD_ENDPOINTS).toHaveLength(8);
  });

  it('includes all 8 dashboard section endpoints', () => {
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/projects/');
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/sectors/');
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/testimonials/all');
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/showrooms/');
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/stacks/');
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/heroes/latest/');
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/abouts/latest/');
    expect(DASHBOARD_ENDPOINTS).toContain('/api/v1/experience/latest/');
  });

  it('uses canonical /testimonials/all without trailing slash (bug-1 regression)', () => {
    const testimonialsEndpoint = DASHBOARD_ENDPOINTS.find((e) =>
      e.includes('testimonials')
    );
    expect(testimonialsEndpoint).toBe('/api/v1/testimonials/all');
    expect(testimonialsEndpoint).not.toMatch(/\/$/);
  });

  it('exports readonly string array', () => {
    for (const endpoint of DASHBOARD_ENDPOINTS) {
      expect(typeof endpoint).toBe('string');
      expect(endpoint.startsWith('/api/v1/')).toBe(true);
    }
  });
});
