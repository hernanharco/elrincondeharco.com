# Skill Registry — elrincondeharco.com

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

See `_shared/skill-resolver.md` for the full resolution protocol.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| Astro components, pages, Three.js effects, GSAP, progressive enhancement | astro | `~/.config/opencode/skills/astro/SKILL.md` |
| Three.js + GSAP + ScrollTrigger + Lenis for immersive 3D | immersive-3d-web | `~/.config/opencode/skills/immersive-3d-web/SKILL.md` |
| TypeScript - types, interfaces, generics | typescript | `~/.config/opencode/skills/typescript/SKILL.md` |
| Tailwind CSS - cn(), theme variables, no var() | tailwind-4 | `~/.config/opencode/skills/tailwind-4/SKILL.md` |
| React 19 - no useMemo/useCallback | react-19 | `~/.config/opencode/skills/react-19/SKILL.md` |
| Next.js 15 routing, Server Actions, data fetching | nextjs-15 | `~/.config/opencode/skills/nextjs-15/SKILL.md` |
| Zustand 5 state management | zustand-5 | `~/.config/opencode/skills/zustand-5/SKILL.md` |
| Zod 4 validation - breaking changes from v3 | zod-4 | `~/.config/opencode/skills/zod-4/SKILL.md` |
| Django REST Framework - ViewSets, Serializers | django-drf | `~/.config/opencode/skills/django-drf/SKILL.md` |
| Pytest - fixtures, mocking, markers | pytest | `~/.config/opencode/skills/pytest/SKILL.md` |
| Go tests, Bubbletea TUI testing | go-testing | `~/.config/opencode/skills/go-testing/SKILL.md` |
| Playwright E2E - Page Objects, selectors | playwright | `~/.config/opencode/skills/playwright/SKILL.md` |
| Vercel AI SDK 5 - breaking changes from v4 | ai-sdk-5 | `~/.config/opencode/skills/ai-sdk-5/SKILL.md` |
| Create new AI agent skills | skill-creator | `~/.config/opencode/skills/skill-creator/SKILL.md` |
| PR creation - issue-first enforcement | branch-pr | `~/.config/opencode/skills/branch-pr/SKILL.md` |
| GitHub PRs - conventional commits | github-pr | `~/.config/opencode/skills/github-pr/SKILL.md` |
| GitHub issue creation | issue-creation | `~/.config/opencode/skills/issue-creation/SKILL.md` |
| Jira epics for large features | jira-epic | `~/.config/opencode/skills/jira-epic/SKILL.md` |
| Jira tasks/tickets | jira-task | `~/.config/opencode/skills/jira-task/SKILL.md` |
| Parallel adversarial code review | judgment-day | `~/.config/opencode/skills/judgment-day/SKILL.md` |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### astro
- Progressive enhancement: 0 JS by default, add client:visible directives only for interactive islands
- Islands architecture: Svelte/React components as islands, NOT page-level frameworks
- SEO: export `metadata` object from layouts/pages, avoid `<head>` manipulation
- Three.js/GSAP: lazy-load via dynamic import inside `client:visible` or `client:load` islands
- No default slot assumed — always use named slots or explicit children props
- Content collections: use `defineCollection` with Zod schemas, query with `getCollection()`

### immersive-3d-web
- Lenis MUST be set up FIRST before any scroll-driven effects
- Three.js canvas: position fixed, z-index 0, pointer-events none
- GSAP ScrollTrigger + Three.js: use `onUpdate` callback, NOT scroll events
- Breakout-frame: elements overflow viewport with `transform-style: preserve-3d` + perspective on parent
- Mobile: cap `pixelRatio` at 1.5, use `renderer.setSize` with devicePixelRatio, add fog for performance
- Camera travel: define waypoints as Vector3 array, tween camera.position + lookAt in parallel

### typescript
- ALWAYS use `as const` objects with extracted types, NEVER raw union strings
- Use flat interfaces (extends), NOT intersection types (`&`)
- Prefer `interface` over `type` for object shapes (better errors, extends, declaration merging)
- Use `satisfies` operator for type validation without widening
- `any` is banned — use `unknown` with type guards
- Strict mode required: `strict: true` in tsconfig

### tailwind-4
- NEVER use `var()` in className — use inline `style` prop with CSS var constants
- Dynamic values → `style={{ width: \`${x}%\` }}`
- Conditional styles → `cn("base", condition && "variant")`
- Static only → plain `className=""` (no cn())
- Theme: use `@theme` directive in CSS, NOT `tailwind.config.js`

### react-19
- No useMemo/useCallback — React Compiler handles memoization
- `use()` hook for promises/context, replaces useEffect for data fetching
- Server Components by default, add 'use client' only for interactivity/hooks
- `ref` is a regular prop — no forwardRef wrapper needed
- Actions: useActionState for form mutations, useOptimistic for optimistic UI

### nextjs-15
- App Router only — no pages/ directory
- All components are Server Components by default
- Data fetching: use Server Components with async/await, NOT useEffect
- Mutations: use Server Actions with `"use server"` directive
- Dynamic routes: `params` is a Promise — must `await` it
- Caching: `fetch()` is cached by default, use `noStore()` or `cache: 'no-store'` to opt out

### zustand-5
- Store: `create<StoreType>()((set, get) => ({...}))` — single store per domain
- Actions mutate state immutably via `set()`, derived values via `get()`
- Subscribe: `useStore(state => state.part)` for granular re-renders
- Persist middleware: `persist(storageKey)` for persisted state
- NO Redux-style reducers — Zustand is NOT Redux

### zod-4
- BREAKING: `z.string().email()` → `z.email()`, `z.string().url()` → `z.url()`
- BREAKING: `.nonempty()` removed — use `.min(1)`
- BREAKING: `.required_error()` on object → second arg `{ error: "msg" }`
- `z.infer<typeof schema>` for TypeScript type extraction
- Use `.pipe()` for transformations instead of `.transform().refine()`

### django-drf
- ViewSets with `queryset` + `serializer_class` + `permission_classes` at minimum
- Override `get_serializer_class()` for per-action serializers
- Use `django-filter` with `filterset_class` for search/filtering
- `@action(detail=True/False)` for custom endpoints
- Serializer validation: `validate_<field>()` methods, NOT `clean_<field>()`

### pytest
- Fixtures over setup functions — use `@pytest.fixture` with explicit scope
- `conftest.py` for shared fixtures, test modules for focused ones
- Parametrize: `@pytest.mark.parametrize` for multiple input cases
- Async: use `pytest-asyncio` with `async def test_*` and `await`
- Markers: `@pytest.mark.slow`, `@pytest.mark.integration` for filtering
- Coverage: `--cov=app --cov-fail-under=80` enforced

### go-testing
- Table-driven tests: `[]struct{name, input, expected}` + `t.Run(name, fn)`
- Bubbletea: use `teatest.NewModel()` with timeouts for TUI testing
- Golden files: `testdata/*.golden` with `flag.Update()` for updates
- Subtests: always use `t.Run()` for parallel execution
- Cleanup: `t.Cleanup()` instead of defer in test helpers

### playwright
- ALWAYS use MCP tools first (navigate + snapshot + interact) before writing tests
- Page Objects pattern: encapsulate selectors and actions in page classes
- Selectors: prefer `getByRole`, `getByLabel`, `getByText` over CSS/XPath
- Assertions: use `await expect(page.locator).toBeVisible()` with auto-wait
- Screenshots: take before/after for visual regression documentation

### ai-sdk-5
- BREAKING: `useChat` from `"@ai-sdk/react"`, NOT `"ai"`
- BREAKING: `transport: new DefaultChatTransport({api})` instead of bare `api`
- BREAKING: `handleSubmit`/`handleInputChange` → `sendMessage`
- `streamText` from `"ai"` for server-side streaming
- Tool calls: use `tools` parameter with Zod schemas for type-safe tools

### skill-creator
- Structure: frontmatter (name, description, trigger) → When to Use → Critical Patterns → Rules
- Frontmatter: `allowed-tools` field to restrict tool access
- Critical Patterns: code-first, show patterns not explanations, use ✅/❌ for correct/wrong
- Rules: bullet-point constraints, one rule per line, prefixed with REQUIRED/ALWAYS/NEVER
- Skills live in `~/.config/opencode/skills/<name>/SKILL.md`

### branch-pr
- Every PR MUST link an approved issue — no exceptions
- Every PR MUST have exactly one `type:*` label
- Branch convention: `<type>/<issue-number>-<description>`
- Automated checks must pass before merge
- Blank PRs without issue linkage are blocked by CI

### github-pr
- PR title = conventional commit: `feat|fix|docs|refactor|test|chore(<scope>): description`
- Description template: what/why/how + screenshots + testing notes
- Use `gh pr create` with `--title`, `--body`, `--base` flags
- Keep PRs small and focused — one feature/fix per PR
- Request reviewers via `gh pr edit --add-reviewer`

### issue-creation
- Blank issues disabled — MUST use template (bug report or feature request)
- New issues get `status:needs-review` automatically
- Maintainer MUST add `status:approved` before any PR
- Questions go to Discussions, not issues
- Bug template: steps to reproduce, expected vs actual, environment

### judgment-day
- Launches 2 independent blind judge sub-agents simultaneously
- Judges review independently, then orchestrator synthesizes findings
- Fixes applied → re-judge cycle (max 2 iterations)
- If both pass → done; if not → escalate to orchestrator
- Pre-review: load skill registry, identify target scope

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| Frontend conventions | `.windsurf/frontend.md` | Astro + Svelte 5 components, layouts, routing |
| Backend conventions | `.windsurf/backend.md` | FastAPI models, API endpoints, DB patterns |
| Docker setup | `.windsurf/docker.md` | Docker compose and deployment |
| General rules | `.windsurf/rules.md` | Coding guidelines and best practices |
| Agent instructions | `.windsurf/claude.md` | AI persona and behavior |
| Test backend | `.windsurf/test-backend.md` | Backend test conventions |
| Test frontend | `.windsurf/test-frontend.md` | Frontend test conventions |
| Scripts | `.windsurf/scripts.md` | Dev/utility scripts |
