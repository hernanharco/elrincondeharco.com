<script lang="ts">
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { fetchApi } from '$lib/config';
  import { listenForDataChange } from '$lib/dataEvents';
  import type { ShowroomResponse } from '$lib/types';
  import { fallbackShowrooms } from '$lib/fallback-data';

  let items: ShowroomResponse[] = [];
  let loading = true;

  async function loadData() {
    try {
      items = await fetchApi<ShowroomResponse[]>('/api/v1/showrooms/');
    } catch {
      items = fallbackShowrooms;
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadData();

    // Escuchar cambios desde el admin
    const cleanup = listenForDataChange('showroom', async () => {
      loading = true;
      await loadData();
    });

    return cleanup;
  });

  function launchPrototype(url: string | null) {
    if (url) {
      window.open(url, '_blank');
    }
  }
</script>

<section class="py-20 px-6 md:px-10 bg-zinc-950">
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-16">
      <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">
        Bocetos de <span class="text-amber-400">Innovacción</span>
      </h1>
      <p class="text-xl text-zinc-400 max-w-2xl mx-auto">
        Explora mis diseños y prototipos funcionales ya desplegados en producción
      </p>
    </div>

    <!-- Loading State -->
    {#if loading}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each Array(6) as _}
          <div class="animate-pulse">
            <!-- Skeleton Card -->
            <div class="bg-zinc-900 rounded-2xl overflow-hidden border border-zinc-800">
              <!-- Image Skeleton -->
              <div class="h-48 bg-zinc-800"></div>
              <!-- Content Skeleton -->
              <div class="p-6 space-y-4">
                <div class="h-4 bg-zinc-800 rounded w-3/4"></div>
                <div class="space-y-2">
                  <div class="h-3 bg-zinc-800 rounded"></div>
                  <div class="h-3 bg-zinc-800 rounded w-5/6"></div>
                </div>
                <div class="h-10 bg-zinc-800 rounded"></div>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {:else if items.length === 0}
      <!-- Empty State -->
      <div class="text-center py-20 border-2 border-dashed border-zinc-800 rounded-2xl">
        <div class="max-w-md mx-auto space-y-6">
          <div
            class="w-20 h-20 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center text-white mx-auto"
          >
            <Icon icon="lucide:rocket" width={40} height={40} />
          </div>
          <div>
            <h3 class="text-2xl font-bold text-white mb-2">Próximamente</h3>
            <p class="text-zinc-400">
              Estoy trabajando en nuevos prototipos. ¡Vuelve pronto para ver los últimos diseños!
            </p>
          </div>
        </div>
      </div>
    {:else}
      <!-- Grid de Prototipos -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each items as item (item.id)}
          <div
            class="group relative bg-zinc-900 rounded-2xl overflow-hidden border border-zinc-800 hover:border-amber-400/50 transition-all duration-500 hover:scale-[1.02] hover:shadow-2xl hover:shadow-amber-500/10"
          >
            <!-- Imagen -->
            <div class="relative h-48 overflow-hidden">
              {#if item.image_url}
                <img
                  src={item.image_url}
                  alt={item.title}
                  class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <!-- Gradient Overlay -->
                <div
                  class="absolute inset-0 bg-gradient-to-t from-zinc-900 via-zinc-900/50 to-transparent"
                ></div>
              {:else}
                <!-- Placeholder con gradient -->
                <div
                  class="w-full h-full bg-gradient-to-br from-amber-500/20 to-orange-600/20 flex items-center justify-center"
                >
                  <div class="text-center space-y-3">
                    <div
                      class="mx-auto w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center text-white shadow-lg"
                    >
                      <Icon icon="lucide:rocket" width={32} height={32} />
                    </div>
                    <p class="text-amber-400 font-medium text-sm">Sin imagen</p>
                  </div>
                </div>
              {/if}

              <!-- Category Badge -->
              <div class="absolute top-4 left-4">
                <div
                  class="px-3 py-1 bg-amber-500/90 backdrop-blur-sm text-white text-sm font-medium rounded-full shadow-lg"
                >
                  {item.category}
                </div>
              </div>
            </div>

            <!-- Contenido -->
            <div class="p-6 space-y-4">
              <!-- Título -->
              <h3
                class="text-xl font-bold text-white group-hover:text-amber-400 transition-colors duration-300"
              >
                {item.title}
              </h3>

              <!-- Descripción -->
              <p class="text-zinc-400 text-sm leading-relaxed line-clamp-3">
                {item.description}
              </p>

              <!-- Botón -->
              {#if item.deploy_url}
                <button
                  on:click={() => launchPrototype(item.deploy_url)}
                  class="w-full py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white font-bold rounded-xl hover:from-amber-600 hover:to-orange-700 transition-all duration-300 shadow-lg hover:shadow-amber-500/25 flex items-center justify-center gap-2 group"
                >
                  <span>Lanzar Prototipo</span>
                  <Icon
                    icon="lucide:external-link"
                    width={16}
                    height={16}
                    class="transition-transform duration-300 group-hover:translate-x-1 group-hover:-translate-y-1"
                  />
                </button>
              {:else}
                <div
                  class="w-full py-3 bg-zinc-800 text-zinc-500 font-medium rounded-xl flex items-center justify-center gap-2 cursor-not-allowed"
                >
                  <Icon icon="lucide:lock" width={16} height={16} />
                  <span>No disponible</span>
                </div>
              {/if}
            </div>

            <!-- Hover Effect -->
            <div
              class="absolute inset-0 bg-gradient-to-t from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
            ></div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</section>

<style>
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
