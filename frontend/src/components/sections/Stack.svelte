<script lang="ts">
  import { onMount } from 'svelte';
  import {
    Zap,
    Rocket,
    Database,
    Server,
    Atom,
    LayoutTemplate,
    GitBranch,
    Github,
    Triangle,
    Cloud,
    Send,
    BrainCircuit,
    Gauge,
    Layers,
    Monitor,
    HardDrive,
    Settings,
    Container,
    Code2,
    FileCode2,
    Palette,
    Lock,
    Globe,
    Terminal,
  } from 'lucide-svelte';
  import { fetchApi } from '$lib/config';
  import type { StackResponse } from '$lib/types';
  import { listenForDataChange } from '$lib/dataEvents';

  let activeCategory = 'Todos';
  let items: StackResponse[] = [];
  let loading = true;

  const categories = ['Todos', 'Frontend', 'Backend', 'DevOps', 'Herramientas'];

  async function loadData() {
    try {
      items = await fetchApi<StackResponse[]>('/api/v1/stacks/');
    } catch {
      items = [];
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadData();

    // Escuchar cambios desde el admin
    const cleanup = listenForDataChange('stack', async () => {
      loading = true;
      await loadData();
    });

    return () => {
      cleanup();
    };
  });

  $: filteredTech =
    activeCategory === 'Todos' ? items : items.filter((t) => t.category === activeCategory);

  function getCategoryIcon(cat: string) {
    switch (cat) {
      case 'Frontend':
        return Monitor;
      case 'Backend':
        return HardDrive;
      case 'DevOps':
        return Layers;
      case 'Herramientas':
        return Settings;
      default:
        return Layers;
    }
  }

  function getIcon(iconName: string, size: number = 24) {
    const iconMap: Record<string, any> = {
      Globe,
      Palette,
      FileCode2,
      Atom,
      Rocket,
      LayoutTemplate,
      Terminal,
      Zap,
      Layers,
      Server,
      Lock,
      Database,
      Container,
      GitBranch,
      Github,
      Triangle,
      Cloud,
      Code2,
      Send,
      BrainCircuit,
      Gauge,
      Monitor,
      HardDrive,
      Settings,
    };
    return iconMap[iconName];
  }

  function setCategory(cat: string) {
    activeCategory = cat;
  }
</script>

<section id="stack" class="py-24 bg-zinc-950 text-white relative">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
      <div class="space-y-2">
        <h2 class="text-3xl md:text-5xl font-bold">
          Arsenal <span class="text-amber-400">Técnico</span>
        </h2>
        <p class="text-gray-400 max-w-lg text-lg">
          Herramientas modernas para soluciones rápidas y escalables.
        </p>
      </div>

      <!-- Category Filter -->
      <div class="flex flex-wrap gap-2">
        {#each categories as cat}
          <button
            on:click={() => setCategory(cat)}
            class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 flex items-center gap-2 border {activeCategory ===
            cat
              ? 'bg-amber-400 text-black border-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.4)]'
              : 'bg-white/5 text-gray-400 border-white/10 hover:border-white/30 hover:text-white'}"
          >
            {#if cat !== 'Todos'}
              <svelte:component this={getCategoryIcon(cat)} size={16} />
            {/if}
            {cat}
          </button>
        {/each}
      </div>
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      {#if loading}
        <!-- Loading skeleton -->
        {#each Array(20) as _}
          <div class="animate-pulse">
            <div class="h-32 bg-zinc-800 rounded-xl"></div>
          </div>
        {/each}
      {:else if filteredTech.length === 0}
        <div class="col-span-full text-center py-8">
          <p class="text-zinc-500">No hay tecnologías en esta categoría</p>
        </div>
      {:else}
        {#each filteredTech as tech (tech.id)}
          <div
            class="group relative p-4 h-32 flex flex-col justify-between bg-zinc-900/50 rounded-xl border border-white/5 transition-all duration-300 hover:-translate-y-1 {tech.border} {tech.glow}"
          >
            <div class="flex justify-between items-start">
              <div class="p-2 rounded-lg bg-white/5 {tech.color}">
                <svelte:component this={getIcon(tech.icon)} size={24} />
              </div>
              <span class="text-[10px] uppercase tracking-wider text-gray-500 font-semibold">
                {tech.category}
              </span>
            </div>
            <div>
              <h3 class="font-bold text-white tracking-wide">{tech.name}</h3>
              <p class="text-xs text-gray-400 mt-1 line-clamp-1">{tech.description}</p>
            </div>
          </div>
        {/each}
      {/if}
    </div>

    <div class="mt-12 text-center">
      <p class="text-zinc-500 text-sm">
        transformando arquitecturas complejas en experiencias digitales impecables y escalables.
      </p>
    </div>
  </div>
</section>
