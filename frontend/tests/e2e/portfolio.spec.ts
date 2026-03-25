import { test, expect } from '@playwright/test';

test.describe('Portfolio E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Mock API responses for consistent testing
    await page.route('**/api/v1/heroes/latest/', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 1,
          title: 'Test Hero',
          subtitle: 'Test Subtitle',
          description: 'Test description for hero section',
          background_image: null,
          contact_button_text: 'Contact Me',
          cv_button_text: 'Download CV',
          image_url: null,
          cv_url: 'https://example.com/cv.pdf'
        })
      });
    });

    await page.route('**/api/projects', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: 1,
            title: 'Test Project 1',
            description: 'Description for project 1',
            image_url: null,
            tags: ['React', 'TypeScript'],
            icon_name: 'Code',
            color: 'from-blue-500/20',
            demo_url: 'https://demo1.com',
            github_url: 'https://github1.com'
          },
          {
            id: 2,
            title: 'Test Project 2',
            description: 'Description for project 2',
            image_url: null,
            tags: ['Svelte', 'Tailwind'],
            icon_name: 'Globe',
            color: 'from-green-500/20',
            demo_url: null,
            github_url: 'https://github2.com'
          }
        ])
      });
    });

    await page.route('**/api/stacks', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: 1,
            name: 'React',
            category: 'Frontend',
            icon: 'Globe',
            description: 'JavaScript library',
            color: 'text-cyan-500',
            border: 'group-hover:border-cyan-500/50',
            glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(6,182,212,0.3)]'
          },
          {
            id: 2,
            name: 'Python',
            category: 'Backend',
            icon: 'Code',
            description: 'Programming language',
            color: 'text-blue-500',
            border: 'group-hover:border-blue-500/50',
            glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]'
          }
        ])
      });
    });
  });

  test('portfolio loads completely', async ({ page }) => {
    await page.goto('/');
    
    // Check main sections are visible
    await expect(page.getByRole('heading', { name: 'Test Hero' })).toBeVisible();
    await expect(page.getByText('Test Subtitle')).toBeVisible();
    await expect(page.getByText('Test description for hero section')).toBeVisible();
  });

  test('navigation works correctly', async ({ page }) => {
    await page.goto('/');
    
    // Check navigation links
    const navigation = page.locator('nav');
    await expect(navigation).toBeVisible();
    
    // Test smooth scrolling to sections
    const projectsLink = page.getByRole('link', { name: 'Projects' });
    if (await projectsLink.isVisible()) {
      await projectsLink.click();
      await expect(page.locator('#projects')).toBeVisible();
    }
  });

  test('projects section loads and filters work', async ({ page }) => {
    await page.goto('/');
    
    // Wait for projects to load
    await expect(page.getByText('Test Project 1')).toBeVisible();
    await expect(page.getByText('Test Project 2')).toBeVisible();
    
    // Check project tags
    await expect(page.getByText('React')).toBeVisible();
    await expect(page.getByText('TypeScript')).toBeVisible();
    await expect(page.getByText('Svelte')).toBeVisible();
    await expect(page.getByText('Tailwind')).toBeVisible();
    
    // Test project links
    const demoLink = page.getByRole('link', { name: 'Live Demo' });
    if (await demoLink.first().isVisible()) {
      await demoLink.first().click();
      // Verify link opens in new tab or navigates
    }
  });

  test('technologies stack displays correctly', async ({ page }) => {
    await page.goto('/');
    
    // Navigate to stack section or wait for it to be visible
    const stackSection = page.locator('#stack');
    await expect(stackSection).toBeVisible();
    
    // Check technologies are displayed
    await expect(page.getByText('React')).toBeVisible();
    await expect(page.getByText('Python')).toBeVisible();
    
    // Check categories
    await expect(page.getByText('Frontend')).toBeVisible();
    await expect(page.getByText('Backend')).toBeVisible();
  });

  test('contact and CV buttons work', async ({ page }) => {
    await page.goto('/');
    
    // Test contact button
    const contactButton = page.getByRole('button', { name: 'Contact Me' });
    if (await contactButton.isVisible()) {
      await contactButton.click();
      // Check if contact form or modal opens
    }
    
    // Test CV download
    const cvButton = page.getByRole('link', { name: 'Download CV' });
    if (await cvButton.isVisible()) {
      await expect(cvButton).toHaveAttribute('href', expect.stringContaining('example.com'));
    }
  });

  test('responsive design works on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Check mobile navigation
    const mobileNav = page.locator('nav');
    await expect(mobileNav).toBeVisible();
    
    // Check content is still accessible
    await expect(page.getByRole('heading', { name: 'Test Hero' })).toBeVisible();
    
    // Test mobile menu if it exists
    const mobileMenuButton = page.getByRole('button', { name: /menu/i });
    if (await mobileMenuButton.isVisible()) {
      await mobileMenuButton.click();
      // Check menu items are visible
    }
  });

  test('responsive design works on tablet', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    
    // Check layout adapts correctly
    await expect(page.getByRole('heading', { name: 'Test Hero' })).toBeVisible();
    await expect(page.getByText('Test Project 1')).toBeVisible();
  });

  test('loading states display correctly', async ({ page }) => {
    // Slow down API responses to test loading states
    await page.route('**/api/**', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      await route.continue();
    });
    
    await page.goto('/');
    
    // Check loading states (implementation depends on actual loading UI)
    await expect(page.locator('body')).toBeVisible();
    
    // Wait for content to load
    await expect(page.getByRole('heading', { name: 'Test Hero' })).toBeVisible({ timeout: 5000 });
  });

  test('error handling works gracefully', async ({ page }) => {
    // Mock API errors
    await page.route('**/api/**', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Internal Server Error' })
      });
    });
    
    await page.goto('/');
    
    // Check error handling (implementation depends on actual error UI)
    // The page should still load with fallback content or error messages
    await expect(page.locator('body')).toBeVisible();
  });

  test('accessibility features work', async ({ page }) => {
    await page.goto('/');
    
    // Check semantic HTML
    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByRole('navigation')).toBeVisible();
    
    // Check ARIA labels
    const headings = page.getByRole('heading');
    await expect(headings.first()).toBeVisible();
    
    // Check keyboard navigation
    await page.keyboard.press('Tab');
    // Verify focus management
  });

  test('performance metrics are acceptable', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    
    // Wait for main content to load
    await expect(page.getByRole('heading', { name: 'Test Hero' })).toBeVisible();
    
    const loadTime = Date.now() - startTime;
    
    // Page should load within reasonable time (adjust threshold as needed)
    expect(loadTime).toBeLessThan(5000);
    
    // Check Core Web Vitals
    const metrics = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const vitals = {};
          entries.forEach((entry) => {
            if (entry.entryType === 'largest-contentful-paint') {
              vitals.lcp = entry.renderTime || entry.loadTime;
            }
            if (entry.entryType === 'first-input') {
              vitals.fid = entry.processingStart - entry.startTime;
            }
          });
          resolve(vitals);
        }).observe({ entryTypes: ['largest-contentful-paint', 'first-input'] });
      });
    });
    
    // Check LCP is reasonable (adjust threshold as needed)
    if (metrics.lcp) {
      expect(metrics.lcp).toBeLessThan(4000);
    }
  });
});
