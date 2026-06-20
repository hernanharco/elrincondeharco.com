# Skill Registry — elrincondeharco.com

## Project Conventions

### Conventions Index
| File | Description |
|------|-------------|
| `.windsurf/frontend.md` | Frontend architecture, component patterns, styling conventions |
| `.windsurf/backend.md` | Backend architecture, API patterns, testing conventions |
| `.windsurf/docker.md` | Docker setup and workflow |
| `.windsurf/rules.md` | General coding rules and guidelines |
| `.windsurf/claude.md` | Agent instructions and persona |

### Note
Project convention files exist under `.windsurf/` directory. Consider migrating relevant conventions to project-level `AGENTS.md` or `.cursorrules` for broader tool compatibility.

## Available Skills

### Framework & Runtime
| Skill | Trigger | Description |
|-------|---------|-------------|
| **astroship** | Astro, Svelte, projects, portfolio | Astro + Svelte starter for portfolio projects |
| **nextjs-15** | Next.js, App Router, Server Actions | Next.js 15 App Router patterns |
| **react-19** | React components, JSX | React 19 with React Compiler (no useMemo/useCallback) |
| **angular-core** | Angular components, signals | Angular core patterns (standalone, signals, inject) |
| **angular-architecture** | Angular structure | Angular project structure and file naming |
| **angular-forms** | Angular forms | Signal Forms and Reactive Forms |
| **angular-performance** | Angular optimization | NgOptimizedImage, @defer, lazy loading |

### Backend
| Skill | Trigger | Description |
|-------|---------|-------------|
| **django-drf** | Django REST APIs | ViewSets, Serializers, Filters |

### Testing
| Skill | Trigger | Description |
|-------|---------|-------------|
| **go-testing** | Go tests, Bubbletea TUI | Go testing with teatest |
| **playwright** | E2E tests | Playwright Page Objects, selectors |
| **pytest** | Python tests | Fixtures, mocking, markers |

### State & Validation
| Skill | Trigger | Description |
|-------|---------|-------------|
| **zustand-5** | React state management | Zustand 5 store patterns |
| **zod-4** | Schema validation | Zod 4 validation (breaking changes from v3) |

### Styling
| Skill | Trigger | Description |
|-------|---------|-------------|
| **tailwind-4** | Tailwind CSS | Tailwind 4 patterns, cn(), theme variables |

### SDD Workflow
| Skill | Trigger | Description |
|-------|---------|-------------|
| **sdd-init** | SDD initialization | Bootstrap SDD in a project |
| **sdd-explore** | Codebase analysis | Investigate and think through features |
| **sdd-propose** | Feature proposals | Create change proposals |
| **sdd-spec** | Requirements | Write specifications with scenarios |
| **sdd-design** | Architecture design | Technical design documents |
| **sdd-tasks** | Task breakdown | Implementation task checklists |
| **sdd-apply** | Implementation | Write code from tasks |
| **sdd-verify** | Validation | Verify implementation against specs |
| **sdd-archive** | Closure | Archive completed changes |
| **sdd-onboard** | Walkthrough | Guided SDD workflow walkthrough |

### Tools
| Skill | Trigger | Description |
|-------|---------|-------------|
| **skill-creator** | New skills | Create new AI agent skills |
| **skill-registry** | Update registry | Create/update skill registry |
| **judgment-day** | Code review | Parallel adversarial code review |
| **branch-pr** | Pull requests | PR creation workflow |
| **github-pr** | GitHub PRs | High-quality PRs with conventional commits |
| **issue-creation** | GitHub issues | Issue creation workflow |
| **jira-epic** | Jira epics | Jira epic creation |
| **jira-task** | Jira tasks | Jira task creation |
| **ai-sdk-5** | AI chat features | Vercel AI SDK 5 patterns |
| **customize-opencode** | OpenCode config | Edit opencode configuration |
| **typescript** | TypeScript code | TypeScript strict patterns |

## Auto-Load Rules

The following skills auto-load based on context detection:

- `go-testing`: Go tests, Bubbletea TUI testing → load when Go test files detected
- `skill-creator`: Creating new AI skills → load when task involves skill creation
