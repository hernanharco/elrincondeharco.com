<script lang="ts">
  import { Menu, X } from 'lucide-svelte';

  // Estado para controlar el menú móvil
  let isOpen = false;

  const links = [
    { name: 'Inicio', href: '#inicio' },
    { name: 'Sobre Mí', href: '#sobre-mi' },
    { name: 'Stack', href: '#stack' },
    { name: 'Proyectos', href: '#proyectos' },
    { name: 'Pasiones', href: '#pasiones' },
  ];

  function toggleMenu() {
    isOpen = !isOpen;
  }

  function closeMenu() {
    isOpen = false;
  }
</script>

<nav class="fixed w-full z-50 bg-black/80 backdrop-blur-md border-b border-white/10 text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <div class="flex-shrink-0">
        <span
          class="text-xl font-bold bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent cursor-pointer"
        >
          HAC
        </span>
      </div>

      <div class="hidden md:block">
        <div class="ml-10 flex items-baseline space-x-4">
          {#each links as link}
            <a
              href={link.href}
              class="hover:text-amber-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-300"
            >
              {link.name}
            </a>
          {/each}
        </div>
      </div>

      <div class="-mr-2 flex md:hidden">
        <button
          on:click={toggleMenu}
          type="button"
          class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
        >
          <span class="sr-only">Abrir menú</span>
          {#if isOpen}
            <X size={24} />
          {:else}
            <Menu size={24} />
          {/if}
        </button>
      </div>
    </div>
  </div>

  {#if isOpen}
    <div class="md:hidden bg-black/95 backdrop-blur-xl border-b border-white/10">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        {#each links as link}
          <a
            href={link.href}
            on:click={closeMenu}
            class="text-gray-300 hover:text-amber-400 block px-3 py-2 rounded-md text-base font-medium transition-colors"
          >
            {link.name}
          </a>
        {/each}
      </div>
    </div>
  {/if}
</nav>
