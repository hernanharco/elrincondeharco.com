<svelte:options runes={false} />

<script lang="ts">
  import Icon from '@iconify/svelte';

  export let sections = [
    { href: '/admin/hero', label: 'Hero', description: 'Título y subtítulo principal' },
    { href: '/admin/projects', label: 'Proyectos', description: 'Galería de proyectos destacados' },
    { href: '/admin/sectors', label: 'Sectores', description: 'Rubros y asignación de proyectos' },
    { href: '/admin/testimonials', label: 'Testimonios', description: 'Lo que dicen los clientes' },
    { href: '/admin/showroom', label: 'Showroom', description: 'Prototipos y experimentos' },
    { href: '/admin/site-settings', label: 'Configuración', description: 'Nombre, redes, copyright' },
  ];
</script>

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  {#each sections as section}
    <a
      href={section.href}
      class="
        block p-5 rounded-xl bg-zinc-900 border border-zinc-800
        hover:border-amber-400 hover:bg-zinc-800
        transition-all duration-200 group
      "
    >
      <h2
        class="text-base font-semibold text-zinc-100 group-hover:text-amber-400 mb-1 transition-colors"
      >
        {section.label}
      </h2>
      <p class="text-sm text-zinc-500">{section.description}</p>
    </a>
  {/each}
</div>
