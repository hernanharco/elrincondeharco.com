<script lang="ts">
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';

  export let currentPath: string = '';

  let collapsed = false;

  onMount(() => {
    collapsed = window.innerWidth < 768;
    window.addEventListener('resize', () => {
      if (window.innerWidth < 768) collapsed = true;
    });
  });

  function toggle() {
    collapsed = !collapsed;
  }

  const navItems = [
    { href: '/admin', label: 'Dashboard', icon: 'lucide:layout-dashboard' },
    { href: '/admin/hero', label: 'Hero', icon: 'lucide:sparkles' },
    { href: '/admin/about', label: 'About', icon: 'lucide:user' },
    { href: '/admin/stack', label: 'Stack', icon: 'lucide:code-2' },
    { href: '/admin/projects', label: 'Proyectos', icon: 'lucide:folder-kanban' },
    { href: '/admin/showroom', label: 'Showroom', icon: 'lucide:rocket' },
    { href: '/admin/passions', label: 'Pasiones', icon: 'lucide:heart' },
    { href: '/admin/footer', label: 'Footer', icon: 'lucide:mail' },
    { href: '/admin/site-settings', label: 'Configuración', icon: 'lucide:settings' },
  ];

  function isActive(href: string): boolean {
    if (href === '/admin') return currentPath === '/admin';
    return currentPath.startsWith(href);
  }
</script>

<aside
  class="
    relative flex flex-col bg-zinc-900 border-r border-zinc-800
    transition-all duration-300 min-h-screen
    {collapsed ? 'w-16' : 'w-60'}
  "
>
  <!-- Botón toggle -->
  <button
    on:click={toggle}
    class="
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
    {#if !collapsed}
      <div class="overflow-hidden">
        <p class="text-sm font-semibold text-zinc-100 truncate">El Rincón de Harco</p>
        <p class="text-xs text-zinc-500">Panel admin</p>
      </div>
    {/if}
  </div>

  <!-- Links de navegación -->
  <nav class="flex-1 py-4 space-y-1 px-2">
    {#each navItems as item}
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
          {#if !collapsed}
            <span class="text-sm font-medium truncate">{item.label}</span>
          {/if}
        </a>

        {#if collapsed}
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
    {/each}
  </nav>

  <!-- Botón volver al sitio -->
  <div class="px-2 py-4 border-t border-zinc-800">
    <div class="relative group">
      <a
        href="/"
        class="
          flex items-center gap-3 px-2 py-2.5 rounded-lg
          text-zinc-400 hover:bg-zinc-800 hover:text-amber-400
          transition-all duration-200
          {collapsed ? 'justify-center' : ''}
        "
      >
        <Icon icon="lucide:external-link" width={18} height={18} class="flex-shrink-0" />
        {#if !collapsed}
          <span class="text-sm font-medium">Volver al sitio</span>
        {/if}
      </a>

      {#if collapsed}
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
