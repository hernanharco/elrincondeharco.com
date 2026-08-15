import { test, expect } from '@playwright/test';

/**
 * Drop-guard e2e — verifies that dropping a file on the ProjectsEditor
 * does NOT navigate to file:// (bug-2 regression).
 *
 * WHY SKIPPED:
 * The admin requires OAuth authentication against a live backend (:8001).
 * Automating the OAuth flow is not feasible in CI without test credentials.
 *
 * RELIABLE COVERAGE (already in place):
 * - uploads.test.ts: collectDroppedImageFiles filters image/* (6 tests)
 * - ProjectsEditor.svelte: on:drop|preventDefault calls handleDrop()
 *   which calls e.preventDefault() + collectDroppedImageFiles()
 *
 * TO ENABLE: provide a test admin account or mock OAuth at the Playwright level.
 */
test.describe('CRM — Admin Projects drop guard', () => {
  test.skip('dropping an image on the editor does NOT navigate to file://', async ({ page }) => {
    // Precondition: authenticated session on /admin/projects
    await page.goto('/admin/projects');

    const urlBeforeDrop = page.url();

    // The drop zone is the <label> with on:drop={handleDrop}
    const dropZone = page.locator('label:has(input[type="file"])');
    await dropZone.dispatchEvent('drop', {
      dataTransfer: { files: [], types: [] },
    });

    // URL must not change to file:// — preventDefault worked
    expect(page.url()).toBe(urlBeforeDrop);
    expect(page.url()).not.toMatch(/^file:\/\//);
  });
});
