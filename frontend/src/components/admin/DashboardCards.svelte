<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type {
    ProjectResponse,
    SectorResponse,
    ShowroomResponse,
    StackResponse,
    TestimonialResponse,
    HeroResponse,
    AboutResponse,
    ExperienceSectionResponse,
  } from '$lib/types';
  import Icon from '@iconify/svelte';

  // ── Estado de carga ─────────────────────────────────────────
  let loading = true;
  let apiError = '';
  let lastUpdated = '';

  // ── Conteos por sección ─────────────────────────────────────
  let projects: ProjectResponse[] = [];
  let sectors: SectorResponse[] = [];
  let testimonials: TestimonialResponse[] = [];
  let showroom: ShowroomResponse[] = [];
  let stacks: StackResponse[] = [];
  let hero: HeroResponse | null = null;
  let about: AboutResponse | null = null;
  let experience: ExperienceSectionResponse | null = null;

  // ── Insights derivados ──────────────────────────────────────
  let projectsWithImage = 0;
  let projectsWithDemo = 0;
  let projectsWithGithub = 0;
  let activeTestimonials = 0;
  let sectorsWithProjects = 0;

  function loadAll() {
    loading = true;
    apiError = '';

    Promise.allSettled([
      fetchApi<ProjectResponse[]>('/api/v1/projects/'),
      fetchApi<SectorResponse[]>('/api/v1/sectors/'),
      fetchApi<TestimonialResponse[]>('/api/v1/testimonials/all'),
      fetchApi<ShowroomResponse[]>('/api/v1/showrooms/'),
      fetchApi<StackResponse[]>('/api/v1/stacks/'),
      fetchApi<HeroResponse>('/api/v1/heroes/latest/'),
      fetchApi<AboutResponse>('/api/v1/abouts/latest/'),
      fetchApi<ExperienceSectionResponse>('/api/v1/experience/latest/'),
    ]).then((results) => {
      const [p, s, t, sh, st, h, a, e] = results;

      projects = p.status === 'fulfilled' ? p.value : [];
      sectors = s.status === 'fulfilled' ? s.value : [];
      testimonials = t.status === 'fulfilled' ? t.value : [];
      showroom = sh.status === 'fulfilled' ? sh.value : [];
      stacks = st.status === 'fulfilled' ? st.value : [];
      hero = h.status === 'fulfilled' ? h.value : null;
      about = a.status === 'fulfilled' ? a.value : null;
      experience = e.status === 'fulfilled' ? e.value : null;

      const failed = results.filter((r) => r.status === 'rejected').length;
      if (failed > 0) {
        apiError = `${failed} de 8 secciones no respondieron. Revisá la conexión con la API.`;
      }

      projectsWithImage = projects.filter((x) => (x.image_urls?.length ?? 0) > 0).length;
      projectsWithDemo = projects.filter((x) => Boolean(x.demo_url)).length;
      projectsWithGithub = projects.filter((x) => Boolean(x.github_url)).length;
      activeTestimonials = testimonials.filter((x) => x.is_active).length;
      sectorsWithProjects = sectors.filter((x) => (x.project_ids?.length ?? 0) > 0).length;

      lastUpdated = new Date().toLocaleString('es-ES', {
        day: '2-digit',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
      });

      loading = false;
    });
  }

  onMount(() => {
    loadAll();
  });

  // ── Tarjetas de navegación con conteo ───────────────────────
  const navCards = [
    { href: '/admin/hero', label: 'Hero', icon: 'lucide:type', description: 'Título y subtítulo principal', count: hero ? 'Configurado' : 'Sin datos' },
    { href: '/admin/about', label: 'Sobre Mí', icon: 'lucide:user', description: 'Trayectoria y foto', count: about ? 'Configurado' : 'Sin datos' },
    { href: '/admin/experience', label: 'Experiencia', icon: 'lucide:briefcase', description: 'Cabecera de la sección de rubros', count: experience ? 'Configurado' : 'Sin datos' },
    { href: '/admin/projects', label: 'Proyectos', icon: 'lucide:folder-kanban', description: 'Galería de proyectos destacados', count: `${projects.length}` },
    { href: '/admin/sectors', label: 'Sectores', icon: 'lucide:layout-grid', description: 'Rubros y asignación de proyectos', count: `${sectors.length}` },
    { href: '/admin/testimonials', label: 'Testimonios', icon: 'lucide:message-square-quote', description: 'Lo que dicen los clientes', count: `${testimonials.length}` },
    { href: '/admin/showroom', label: 'Showroom', icon: 'lucide:sparkles', description: 'Prototipos y experimentos', count: `${showroom.length}` },
    { href: '/admin/stack', label: 'Stack', icon: 'lucide:layers', description: 'Tecnologías del arsenal', count: `${stacks.length}` },
    { href: '/admin/site-settings', label: 'Configuración', icon: 'lucide:settings', description: 'Nombre, redes, copyright, CTA', count: '—' },
  ];

  // ── Alertas de configuración ────────────────────────────────
  function getAlerts(): { level: 'warn' | 'info'; text: string }[] {
    const alerts: { level: 'warn' | 'info'; text: string }[] = [];

    const emptySectors = sectors.filter((s) => (s.project_ids?.length ?? 0) === 0);
    if (emptySectors.length > 0) {
      alerts.push({
        level: 'warn',
        text: `Sectores sin proyectos: ${emptySectors.map((s) => s.name).join(', ')}.`,
      });
    }

    const noImage = projects.filter((x) => (x.image_urls?.length ?? 0) === 0);
    if (noImage.length > 0) {
      alerts.push({
        level: 'info',
        text: `${noImage.length} proyectos sin imagen. Se muestran con un placeholder.`,
      });
    }

    if (projectsWithDemo < projects.length) {
      alerts.push({
        level: 'info',
        text: `${projects.length - projectsWithDemo} proyectos sin demo URL.`,
      });
    }

    if (activeTestimonials < testimonials.length) {
      alerts.push({
        level: 'info',
        text: `${testimonials.length - activeTestimonials} testimonios inactivos.`,
      });
    }

    return alerts;
  }
</script>

<div>
  <!-- ── Barra de estado ─────────────────────────────────────── -->
  <div class="flex items-center justify-between gap-3 mb-6 p-4 rounded-xl bg-zinc-900 border border-zinc-800">
    <div class="flex items-center gap-3">
      <div
        class="w-2.5 h-2.5 rounded-full {loading ? 'bg-zinc-600 animate-pulse' : apiError ? 'bg-red-500' : 'bg-emerald-500'}"
      ></div>
      <div>
        <p class="text-sm font-semibold text-zinc-100">
          {loading ? 'Consultando API…' : apiError ? 'API con errores parciales' : 'API conectada'}
        </p>
        {#if !loading && lastUpdated}
          <p class="text-xs text-zinc-500">Actualizado {lastUpdated}</p>
        {/if}
      </div>
    </div>
    <button
      on:click={loadAll}
      class="px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-amber-400 hover:bg-zinc-800 border border-zinc-700/60 transition-colors flex items-center gap-1.5"
    >
      <Icon icon="lucide:refresh-cw" width="14" height="14" />
      Refrescar
    </button>
  </div>

  {#if apiError}
    <div class="mb-6 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-sm text-red-400">
      {apiError}
    </div>
  {/if}

  <!-- ── Alertas ─────────────────────────────────────────────── -->
  {#if !loading && getAlerts().length > 0}
    <div class="mb-8 space-y-2">
      {#each getAlerts() as alert}
        <div
          class="flex items-start gap-2.5 p-3 rounded-lg border text-sm
            {alert.level === 'warn'
              ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
              : 'bg-cyan-500/5 border-cyan-500/20 text-cyan-300/80'}"
        >
          <Icon
            icon={alert.level === 'warn' ? 'lucide:alert-triangle' : 'lucide:info'}
            width="16"
            height="16"
            class="mt-0.5 shrink-0"
          />
          <span>{alert.text}</span>
        </div>
      {/each}
    </div>
  {/if}

  <!-- ── Métricas rápidas ────────────────────────────────────── -->
  {#if !loading}
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="p-4 rounded-xl bg-zinc-900 border border-zinc-800">
        <p class="text-3xl font-bold text-amber-400">{projectsWithImage}<span class="text-lg text-zinc-500">/{projects.length}</span></p>
        <p class="text-xs text-zinc-500 mt-1">Proyectos con imagen</p>
      </div>
      <div class="p-4 rounded-xl bg-zinc-900 border border-zinc-800">
        <p class="text-3xl font-bold text-amber-400">{projectsWithDemo}</p>
        <p class="text-xs text-zinc-500 mt-1">Con demo en línea</p>
      </div>
      <div class="p-4 rounded-xl bg-zinc-900 border border-zinc-800">
        <p class="text-3xl font-bold text-amber-400">{sectorsWithProjects}<span class="text-lg text-zinc-500">/{sectors.length}</span></p>
        <p class="text-xs text-zinc-500 mt-1">Sectores con proyectos</p>
      </div>
      <div class="p-4 rounded-xl bg-zinc-900 border border-zinc-800">
        <p class="text-3xl font-bold text-amber-400">{projectsWithGithub}</p>
        <p class="text-xs text-zinc-500 mt-1">Con repositorio</p>
      </div>
    </div>
  {/if}

  <!-- ── Tarjetas de navegación ──────────────────────────────── -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    {#each navCards as section}
      <a
        href={section.href}
        class="
          block p-5 rounded-xl bg-zinc-900 border border-zinc-800
          hover:border-amber-400 hover:bg-zinc-800
          transition-all duration-200 group
        "
      >
        <div class="flex items-start justify-between gap-3 mb-2">
          <Icon icon={section.icon} width="22" height="22" class="text-amber-400/80 group-hover:text-amber-400 transition-colors" />
          {#if loading}
            <span class="w-8 h-4 rounded bg-zinc-800 animate-pulse"></span>
          {:else}
            <span class="text-xs font-semibold text-amber-400/90 whitespace-nowrap">{section.count}</span>
          {/if}
        </div>
        <h2
          class="text-base font-semibold text-zinc-100 group-hover:text-amber-400 mb-1 transition-colors"
        >
          {section.label}
        </h2>
        <p class="text-sm text-zinc-500">{section.description}</p>
      </a>
    {/each}
  </div>
</div>
