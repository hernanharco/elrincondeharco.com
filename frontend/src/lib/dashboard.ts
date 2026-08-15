/**
 * dashboard.ts — Canonical endpoint URLs for the admin dashboard.
 *
 * Extracted from DashboardCards.svelte (REQ-TS-EXTRACTION).
 * These are the 8 endpoints fetched on dashboard load.
 * Note: /testimonials/all has NO trailing slash (bug-1: /all/ triggers 307 → mixed content).
 */
export const DASHBOARD_ENDPOINTS = [
  '/api/v1/projects/',
  '/api/v1/sectors/',
  '/api/v1/testimonials/all',
  '/api/v1/showrooms/',
  '/api/v1/stacks/',
  '/api/v1/heroes/latest/',
  '/api/v1/abouts/latest/',
  '/api/v1/experience/latest/',
] as const;
