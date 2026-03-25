# Frontend Testing

This directory contains comprehensive tests for the Astro + Svelte 5 frontend.

## 📁 Test Structure

```
tests/
├── setup.ts                    # Test setup and global mocks
├── components/
│   ├── sections/               # Section component tests
│   │   ├── Hero.test.ts
│   │   ├── About.test.ts
│   │   ├── Stack.test.ts
│   │   ├── Projects.test.ts
│   │   └── Passions.test.ts
│   ├── ui/                     # UI component tests
│   │   └── ImageUpload.test.ts
│   └── layout/                 # Layout component tests
│       ├── Navbar.test.ts
│       └── Footer.test.ts
├── lib/                        # Library function tests
│   ├── config.test.ts
│   ├── types.test.ts
│   └── dataEvents.test.ts
├── integration/                # Integration tests
│   ├── hero-flow.test.ts
│   ├── navigation.test.ts
│   └── api-integration.test.ts
└── e2e/                       # End-to-end tests
    └── portfolio.spec.ts
```

## 🧪 Test Types

### Unit Tests
- **Components**: Test Svelte components in isolation
- **Libraries**: Test utility functions and API calls
- **Types**: Test TypeScript interfaces and validation

### Integration Tests
- **Component Flow**: Test data flow between components
- **API Integration**: Test frontend-backend communication
- **User Interactions**: Test complete user workflows

### E2E Tests
- **Full Portfolio**: Test complete user journey
- **Responsive Design**: Test across device sizes
- **Performance**: Test loading and interactions

## 🚀 Running Tests

### Quick Start
```bash
# Install dependencies
pnpm install

# Run all tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with coverage
pnpm test:coverage

# Run tests with UI
pnpm test:ui

# Run E2E tests
pnpm test:e2e

# Run E2E tests with UI
pnpm test:e2e:ui
```

### Specific Test Commands
```bash
# Run specific test file
pnpm test Hero.test.ts

# Run tests by pattern
pnpm test --grep "Hero"

# Run integration tests only
pnpm test integration/

# Run component tests only
pnpm test components/
```

## 📊 Coverage

Tests generate coverage reports:
- Terminal output: Coverage summary
- HTML report: `coverage/index.html`
- JSON report: `coverage/coverage-final.json`

Target: 80% coverage minimum

## 🔧 Configuration

### Vitest Configuration
- Environment: jsdom
- Coverage: Text + HTML + JSON
- Setup file: `tests/setup.ts`
- Global mocks: fetch, environment variables

### Playwright Configuration
- Browsers: Chromium, Firefox, Safari
- Viewport: Responsive testing
- Timeout: 30 seconds default

## 📝 Test Examples

### Component Test
```typescript
import { render, screen } from '@testing-library/svelte';
import Hero from '$lib/components/sections/Hero.svelte';

test('Hero component renders correctly', async () => {
  render(Hero);
  
  expect(screen.getByRole('heading')).toBeInTheDocument();
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
```

### API Test
```typescript
import { fetchApi } from '$lib/config';
import { mockApiResponse } from '../setup';

test('fetchApi handles successful responses', async () => {
  const mockData = { id: 1, title: 'Test' };
  mockApiResponse(mockData);
  
  const result = await fetchApi('/api/test');
  expect(result).toEqual(mockData);
});
```

### Integration Test
```typescript
test('Hero section loads data from API', async () => {
  const mockData = { title: 'Test Hero', subtitle: 'Test Subtitle' };
  mockApiResponse(mockData);
  
  render(Hero);
  
  await waitFor(() => {
    expect(screen.getByText('Test Hero')).toBeInTheDocument();
  });
});
```

### E2E Test
```typescript
import { test, expect } from '@playwright/test';

test('Portfolio loads completely', async ({ page }) => {
  await page.goto('/');
  
  await expect(page.getByRole('heading', { name: 'elRincondelHarco.com' })).toBeVisible();
  await expect(page.getByText('Projects')).toBeVisible();
  await expect(page.getByText('Technologies')).toBeVisible();
});
```

## 🎯 Best Practices

1. **Isolation**: Each test should be independent
2. **Mocking**: Mock external dependencies (API, environment)
3. **Assertions**: Be specific with assertions
4. **Cleanup**: Clean up after each test
5. **Accessibility**: Test ARIA labels and roles

## 🐛 Debugging

```bash
# Run tests with debugging
pnpm test --no-coverage --reporter=verbose

# Run specific test with debugging
pnpm test Hero.test.ts --no-coverage

# Playwright debugging
pnpm test:e2e --debug

# Generate HTML report
pnpm test:coverage && open coverage/index.html
```
