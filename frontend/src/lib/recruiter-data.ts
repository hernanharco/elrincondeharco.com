// ──────────────────────────────────────────────────────────────
// recruiter-data.ts — Perfil técnico para modo recruiter
// ──────────────────────────────────────────────────────────────
// Datos completos del perfil profesional de Hernán Arango Cortés
// orientado a reclutadores y desarrolladores.
// ──────────────────────────────────────────────────────────────

export interface TechItem {
  name: string;
  category: string;
  icon: string;
  description: string;
}

export interface RecruiterProject {
  title: string;
  description: string;
  tags: string[];
  github?: string;
  demo?: string;
  type: 'freelance' | 'personal' | 'empresa';
}

export interface TimelineEntry {
  year: string;
  title: string;
  subtitle: string;
  description: string;
  type: 'trabajo' | 'estudio' | 'logro' | 'hito';
  tags?: string[];
}

export interface Certification {
  name: string;
  area: string;
  icon: string;
}

export interface ServerSpec {
  name: string;
  provider: string;
  specs: string;
  services: string[];
  os: string;
  uptime?: string;
}

export interface RecruiterData {
  name: string;
  role: string;
  location: string;
  email: string;
  github: string;
  linkedin: string;
  summary: string;
  stack: TechItem[];
  projects: RecruiterProject[];
  servers: ServerSpec[];
  metrics: { label: string; value: string }[];
  timeline: TimelineEntry[];
  certifications: Certification[];
}

// ── Stack Tecnológico ────────────────────────────────────────

export const RECRUITER_TECH_STACK: TechItem[] = [
  // Backend
  { name: 'Python', category: 'Backend', icon: '🐍', description: 'FastAPI, Django, Scripts' },
  { name: 'Go', category: 'Backend', icon: '🔷', description: 'Microservicios, APIs, TUIs' },
  { name: 'Node.js', category: 'Backend', icon: '🟢', description: 'APIs, herramientas CLI' },
  // Frontend
  { name: 'Astro', category: 'Frontend', icon: '🚀', description: 'Islas, SSG, rendimiento' },
  { name: 'Svelte', category: 'Frontend', icon: '🧡', description: 'Componentes reactivos ligeros' },
  { name: 'React', category: 'Frontend', icon: '⚛️', description: 'SPAs, dashboards' },
  { name: 'Angular', category: 'Frontend', icon: '🅰️', description: 'Aplicaciones empresariales' },
  { name: 'Tailwind CSS', category: 'Frontend', icon: '🎨', description: 'Estilos utilities-first' },
  // Infraestructura
  { name: 'Docker', category: 'Infra', icon: '🐳', description: 'Contenedores, compose, swarm' },
  { name: 'Hetzner', category: 'Infra', icon: '☁️', description: 'Servidor dedicado CX22' },
  { name: 'Netcup', category: 'Infra', icon: '☁️', description: 'Servidor corporativo' },
  { name: 'Traefik', category: 'Infra', icon: '🔀', description: 'Proxy inverso, SSL automático' },
  { name: 'WireGuard', category: 'Infra', icon: '🔒', description: 'VPN site-to-site' },
  { name: 'Cloudflare Tunnel', category: 'Infra', icon: '🌐', description: 'SSH sin puertos abiertos' },
  { name: 'Tailscale', category: 'Infra', icon: '🔗', description: 'Mesh VPN zero-config' },
  // Base de datos
  { name: 'PostgreSQL', category: 'BD', icon: '🐘', description: 'Base de datos relacional' },
  { name: 'Supabase', category: 'BD', icon: '🔥', description: 'BaaS con PostgreSQL' },
  // Herramientas
  { name: 'OpenCode', category: 'Tools', icon: '🤖', description: 'AI coding assistant' },
  { name: 'n8n', category: 'Tools', icon: '⚡', description: 'Workflow automation' },
  { name: 'Ollama', category: 'Tools', icon: '🧠', description: 'Modelos open-source locales' },
  { name: 'Git', category: 'Tools', icon: '📦', description: 'Control de versiones' },
];

// ── Proyectos ─────────────────────────────────────────────────

export const RECRUITER_PROJECTS: RecruiterProject[] = [
  {
    title: 'AuthCore',
    description: 'Sistema de autenticación multi-app con Google OAuth, JWT y sesiones. Backend en FastAPI + frontend en Astro.',
    tags: ['FastAPI', 'Astro', 'PostgreSQL', 'JWT', 'Docker'],
    github: 'https://github.com/hernanharco/authcore',
    type: 'personal',
  },
  {
    title: 'Scrapers Automatizados',
    description: 'Scrapers para Idealista y Fotocasa con extracción de datos de propiedades, almacenamiento en PostgreSQL y dashboards.',
    tags: ['Python', 'Scraping', 'PostgreSQL', 'Docker'],
    type: 'freelance',
  },
  {
    title: 'MiniCRM Ghogares',
    description: 'CRM inmobiliario liviano para gestión de propiedades, clientes y seguimiento de visitas.',
    tags: ['React', 'Node.js', 'PostgreSQL', 'Tailwind'],
    type: 'freelance',
  },
  {
    title: 'Appointment System',
    description: 'Sistema de turnos y reservas online con notificaciones y panel de administración.',
    tags: ['FastAPI', 'Astro', 'PostgreSQL', 'Docker'],
    github: 'https://github.com/hernanharco/appointment',
    type: 'personal',
  },
  {
    title: 'Café Mi Tierra',
    description: 'Web profesional para hostelería con carta digital, reservas y presencia online.',
    tags: ['Astro', 'Svelte', 'Tailwind', 'PostgreSQL'],
    type: 'freelance',
  },
  {
    title: 'Tienda Nanatha',
    description: 'E-commerce completo con catálogo, carrito, pasarela de pago y panel de gestión.',
    tags: ['Astro', 'Svelte', 'Tailwind', 'PostgreSQL'],
    demo: 'https://frontend-six-drab-fsccnsoh2d.vercel.app/',
    type: 'freelance',
  },
  {
    title: 'Dashboard Bayiva',
    description: 'Panel de analytics con visualización de datos de propiedades, métricas de scraping y reportes.',
    tags: ['React', 'Python', 'PostgreSQL', 'Docker'],
    type: 'freelance',
  },
  {
    title: 'Portfolio elRincondeHarco',
    description: 'Landing page + CRM personal con panel admin, sectores, proyectos y testimonios. Efectos 3D con Three.js y GSAP.',
    tags: ['Astro', 'Svelte', 'Three.js', 'GSAP', 'FastAPI', 'Docker'],
    github: 'https://github.com/hernanharco/portfolio',
    demo: 'https://www.elrincondeharco.com/',
    type: 'personal',
  },
  {
    title: 'Tapiceria Rincones',
    description: 'Web profesional para taller de tapicería con galería de trabajos y contacto.',
    tags: ['Astro', 'Tailwind', 'PostgreSQL'],
    type: 'freelance',
  },
];

// ── Timeline profesional ─────────────────────────────────────
export const RECRUITER_TIMELINE: TimelineEntry[] = [
  { year: '1998', title: 'Descubrí la programación', subtitle: 'Visual Basic', description: 'Mi profesor John Freddy Tamayo me enseñó hardware y Visual Basic. A los 12 años ya hacía mis primeros programitas.', type: 'hito', tags: ['Visual Basic'] },
  { year: '2004', title: 'Profesor de informática', subtitle: 'Colegio, Colombia', description: 'El colegio me contrató para enseñar bachillerato acelerado. 4-6 meses dando clase a otros estudiantes.', type: 'trabajo', tags: ['Educación'] },
  { year: '2007', title: 'Ingeniero de Sistemas', subtitle: 'Univ. San Buenaventura / Unicomfacauca', description: 'Ingresé a la Universidad San Buenaventura de Cali (prestigiosa) y terminé en la Antonio José Camacho por economía familiar.', type: 'estudio', tags: ['Ingeniería'] },
  { year: '2007', title: 'Ingreso a DICEL', subtitle: 'Analista de datos', description: 'Entré como sistemas y pasé a analista de datos. Creé un programa en Java que redujo jornadas de 15h a 9h.', type: 'trabajo', tags: ['Java', 'SQL', 'Excel'] },
  { year: '2015', title: 'Analista 1 / Semijefe', subtitle: 'DICEL, Colombia', description: 'Mano derecha del jefe, poder de decisión. Formé el "equipo de oro". Resultados ISO >90%. Mejoré el área más del 50%.', type: 'logro', tags: ['Liderazgo', 'Gestión'] },
  { year: '2021', title: 'Emigración a España', subtitle: 'Avilés, Asturias', description: 'Llegué a España en octubre. Sin papeles, trabajé en construcción mientras buscaba oportunidades.', type: 'hito', tags: ['Adaptación'] },
  { year: '2023', title: 'Primer empleo formal en España', subtitle: 'SEKELY CASAS SL', description: 'Primer contrato formal. Luego SUMESA S.A. (294 días) como mozo de almacén.', type: 'trabajo', tags: ['Logística'] },
  { year: '2024', title: 'Desarrollo de software freelance', subtitle: 'Bayiva + proyectos propios', description: 'Pruebas técnicas con Bayiva: scrapers de Idealista y Fotocasa, dashboard, mini CRM. Empecé a construir mi portfolio.', type: 'trabajo', tags: ['Python', 'Scraping', 'React', 'FastAPI'] },
  { year: '2025', title: 'Autónomo en Asturias', subtitle: 'Reparto + desarrollo', description: 'Trabajé como autónomo mientras seguía desarrollando. AuthCore, Appointment, Nanatha, Café Mi Tierra.', type: 'trabajo', tags: ['FastAPI', 'Astro', 'Svelte', 'Docker'] },
  { year: '2026', title: 'Arquitecto en formación', subtitle: 'elRincondeHarco.com', description: 'Portfolio dual con CRM, panel admin, efectos 3D, CI/CD. Administro mis propios servidores Hetzner + Netcup.', type: 'logro', tags: ['FullStack', 'DevOps', 'Arquitectura'] },
];

// ── Certificaciones ───────────────────────────────────────────
export const RECRUITER_CERTIFICATIONS: Certification[] = [
  { name: 'Universidad Python sin Límites', area: 'Python', icon: '🐍' },
  { name: 'Universidad Python con IA de ChatGPT', area: 'Python', icon: '🐍' },
  { name: 'Curso Práctico de Django', area: 'Django', icon: '🌐' },
  { name: 'Angular - Tomas Ruiz Diaz', area: 'Angular', icon: '🅰️' },
  { name: 'Desarrollo de Páginas Web CSS y Joomla', area: 'CSS/Web', icon: '🎨' },
  { name: 'Testing y Debugging de Software', area: 'Testing', icon: '🧪' },
  { name: 'Fundamentos de Data Analytics', area: 'Data', icon: '📊' },
  { name: 'ChatGPT 5 - Marketing y Branding con IA', area: 'IA', icon: '🤖' },
  { name: 'Prompt Engineering para IA Generativa', area: 'IA', icon: '🤖' },
  { name: 'Curso n8n - Crea Agentes de IA', area: 'IA', icon: '⚡' },
  { name: 'Inteligencia Artificial TOTAL', area: 'IA', icon: '🧠' },
  { name: 'Facturación Electrónica', area: 'Ofimática', icon: '📄' },
];

// ── Servidores ────────────────────────────────────────────────

export const RECRUITER_SERVERS: ServerSpec[] = [
  {
    name: 'Hetzner',
    provider: 'Hetzner CX22',
    specs: '2 cores · 4GB RAM · 40GB SSD · Ubuntu 24.04',
    services: ['Traefik', 'Dokploy', 'Backend API', 'AuthCore', 'PostgreSQL', 'Appointment', 'Engram Cloud', 'Cloudflared', 'Netdata', 'Ollama'],
    os: 'Ubuntu 24.04 LTS',
    uptime: '9+ dias',
  },
  {
    name: 'Netcup',
    provider: 'Netcup VPS',
    specs: '2 cores · 4GB RAM · 100GB SSD · Ubuntu 24.04',
    services: ['Coolify', 'Supabase', 'N8N', 'APIs Bayiva', 'WireGuard'],
    os: 'Ubuntu 24.04 LTS',
  },
];

// ── Métricas ──────────────────────────────────────────────────

export const RECRUITER_METRICS = [
  { label: 'Años de experiencia', value: '14+' },
  { label: 'Proyectos entregados', value: '20+' },
  { label: 'Servidores administrados', value: '2' },
  { label: 'Certificaciones', value: '23' },
  { label: 'Tecnologias dominadas', value: '21' },
];

// ── Perfil completo ───────────────────────────────────────────

export const recruiterData: RecruiterData = {
  name: 'Hernan Arango Cortes',
  role: 'Ingeniero de Sistemas | 14+ años en tecnología',
  location: 'Aviles, Asturias, Espana',
  email: 'hernan.harco@gmail.com',
  github: 'https://github.com/hernanharco',
  linkedin: 'https://www.linkedin.com/in/hernan-harco/',
  summary:
    'Ingeniero de Sistemas con 14+ años de experiencia en tecnología. ' +
    'He liderado equipos, diseñado arquitecturas y construido soluciones completas: ' +
    'desde scrapers automatizados y CRMs hasta sistemas de autenticación multi-app. ' +
    'Administro mis propios servidores (Hetzner + Netcup) con Docker, Traefik, WireGuard y Cloudflare Tunnel. ' +
    'Apasionado por la automatización, las arquitecturas limpias y crear software que resuelva problemas reales.',
  stack: RECRUITER_TECH_STACK,
  projects: RECRUITER_PROJECTS,
  servers: RECRUITER_SERVERS,
  metrics: RECRUITER_METRICS,
  timeline: RECRUITER_TIMELINE,
  certifications: RECRUITER_CERTIFICATIONS,
};
