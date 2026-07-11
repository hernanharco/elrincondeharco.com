/**
 * ──────────────────────────────────────────────────────────────
 * fallback-data.ts — Datos de respaldo para el Frontend
 * ──────────────────────────────────────────────────────────────
 * Estos datos se muestran cuando la API del backend no responde.
 * Son un snapshot de la base de datos al momento de generar este archivo.
 * 
 * Estrategia:
 *   1. Mientras carga → Skeleton
 *   2. API responde ok → Datos reales
 *   3. API falla → Fallback (NUNCA skeleton vacío)
 * ──────────────────────────────────────────────────────────────
 */

import type {
  HeroResponse,
  AboutResponse,
  StackResponse,
  ProjectResponse,
  PassionResponse,
  FooterResponse,
  SiteSettingsResponse,
  ShowroomResponse,
  SectorResponse,
} from '$lib/types';

// ────────────────────────────────────
// HERO
// ────────────────────────────────────
export const fallbackHero: HeroResponse = {
  id: 3,
  title: 'Soluciones Digitales para tu Negocio',
  subtitle: 'El <span class="text-amber-400">Rincom</span><br /><span class="text-cyan-400">de Harco</span>',
  description:
    'Creo la web que tu negocio necesita para crecer.',
  background_image: null,
  contact_button_text: 'Contacto',
  cv_button_text: 'Descargar CV',
  image_url: null,
  cv_url:
    'https://res.cloudinary.com/dxyk76jhu/raw/upload/fl_attachment:Hernan_Arango_FullStack_2026/v1776385388/elrincondelharco/Hernan_Arango_FullStack_2026.pdf',
};

// ────────────────────────────────────
// ABOUT
// ────────────────────────────────────
export const fallbackAbout: AboutResponse = {
  id: 3,
  title: 'Mi Trayectoria Profesional',
  description:
    'Mi nombre es Hernan Arango Cortes. Hace aproximadamente 5 años que resido en Avilés, Asturias, donde me he especializado en las tecnologías más modernas para ofrecer los mejores servicios a mis futuros clientes.\r\n\r\nMi carrera comenzó en Colombia a los 18 años. Durante 14 años trabajé en una empresa donde escalé posiciones hasta formar un equipo competitivo y ágil, al que con orgullo llamé el "Equipo de Oro".\r\n\r\nNos caracterizábamos por presentar soluciones rápidas y efectivas, una filosofía que mantengo hoy en día utilizando herramientas como FastAPI y Astro.',
  image_url:
    'https://res.cloudinary.com/dxyk76jhu/image/upload/v1776434042/elrincondelharco/WhatsApp_Image_2026-03-24_at_22_18_08.jpg',
  location: 'Avilés, Asturias, España',
  years_experience: '14+ Años',
  team_name: 'Equipo de Oro',
  leadership_title: 'Liderazgo',
  leadership_desc: 'Formación de equipos de alto rendimiento.',
  experience_title: 'Experiencia',
  experience_desc: 'Más de una década entregando soluciones tecnológicas.',
};

// ────────────────────────────────────
// STACK (24 tecnologías)
// ────────────────────────────────────
export const fallbackStacks: StackResponse[] = [
  { id: 26, name: 'HTML5', category: 'Frontend', icon: 'Globe', description: 'Estructura Web', color: 'text-orange-500', border: 'group-hover:border-orange-500/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]' },
  { id: 27, name: 'CSS3', category: 'Frontend', icon: 'Palette', description: 'Estilos Modernos', color: 'text-blue-500', border: 'group-hover:border-blue-500/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]' },
  { id: 28, name: 'Tailwind CSS', category: 'Frontend', icon: 'Palette', description: 'Estilos Utilitarios', color: 'text-cyan-400', border: 'group-hover:border-cyan-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]' },
  { id: 29, name: 'JavaScript', category: 'Frontend', icon: 'FileCode2', description: 'Interactividad', color: 'text-yellow-400', border: 'group-hover:border-yellow-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]' },
  { id: 30, name: 'TypeScript', category: 'Frontend', icon: 'FileCode2', description: 'JS Tipado', color: 'text-blue-400', border: 'group-hover:border-blue-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]' },
  { id: 31, name: 'React', category: 'Frontend', icon: 'Atom', description: 'Interfaces interactivas', color: 'text-cyan-400', border: 'group-hover:border-cyan-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]' },
  { id: 32, name: 'Astro', category: 'Frontend', icon: 'Rocket', description: 'Webs ultra rápidas', color: 'text-orange-400', border: 'group-hover:border-orange-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(251,146,60,0.3)]' },
  { id: 33, name: 'Next.js', category: 'Frontend', icon: 'LayoutTemplate', description: 'Framework de producción', color: 'text-white', border: 'group-hover:border-white/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]' },
  { id: 34, name: 'Python', category: 'Backend', icon: 'Terminal', description: 'Lenguaje Versátil', color: 'text-yellow-300', border: 'group-hover:border-yellow-300/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(253,224,71,0.3)]' },
  { id: 35, name: 'FastAPI', category: 'Backend', icon: 'Zap', description: 'APIs rápidas con Python', color: 'text-teal-400', border: 'group-hover:border-teal-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(45,212,191,0.3)]' },
  { id: 36, name: 'Django', category: 'Backend', icon: 'Layers', description: 'Framework Web Robusto', color: 'text-green-600', border: 'group-hover:border-green-600/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(22,163,74,0.3)]' },
  { id: 37, name: 'API REST', category: 'Backend', icon: 'Server', description: 'Arquitectura de APIs', color: 'text-indigo-400', border: 'group-hover:border-indigo-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(129,140,248,0.3)]' },
  { id: 38, name: 'JWT', category: 'Backend', icon: 'Lock', description: 'Seguridad & Auth', color: 'text-pink-500', border: 'group-hover:border-pink-500/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(236,72,153,0.3)]' },
  { id: 39, name: 'MongoDB', category: 'Backend', icon: 'Database', description: 'NoSQL escalable', color: 'text-green-400', border: 'group-hover:border-green-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(74,222,128,0.3)]' },
  { id: 40, name: 'NEON', category: 'Backend', icon: 'Server', description: 'Postgres Serverless', color: 'text-blue-400', border: 'group-hover:border-blue-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]' },
  { id: 41, name: 'Docker', category: 'DevOps', icon: 'Container', description: 'Contenedorización', color: 'text-blue-500', border: 'group-hover:border-blue-500/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]' },
  { id: 42, name: 'Git', category: 'DevOps', icon: 'GitBranch', description: 'Control de versiones', color: 'text-red-500', border: 'group-hover:border-red-500/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(239,68,68,0.3)]' },
  { id: 43, name: 'GitHub', category: 'DevOps', icon: 'Github', description: 'Colaboración', color: 'text-white', border: 'group-hover:border-white/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]' },
  { id: 44, name: 'Vercel', category: 'DevOps', icon: 'Triangle', description: 'Deploy Frontend', color: 'text-gray-200', border: 'group-hover:border-gray-200/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(229,231,235,0.2)]' },
  { id: 45, name: 'Render', category: 'DevOps', icon: 'Cloud', description: 'Cloud Hosting', color: 'text-purple-400', border: 'group-hover:border-purple-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(192,132,252,0.3)]' },
  { id: 46, name: 'VS Code', category: 'Herramientas', icon: 'Code2', description: 'Editor de Código', color: 'text-blue-500', border: 'group-hover:border-blue-500/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]' },
  { id: 47, name: 'Postman', category: 'Herramientas', icon: 'Send', description: 'Testing de APIs', color: 'text-orange-500', border: 'group-hover:border-orange-500/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]' },
  { id: 48, name: 'IA & LLMs', category: 'Herramientas', icon: 'BrainCircuit', description: 'Inteligencia Artificial', color: 'text-rose-400', border: 'group-hover:border-rose-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(251,113,133,0.3)]' },
  { id: 49, name: 'Optimización', category: 'Herramientas', icon: 'Gauge', description: 'Performance Web', color: 'text-yellow-400', border: 'group-hover:border-yellow-400/50', glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]' },
];

// ────────────────────────────────────
// PROJECTS
// ────────────────────────────────────
export const fallbackProjects: ProjectResponse[] = [
  {
    id: 6,
    title: 'Tapicería Moderna',
    description: 'Plataforma de gestión para taller de tapicería. Seguimiento de pedidos e inventario.',
    image_url: 'https://res.cloudinary.com/dxyk76jhu/image/upload/v1774103337/elrincondelharco/Captura_desde_2026-03-20_06-43-46.png',
    tags: ['Vite', 'Neon', 'Django', 'Tailwind'],
    icon_name: 'Layers',
    color: 'from-amber-500/20 to-orange-600/20',
    demo_url: 'https://www.tapiceriarincon.es/',
    github_url: 'https://github.com/hernanharco/web-tapiceriarincones',
  },
  {
    id: 8,
    title: 'Módulo de Seguridad',
    description: 'Autenticación robusta con JWT y OAuth2 para aplicaciones FastAPI.',
    image_url: 'https://res.cloudinary.com/dxyk76jhu/image/upload/v1776433683/elrincondelharco/Captura_desde_2026-04-17_14-53-54.png',
    tags: ['FastAPI', 'JWT', 'Security'],
    icon_name: 'Lock',
    color: 'from-pink-500/20 to-rose-600/20',
    demo_url: 'https://auth.elrincondeharco.com/dashboard',
    github_url: 'https://github.com/hernanharco/authelrincondeharco',
  },
  {
    id: 7,
    title: 'CoreAppointment',
    description: 'Sistema modular de gestión de citas y turnos multi-tenant.',
    image_url: 'https://res.cloudinary.com/dxyk76jhu/image/upload/v1776430358/elrincondelharco/Captura_desde_2026-04-17_14-51-45.png',
    tags: ['FastAPI', 'Svelte', 'PostgreSQL'],
    icon_name: 'Calendar',
    color: 'from-blue-500/20 to-cyan-600/20',
    demo_url: 'https://appointment.elrincondeharco.com/',
    github_url: 'https://github.com/hernanharco/Appointment-elrincondeharco',
  },
  {
    id: 9,
    title: 'Café Mi Tierra',
    description: 'Web corporativa para cafetería/bar con efectos visuales inmersivos (Three.js, GSAP), panel de administración completo, galería interactiva, horarios, reseñas y sistema de contacto.',
    image_url: null,
    tags: ['Astro 7', 'Svelte 5', 'Three.js', 'GSAP', 'Hono.js', 'PostgreSQL'],
    icon_name: 'Coffee',
    color: 'from-amber-700/30 to-red-800/30',
    demo_url: 'https://frontend-gray-alpha-wjs0x2ofbn.vercel.app/',
    github_url: 'https://github.com/hernanharco/cafemitierra',
  },
  {
    id: 10,
    title: 'Nanatha',
    description: 'Tienda online de moda femenina con catálogo inteligente, filtros avanzados por categoría/color/material, drops exclusivos y panel de administración.',
    image_url: null,
    tags: ['Astro 7', 'Tailwind 4', 'Hono.js', 'Node.js'],
    icon_name: 'ShoppingBag',
    color: 'from-blush-400/30 to-rose-500/30',
    demo_url: 'https://frontend-six-drab-fsccnsoh2d.vercel.app/',
    github_url: 'https://github.com/hernanharco/tiendananatha',
  },
  {
    id: 11,
    title: 'miniCRM Ghogares',
    description: 'CRM inmobiliario inteligente con motor de matching automático. Integra scrapers de Fotocasa e Idealista para emparejar propiedades con contactos según presupuesto, ubicación y preferencias.',
    image_url: null,
    tags: ['FastAPI', 'Python', 'SQLAlchemy', 'HTMX', 'SQLite'],
    icon_name: 'Building2',
    color: 'from-emerald-500/30 to-teal-600/30',
    demo_url: null,
    github_url: 'https://github.com/hernanharco/miniCRM-Ghogares',
  },
  {
    id: 12,
    title: 'Scrapers Inmobiliarios',
    description: 'Sistema de scraping automático para portales inmobiliarios (Fotocasa e Idealista). Extracción programada de propiedades con normalización de datos y detección de cambios en tiempo real.',
    image_url: null,
    tags: ['Python', 'Playwright', 'ETL', 'Automatización'],
    icon_name: 'Bot',
    color: 'from-violet-500/30 to-purple-700/30',
    demo_url: null,
    github_url: null,
  },
];

// ────────────────────────────────────
// SECTORS (6 rubros)
// ────────────────────────────────────
export const fallbackSectors: SectorResponse[] = [
  {
    id: 1,
    name: 'Hostelería',
    client_name: 'Café Mi Tierra',
    description: 'Webs inmersivas con gestión de reservas y pedidos.',
    icon_path: 'M17 8h1a4 4 0 1 1 0 8h-1 M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z',
    color_gradient: 'from-amber-700/30 to-red-800/30',
    sort_order: 1,
    project_ids: [], // projects are matched by title in SectorProjects
  },
  {
    id: 2,
    name: 'Inmobiliaria',
    client_name: 'Grupo Hogares',
    description: 'CRM con matching automático y scrapers de portales.',
    icon_path: 'M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2',
    color_gradient: 'from-emerald-500/30 to-teal-600/30',
    sort_order: 2,
    project_ids: [],
  },
  {
    id: 3,
    name: 'Talleres',
    client_name: 'Tapicería Moderna',
    description: 'Plataformas de gestión de pedidos e inventario.',
    icon_path: 'M12 2 2 7l10 5 10-5-10-5Z m2 17 10 5 10-5',
    color_gradient: 'from-amber-500/20 to-orange-600/20',
    sort_order: 3,
    project_ids: [],
  },
  {
    id: 4,
    name: 'Salud',
    client_name: 'Clínicas',
    description: 'Sistemas de gestión de citas y pacientes.',
    icon_path: 'M22 12h-4l-3 9L9 3l-3 9H2',
    color_gradient: 'from-blue-500/20 to-cyan-600/20',
    sort_order: 4,
    project_ids: [],
  },
  {
    id: 5,
    name: 'Belleza',
    client_name: 'Centros Estéticos',
    description: 'Tiendas online y plataformas de gestión de servicios.',
    icon_path: 'M12 20h9 M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z',
    color_gradient: 'from-blush-400/30 to-rose-500/30',
    sort_order: 5,
    project_ids: [],
  },
  {
    id: 6,
    name: 'Logística',
    client_name: 'Distribución',
    description: 'Sistemas modulares de control de envíos.',
    icon_path: 'M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16',
    color_gradient: 'from-violet-500/30 to-purple-700/30',
    sort_order: 6,
    project_ids: [],
  },
];

// ────────────────────────────────────
// SITE SETTINGS
// ────────────────────────────────────
// PASSIONS
// ────────────────────────────────────
export const fallbackPassion: PassionResponse = {
  id: 3,
  title: 'Más allá del Código',
  description:
    'Mi pasión, aparte de programar y jugar videojuegos, es estar con mi familia.',
  image_url:
    'https://res.cloudinary.com/dxyk76jhu/image/upload/v1776596418/elrincondelharco/image2.jpg',
  family_title: 'Mi Familia',
  family_desc:
    'Son mi motor, mi pasión y la razón de querer continuar cada día y cada momento.',
  games_title: 'Videojuegos',
  games_desc: 'Un hobby que me permite desconectar y explorar nuevos mundos digitales.',
  coding_title: 'Programación',
  coding_desc: 'No es solo mi trabajo, es mi forma de crear y aportar valor al mundo.',
};

// ────────────────────────────────────
// FOOTER
// ────────────────────────────────────
export const fallbackFooter: FooterResponse = {
  id: 2,
  name: 'Hernan Arango Cortes',
  description: 'Programador Full Stack enfocado en rendimiento. Creando el futuro web desde Asturias.',
  location: 'Avilés, Asturias, España',
  email: 'hernan.harco@gmail.com',
  github_url: null,
  linkedin_url: null,
  twitter_url: null,
  quick_links: [
    { href: '#inicio', text: 'Inicio' },
    { href: '#sobre-mi', text: 'Sobre Mí' },
    { href: '#stack', text: 'Stack Tecnológico' },
  ],
};

// ────────────────────────────────────
// SITE SETTINGS
// ────────────────────────────────────
export const fallbackSiteSettings: SiteSettingsResponse = {
  id: 3,
  brand_name: 'elrincondeharco.com',
  site_url: 'https://elrincondeharco.com/',
  legal_name: 'Hernan Arango Cortes',
  slogan:
    'Programador Full Stack enfocado en velocidad y rendimiento. Creando el futuro de la web desde Asturias para el mundo.',
  copyright_notice: '© 2026 Todos los derechos reservados.',
  contact_email: 'hernan.harco@gmail.com',
  social_networks: {
    github: 'https://github.com/hernanharco',
    linkedin: 'https://www.linkedin.com/in/hernan-harco/',
  },
  is_active: true,
};

// ────────────────────────────────────
// SHOWROOM (7 registros)
// ────────────────────────────────────
export const fallbackShowrooms: ShowroomResponse[] = [
  {
    id: 1,
    title: 'Pagina Web Barberia',
    description: 'pagina para un centro de peluquería para hombre',
    category: 'Web App',
    deploy_url: 'https://elrincondeharco-barberia.vercel.app/',
    image_url:
      'https://res.cloudinary.com/dxyk76jhu/image/upload/v1776685027/elrincondelharco/Captura_desde_2026-04-20_13-36-12.png',
  },
  {
    id: 2,
    title: 'SegurosConfianza',
    description:
      'Plataforma interactiva para gestionar pólizas de seguros, enfocada en la experiencia de usuario, diseño moderno con Svelte y navegación eficiente.',
    category: 'Web App',
    deploy_url: 'https://prototipo-seguros-ten.vercel.app/',
    image_url:
      'https://res.cloudinary.com/dxyk76jhu/image/upload/v1778130584/elrincondelharco/Captura_desde_2026-05-07_07-09-29.png',
  },
  {
    id: 3,
    title: 'Gestión de Taller Mecánico Pro',
    description:
      'Sistema modular para administrar reparaciones y clientes, optimizado para flujos de trabajo eficientes y visualización clara del estado vehicular.',
    category: 'Web App',
    deploy_url: 'https://prototipo-tallermecanico.vercel.app/',
    image_url:
      'https://res.cloudinary.com/dxyk76jhu/image/upload/v1778130662/elrincondelharco/Captura_desde_2026-05-07_07-10-40.png',
  },
  {
    id: 4,
    title: 'Prixline: Gestión de Logística Integral',
    description:
      'Sistema modular para el control de envíos y distribución, diseñado con responsabilidad única para optimizar la cadena de suministro logística.',
    category: 'Web App',
    deploy_url: 'https://prototipo-prixline.vercel.app/',
    image_url:
      'https://res.cloudinary.com/dxyk76jhu/image/upload/v1778130727/elrincondelharco/Captura_desde_2026-05-07_07-11-50.png',
  },
  {
    id: 5,
    title: 'Gestión Gastronómica Inteligente',
    description:
      'Plataforma modular para administrar pedidos y reservas de restaurante, optimizada con una interfaz moderna para mejorar la experiencia del comensal.',
    category: 'Web App',
    deploy_url: 'https://prototipo-restauran-dafni.vercel.app/',
    image_url:
      'https://res.cloudinary.com/dxyk76jhu/image/upload/v1778130800/elrincondelharco/Captura_desde_2026-05-07_07-13-02.png',
  },
  {
    id: 6,
    title: 'Gestión Clínica Especializada',
    description:
      'Sistema modular para la administración de consultas y pacientes, enfocado en la eficiencia operativa y una interfaz clara y profesional.',
    category: 'Web App',
    deploy_url: 'https://prototipo-dctandrea.vercel.app/',
    image_url:
      'https://res.cloudinary.com/dxyk76jhu/image/upload/v1778130904/elrincondelharco/Captura_desde_2026-05-07_07-14-55.png',
  },
  {
    id: 7,
    title: 'Gestión Estética Modular',
    description:
      'Plataforma optimizada para la administración de citas y servicios de belleza, con una interfaz intuitiva centrada en la experiencia del cliente.',
    category: 'Web App',
    deploy_url: 'https://prototipo-beautycenter.vercel.app/',
    image_url:
      'https://res.cloudinary.com/dxyk76jhu/image/upload/v1778130965/elrincondelharco/Captura_desde_2026-05-07_07-15-54.png',
  },
];

// ────────────────────────────────────
// TESTIMONIALS
// ────────────────────────────────────
export const fallbackTestimonials: TestimonialResponse[] = [
  {
    id: 1,
    name: 'Carlos Martínez',
    role: 'Dueño',
    company: 'Café Mi Tierra',
    content: 'Hernán transformó por completo nuestra presencia online. Pasamos de tener una web que no funcionaba a una plataforma que nos genera clientes cada semana. Profesional total.',
    rating: 5,
    avatar_url: null,
    is_active: true,
    sort_order: 1,
  },
  {
    id: 2,
    name: 'María García',
    role: 'Directora',
    company: 'Grupo Hogares',
    content: 'Necesitábamos un sistema para gestionar propiedades y contactos. Hernán no solo nos hizo la plataforma, sino que nos automatizó procesos que nos ahorran horas cada semana.',
    rating: 5,
    avatar_url: null,
    is_active: true,
    sort_order: 2,
  },
  {
    id: 3,
    name: 'Ana López',
    role: 'Dueña',
    company: 'Nanatha',
    content: 'La web que me hizo no solo es hermosa, sino que MIS CLIENTES me dicen "qué página más profesional". Y lo mejor: ahora recibo pedidos online sin esfuerzo.',
    rating: 5,
    avatar_url: null,
    is_active: true,
    sort_order: 3,
  },
];
