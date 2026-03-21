<script lang="ts">
  import { onMount } from 'svelte';
  import { ExternalLink, Github, Layers, Lock, Calendar } from 'lucide-svelte';
  import { fetchApi } from '$lib/config';
  import type { ProjectResponse } from '$lib/types';
  import { listenForDataChange } from '$lib/dataEvents';

  let items: ProjectResponse[] = [];
  let loading = true;

  async function loadData() {
    try {
      items = await fetchApi<ProjectResponse[]>('/api/v1/projects/');
    } catch {
      items = [];
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    await loadData();

    // Escuchar cambios desde el admin
    const cleanup = listenForDataChange('projects', async () => {
      loading = true;
      await loadData();
    });

    return cleanup;
  });

  function getIcon(iconName: string, size: number = 20) {
    const iconMap: Record<string, any> = {
      Layers,
      Lock,
      Calendar,
      ExternalLink,
      Github,
    };
    return iconMap[iconName];
  }
</script>

<section id="proyectos" class="py-24 bg-zinc-900 text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-16">
      <h2 class="text-3xl md:text-5xl font-bold mb-4">
        Proyectos <span class="text-amber-400">Destacados</span>
      </h2>
      <p class="text-gray-400 max-w-2xl mx-auto text-lg">
        Soluciones reales que demuestran la capacidad de entrega y calidad técnica.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {#if loading}
        <!-- Loading skeleton -->
        {#each Array(6) as _}
          <div class="animate-pulse">
            <div class="h-48 bg-zinc-800 rounded-t-2xl"></div>
            <div class="p-6 bg-black border border-white/10 rounded-b-2xl">
              <div class="h-6 bg-zinc-700 rounded mb-2"></div>
              <div class="h-4 bg-zinc-700 rounded mb-4"></div>
              <div class="flex gap-2 mb-4">
                <div class="h-6 w-16 bg-zinc-700 rounded-full"></div>
                <div class="h-6 w-16 bg-zinc-700 rounded-full"></div>
              </div>
            </div>
          </div>
        {/each}
      {:else if items.length === 0}
        <div class="col-span-full text-center py-8">
          <p class="text-zinc-500">No hay proyectos registrados</p>
        </div>
      {:else}
        {#each items as project, index}
          <div
            class="group bg-black border border-white/10 rounded-2xl overflow-hidden hover:border-amber-500/30 transition-all duration-500 hover:shadow-[0_0_30px_-5px_rgba(251,191,36,0.15)] flex flex-col h-full"
          >
            <!-- Image Container -->
            <div class="relative h-48 overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-tr {project.color} opacity-60 z-10"></div>
              <img
                src={project.image_url ||
                  'https://images.unsplash.com/photo-1762803841043-bee9f5691411?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBmdXJuaXR1cmUlMjB1cGhvbHN0ZXJ5JTIwd29ya3Nob3B8ZW58MXx8fHwxNzcwNDgzNjg3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral'}
                alt={project.title}
                class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
              />
              <div
                class="absolute top-4 right-4 z-20 bg-black/50 backdrop-blur-md p-2 rounded-lg border border-white/10 text-white"
              >
                <svelte:component this={getIcon(project.icon_name)} size={20} />
              </div>
            </div>

            <!-- Content -->
            <div class="p-6 flex-1 flex flex-col">
              <h3
                class="text-xl font-bold text-white mb-2 group-hover:text-amber-400 transition-colors"
              >
                {project.title}
              </h3>
              <p class="text-gray-400 mb-6 text-sm leading-relaxed flex-1">
                {project.description}
              </p>

              <!-- Tags -->
              <div class="flex flex-wrap gap-2 mb-6">
                {#each project.tags as tag}
                  <span
                    class="px-3 py-1 text-xs font-medium rounded-full bg-white/5 border border-white/10 text-gray-300"
                  >
                    {tag}
                  </span>
                {/each}
              </div>

              <!-- Actions -->
              <div class="flex items-center gap-4 pt-4 border-t border-white/5 mt-auto">
                {#if project.demo_url}
                  <a
                    href={project.demo_url}
                    target="_blank"
                    class="flex items-center gap-2 text-sm font-medium text-white hover:text-amber-400 transition-colors"
                  >
                    <ExternalLink size={16} /> Ver Demo
                  </a>
                {/if}
                {#if project.github_url}
                  <a
                    href={project.github_url}
                    target="_blank"
                    class="flex items-center gap-2 text-sm font-medium text-gray-400 hover:text-white transition-colors"
                  >
                    <Github size={16} /> Código
                  </a>
                {/if}
              </div>
            </div>
          </div>
        {/each}
      {/if}
    </div>
  </div>
</section>
