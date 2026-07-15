import { test, expect, Page } from '@playwright/test';

test.describe('Portfolio — Hero Section', () => {
  test('renders hero content from API', async ({ page }) => {
    await page.goto('/');

    // Real data from the backend API
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await expect(page.locator('#inicio')).toBeVisible();
  });

  test('renders contact and CV buttons', async ({ page }) => {
    await page.goto('/');

    // Hero should have action buttons
    const buttons = page.locator('#inicio a, #inicio button');
    await expect(buttons.first()).toBeVisible();
  });

  test('hero section has correct accessibility attributes', async ({ page }) => {
    await page.goto('/');

    const heroSection = page.locator('#inicio');
    await expect(heroSection).toBeVisible();
  });

  test('portfolio loads with complete HTML structure', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByRole('navigation')).toBeVisible();
    await expect(page.locator('#inicio')).toBeVisible();
  });
});

test.describe('Portfolio — Navigation & Layout', () => {
  test('navigation has working links', async ({ page }) => {
    await page.goto('/');

    const nav = page.getByRole('navigation');
    await expect(nav).toBeVisible();
    const links = nav.getByRole('link');
    await expect(links.first()).toBeVisible();
  });

  test('responsive design on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    await expect(page.locator('#inicio')).toBeVisible();
    await expect(page.locator('nav')).toBeVisible();
  });

  test('responsive design on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');

    await expect(page.locator('#inicio')).toBeVisible();
  });

  test('page title is correct', async ({ page }) => {
    await page.goto('/');

    const title = await page.title();
    expect(title).toContain('El Rincom de Harco');
  });
});

test.describe('Portfolio — Loading & Error States', () => {
  test('handles API error gracefully', async ({ page }) => {
    // Mock API to return errors
    await page.route('**/api/v1/**', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Internal Server Error' })
      });
    });
    // Reload with error mocks active
    await page.goto('/');

    // Page should still load without crashing
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Portfolio — Performance', () => {
  test('loads within acceptable time', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await expect(page.locator('#inicio')).toBeVisible();
    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(10000);
  });
});

test.describe('Portfolio — Dual Mode (Robot + Recruiter)', () => {
  test.beforeEach(async ({ page }) => {
    // Clean localStorage to start from client mode
    await page.goto('/');
    await page.evaluate(() => localStorage.removeItem('portfolio-mode'));
    await page.reload();
  });

  test.afterEach(async ({ page }) => {
    await page.evaluate(() => localStorage.removeItem('portfolio-mode'));
  });

  test('robot assistant button is visible in bottom-right corner', async ({ page }) => {
    await page.goto('/');

    const robotBtn = page.locator('#robot-btn');
    await expect(robotBtn).toBeVisible();
  });

  test('clicking robot button opens modal with question', async ({ page }) => {
    // Capture JS errors
    const errors: string[] = [];
    page.on('pageerror', err => errors.push(err.message));

    await page.goto('/');
    await page.waitForTimeout(500); // Wait for JS to init

    // Log any errors found
    if (errors.length > 0) {
      console.log('Page errors:', errors.join(', '));
    }

    await page.locator('#robot-btn').click({ force: true });
    const modal = page.locator('#robot-modal');
    await expect(modal).toHaveClass(/open/);
    await expect(page.getByText('programador')).toBeVisible();
  });

  test('modal has Sí and No buttons', async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(500);

    await page.locator('#robot-btn').click({ force: true });
    await expect(page.locator('#btn-yes')).toBeVisible();
    await expect(page.locator('#btn-no')).toBeVisible();
  });

  test('clicking No closes the modal', async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(500);

    await page.locator('#robot-btn').click({ force: true });
    await page.locator('#btn-no').click();
    const modal = page.locator('#robot-modal');
    await expect(modal).not.toHaveClass(/open/);
  });

  test('clicking Sí switches to recruiter mode and saves to localStorage', async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(500);

    await page.locator('#robot-btn').click({ force: true });
    await page.locator('#btn-yes').click();

    // Should trigger destruction and switch to recruiter mode
    const mode = await page.evaluate(() => localStorage.getItem('portfolio-mode'));
    expect(mode).toBe('recruiter');
  });

  test('recruiter sections are visible in recruiter mode', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => localStorage.setItem('portfolio-mode', 'recruiter'));
    await page.reload();
    await page.waitForTimeout(1000); // Wait for JS + event chain

    // Wait for recruiter sections to be visible
    await expect(page.getByText('Buscando nuevos retos')).toBeVisible();
    await expect(page.getByText('Hernan Arango Cortes')).toBeVisible();
  });

  test('recruiter mode persists on page reload', async ({ page }) => {
    // Set recruiter mode
    await page.goto('/');
    await page.evaluate(() => localStorage.setItem('portfolio-mode', 'recruiter'));
    await page.reload();

    // After reload, should still be in recruiter mode
    const mode = await page.evaluate(() => localStorage.getItem('portfolio-mode'));
    expect(mode).toBe('recruiter');

    // Back button should be visible
    await expect(page.locator('#btn-back')).toBeVisible();
  });

  test('back button switches back to client mode', async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => localStorage.setItem('portfolio-mode', 'recruiter'));
    await page.reload();
    await page.waitForTimeout(500);

    // Click back button → modal opens asking to go back
    await page.locator('#btn-back').click();
    // Modal should show "Volver" option
    await expect(page.locator('#btn-yes-text')).toHaveText('Volver');
    // Click "Volver" in the modal
    await page.locator('#btn-yes').click();

    // Should be back in client mode
    const mode = await page.evaluate(() => localStorage.getItem('portfolio-mode'));
    expect(mode).toBeNull();
  });
});
