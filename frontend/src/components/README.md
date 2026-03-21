# Components Organization

## 📁 Structure

```
src/components/
├── README.md                    # This file
├── ui/                          # Shared/UI Components
│   ├── ImageUpload.svelte      # Reusable image upload
│   ├── LoadingSpinner.svelte   # Loading states
│   └── Button.svelte           # Custom button component
├── layout/                      # Layout Components
│   ├── Navbar.svelte
│   ├── Footer.svelte
│   └── AdminSidebar.svelte
├── sections/                    # Page Sections
│   ├── Hero.svelte
│   ├── About.svelte
│   ├── Stack.svelte
│   ├── Projects.svelte
│   └── Passions.svelte
└── admin/                       # Admin Components
    ├── AboutEditor.svelte
    ├── HeroEditor.svelte
    ├── StackEditor.svelte
    ├── ProjectsEditor.svelte
    ├── FooterEditor.svelte
    ├── PassionsEditor.svelte
    ├── SiteSettingsEditor.svelte
    └── DashboardCards.svelte
```

## 📝 Component Guidelines

### Svelte 5 Requirements
- Use `$state()` for reactive variables
- Use `$derived()` for computed values
- Use `$effect()` for side effects
- Use `onevent` syntax (not `on:event`)
- Use `$props()` instead of `export let`

### Accessibility
- All labels must have `for` attribute
- All inputs must have corresponding `id`
- Use semantic HTML elements

### Naming Conventions
- Use PascalCase for component names
- Use descriptive names
- Group related components together

### Import Organization
1. External libraries first
2. Internal/lib imports second
3. Component imports last
