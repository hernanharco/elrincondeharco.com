# Componentes - elRincondeHarco.com

## 📁 Estructura

```
src/components/
├── ui/                              # Componentes UI compartidos
│   ├── ImageUpload.svelte           # Subida de imágenes a Cloudinary
│   ├── ProjectCard.astro            # Tarjeta de proyecto
│   └── ShowroomCard.svelte          # Tarjeta de showroom
├── layout/                          # Layout y navegación
│   ├── Navbar.astro                 # Navegación principal
│   ├── Footer.astro                 # Footer del sitio
│   └── AdminSidebar.svelte          # Sidebar del panel admin
├── sections/                        # Secciones de la landing page
│   ├── Hero.astro                   # Hero principal
│   ├── About.astro                  # Sobre mí
│   ├── Stack.astro                  # Stack tecnológico
│   ├── Projects.astro               # Proyectos
│   ├── Passions.astro               # Pasiones
│   ├── Stats.astro                  # Estadísticas
│   ├── Sectors.astro                # Sectores (rúbrica)
│   ├── SectorProjects.astro         # Unifica sectores + proyectos
│   ├── Testimonials.astro           # Testimonios
│   ├── ShowroomGrid.astro           # Grid de prototipos
│   ├── Contact.astro                # Contacto
│   ├── CTA.astro                    # Call to action
│   ├── Ecosystem.astro              # Ecosistema
│   ├── WorkProcess.astro            # Metodología de trabajo
│   ├── PrototypesSection.astro      # Sección de prototipos
│   └── recruiter/                   # Secciones modo recruiter
│       ├── RecruiterHero.astro
│       ├── RecruiterStack.astro
│       ├── RecruiterProjects.astro
│       ├── RecruiterTimeline.astro
│       ├── RecruiterCertifications.astro
│       ├── RecruiterInfra.astro
│       ├── RecruiterMethod.astro
│       ├── RecruiterLocation.astro
│       ├── RecruiterGitHub.astro
│       └── RecruiterAdmin.astro
├── effects/                         # Efectos visuales 3D y animaciones
│   ├── CaosOrden.astro              # Escena Three.js Caos → Orden
│   ├── Hero3DBackground.astro       # Background 3D del hero
│   ├── DestructionEffect.astro      # Efecto destrucción (Thanos Snap)
│   ├── Robot3D.astro                # Mascota 3D interactiva
│   ├── RobotAssistant.astro         # Asistente flotante modo recruiter
│   ├── SmoothScroll.astro           # Lenis + GSAP ScrollTrigger
│   └── TiltCard.astro               # Efecto tilt en tarjetas
├── auth/                            # Autenticación
│   ├── AuthGuard.svelte             # Guard de rutas protegidas
│   └── LoginForm.svelte             # Formulario de login
└── admin/                           # Paneles del admin (CRUD)
    ├── DashboardCards.svelte        # Cards del dashboard
    ├── HeroEditor.svelte
    ├── AboutEditor.svelte
    ├── StackEditor.svelte
    ├── ProjectsEditor.svelte
    ├── SectorEditor.svelte
    ├── TestimonialEditor.svelte
    ├── ShowroomEditor.svelte
    ├── FooterEditor.svelte
    ├── PassionsEditor.svelte
    └── SiteSettingsEditor.svelte
```

## 📝 Guías por tipo de componente

### Astro (`.astro`)
- **Usar para**: secciones estáticas o con poca interactividad, layouts, efectos 3D
- El frontmatter (`---`) es para lógica server-side
- Las variables públicas van con `Astro.props`
- El `<script>` es client-side, con `// @ts-nocheck` si hay Three.js/GSAP
- Preferir `client:load` solo cuando sea necesario; `client:visible` para lazy loading

### Svelte 5 (`.svelte`)
- **Usar para**: componentes interactivos, forms, admin panels
- Usar `$state()` para variables reactivas
- Usar `$derived()` para valores computados
- Usar `$effect()` para side effects
- Usar `onclick` (no `on:click`)
- Usar `$props()` en vez de `export let`

### Svelte 4 legacy (`.svelte` con `runes={false}`)
- Componentes del admin aún no migrados a Svelte 5
- Usan `export let` y `on:click`
- Migración pendiente: `AdminSidebar`, `AuthGuard`, `LoginForm`, `ShowroomCard`, y todos los `*Editor.svelte`

## 🎯 Convenciones

- **PascalCase** para nombres de componentes
- Nombres descriptivos y agrupados por dominio
- Imports: primero librerías externas, luego internas
- Los efectos 3D llevan `// @ts-nocheck` por tipos implícitos de Three.js/GSAP
- Los componentes públicos cargan datos con fetch SSR + fallback local
