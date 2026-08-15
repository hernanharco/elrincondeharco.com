<svelte:options runes={false} />

<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Icon from '@iconify/svelte';

  export let currentPath: string = '';

  // La preferencia del usuario (colapsado/expandido) se guarda en
  // localStorage para que el sidebar mantenga la última elección entre
  // visitas. En móvil el drawer siempre arranca cerrado (no se persiste).
  const STORAGE_KEY = 'admin:sidebar:collapsed';

  let collapsed = false;
  let mobileOpen = false;

  function restorePreference() {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored !== null) collapsed = stored === 'true';
    } catch {
      // localStorage no disponible (modo privado, etc.) → default
    }
  }

  // En móvil el sidebar es un drawer overlay; en desktop mantiene el
  // comportamiento expandido/colapsado con el botón chevron.
  onMount(() => {
    restorePreference();
    if (window.innerWidth < 768) {
      collapsed = true;
    }
    window.addEventListener('resize', handleResize);
    window.addEventListener('admin:sidebar-open', handleOpenEvent);
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('admin:sidebar-open', handleOpenEvent);
    };
  });

  function handleResize() {
    if (window.innerWidth < 768) {
      collapsed = true;
      mobileOpen = false;
    } else {
      // Al volver a desktop, restaurar la preferencia guardada del usuario.
      restorePreference();
      mobileOpen = false;
    }
  }

  // El header móvil (AdminLayout) dispara este evento al tocar ☰.
  function handleOpenEvent() {
    mobileOpen = true;
  }

  function toggle() {
    collapsed = !collapsed;
    try {
      window.localStorage.setItem(STORAGE_KEY, String(collapsed));
    } catch {
      // localStorage no disponible → el estado solo vale para esta visita
    }
  }

  function closeMobile() {
    mobileOpen = false;
  }

  const navItems = [
    { href: '/admin', label: 'Dashboard', icon: 'lucide:layout-dashboard' },
    { href: '/admin/hero', label: 'Hero', icon: 'lucide:sparkles' },
    { href: '/admin/experience', label: 'Experiencia', icon: 'lucide:briefcase' },
    { href: '/admin/projects', label: 'Proyectos', icon: 'lucide:folder-kanban' },
    { href: '/admin/sectors', label: 'Sectores', icon: 'lucide:layout-list' },
    { href: '/admin/testimonials', label: 'Testimonios', icon: 'lucide:message-square-quote' },
    { href: '/admin/site-settings', label: 'Configuración', icon: 'lucide:settings' },
    { type: 'divider' },
    { href: '/admin/radar', label: 'Radar', icon: 'lucide:satellite-dish' },
  ];

  function isActive(href: string): boolean {
    if (href === '/admin') return currentPath === '/admin';
    return currentPath.startsWith(href);
  }
</script>

<!-- ── Móvil: backdrop del drawer ─────────────────────────────── -->
{#if mobileOpen}
  <div
    class="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm md:hidden"
    role="presentation"
    on:click={closeMobile}
  ></div>
{/if}

<!-- ── Sidebar ───────────────────────────────────────────────────
     Móvil: fixed + translate-x (drawer). Desktop: relative en flujo. -->
<aside
  class:translate-x-0={mobileOpen}
  class="
    z-50 flex flex-col bg-zinc-900
    transition-all duration-300
    fixed inset-y-0 left-0 w-72 -translate-x-full md:translate-x-0
    md:sticky md:top-0 md:inset-auto md:w-auto md:h-screen md:shadow-none
    {collapsed ? 'md:w-16' : 'md:w-60'}
  "
>
  <!-- Botón toggle (solo desktop) -->
  <button
    on:click={toggle}
    class="
      hidden md:block
      absolute -right-3 top-6 z-10
      bg-zinc-800 border border-zinc-700 rounded-full p-1
      text-zinc-400 hover:text-amber-400 hover:border-amber-400
      transition-colors duration-200
    "
    aria-label={collapsed ? 'Expandir menú' : 'Colapsar menú'}
  >
    {#if collapsed}
      <Icon icon="lucide:chevron-right" width={14} height={14} />
    {:else}
      <Icon icon="lucide:chevron-left" width={14} height={14} />
    {/if}
  </button>

  <!-- Botón cerrar (solo móvil) -->
  <button
    on:click={closeMobile}
    class="
      md:hidden absolute top-5 right-4 z-10
      text-zinc-400 hover:text-white text-xl
    "
    aria-label="Cerrar menú"
  >
    ✕
  </button>

  <!-- Logo / nombre del sitio -->
  <div class="flex items-center gap-3 px-4 py-5 border-b border-zinc-800">
    <div
      class="
        w-8 h-8 rounded-lg flex-shrink-0
        bg-gradient-to-br from-amber-400 to-orange-500
        flex items-center justify-center
        text-zinc-900 font-bold text-sm
      "
    >
      H
    </div>
    {#if !collapsed || mobileOpen}
      <div class="overflow-hidden">
        <p class="text-sm font-semibold text-zinc-100 truncate">El Rincón de Harco</p>
        <p class="text-xs text-zinc-500">Panel admin</p>
      </div>
    {/if}
  </div>

  <!-- Links de navegación (scroll interno si no entran; el botón de abajo queda visible) -->
  <nav class="flex-1 min-h-0 overflow-y-auto overscroll-contain py-4 space-y-1 px-2">
    {#each navItems as item}
      {#if item.type === 'divider'}
        <div class="h-px bg-zinc-800 my-2 mx-2"></div>
      {:else}
        {@const active = isActive(item.href)}
        <div class="relative group">
          <a
            href={item.href}
            class="
              flex items-center gap-3 px-2 py-2.5 rounded-lg
              transition-all duration-200 border-l-2
              {active
              ? 'bg-zinc-800 text-amber-400 border-amber-400'
              : 'text-zinc-400 hover:bg-zinc-800 hover:text-amber-400 border-transparent'}
              {collapsed ? 'justify-center' : ''}
            "
          >
            <Icon icon={item.icon} width={18} height={18} class="flex-shrink-0" />
            {#if !collapsed || mobileOpen}
              <span class="text-sm font-medium truncate">{item.label}</span>
            {/if}
          </a>

          {#if collapsed && !mobileOpen}
            <span
              class="
                absolute left-full top-1/2 -translate-y-1/2 ml-2 px-2 py-1
                rounded-md bg-zinc-800 text-zinc-100 text-xs whitespace-nowrap
                opacity-0 group-hover:opacity-100 pointer-events-none
                transition-opacity duration-150 z-50
              "
            >
              {item.label}
            </span>
          {/if}
        </div>
      {/if}
    {/each}
  </nav>

  <!-- Botón volver al sitio -->
  <div class="px-2 py-4 border-t border-zinc-800">
    <div class="relative group">
      <a
        href="/"
        on:click={closeMobile}
        class="
          flex items-center gap-3 px-2 py-2.5 rounded-lg
          text-zinc-400 hover:bg-zinc-800 hover:text-amber-400
          transition-all duration-200
          {collapsed ? 'justify-center' : ''}
        "
      >
        <Icon icon="lucide:external-link" width={18} height={18} class="flex-shrink-0" />
        {#if !collapsed || mobileOpen}
          <span class="text-sm font-medium">Volver al sitio</span>
        {/if}
      </a>

      {#if collapsed && !mobileOpen}
        <span
          class="
            absolute left-full top-1/2 -translate-y-1/2 ml-2 px-2 py-1
            rounded-md bg-zinc-800 text-zinc-100 text-xs whitespace-nowrap
            opacity-0 group-hover:opacity-100 pointer-events-none
            transition-opacity duration-150 z-50
          "
        >
          Volver al sitio
        </span>
      {/if}
    </div>
  </div>
</aside>
