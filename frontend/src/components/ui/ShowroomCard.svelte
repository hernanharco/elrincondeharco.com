<svelte:options runes={false} />

<script lang="ts">
  import Icon from '@iconify/svelte';
  
  export let title: string;
  export let description: string;
  export let category: string;
  export let deployUrl: string | null = null;
  export let imageUrl: string | null = null;
  export let featured = false;

  function handleVisitPrototype() {
    if (deployUrl) {
      window.open(deployUrl, '_blank');
    }
  }
</script>

<div 
  class={`
    relative group rounded-2xl overflow-hidden transition-all duration-500 transform hover:scale-[1.02] hover:shadow-2xl
    ${featured 
      ? 'bg-gradient-to-br from-amber-500/10 to-orange-600/10 border border-amber-400/30 hover:border-amber-400/50' 
      : 'bg-zinc-900/50 border border-zinc-800 hover:border-amber-400/30'
    }
  `}
>
  <!-- Image Section -->
  <div class="relative h-48 overflow-hidden">
    {#if imageUrl}
      <img 
        src={imageUrl} 
        alt={title}
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
      />
      <!-- Gradient Overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-zinc-900 via-zinc-900/50 to-transparent"></div>
    {:else}
      <!-- Placeholder with gradient -->
      <div class="w-full h-full bg-gradient-to-br from-amber-500/20 to-orange-600/20 flex items-center justify-center">
        <div class="text-center space-y-3">
          <div class="mx-auto w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center text-white shadow-lg">
            <Icon icon="lucide:rocket" width={32} height={32} />
          </div>
          <p class="text-amber-400 font-medium text-sm">Sin imagen</p>
        </div>
      </div>
    {/if}

    <!-- Category Badge -->
    <div class="absolute top-4 left-4">
      <div class="px-3 py-1 bg-amber-500/90 backdrop-blur-sm text-white text-sm font-medium rounded-full shadow-lg">
        {category}
      </div>
    </div>

    <!-- Featured Badge -->
    {#if featured}
      <div class="absolute top-4 right-4">
        <div class="px-3 py-1 bg-gradient-to-r from-amber-400 to-orange-500 text-white text-sm font-medium rounded-full shadow-lg flex items-center gap-1">
          <Icon icon="lucide:star" width={14} height={14} />
          Destacado
        </div>
      </div>
    {/if}
  </div>

  <!-- Content Section -->
  <div class="p-6 space-y-4">
    <!-- Title -->
    <h3 class="text-xl font-bold text-white group-hover:text-amber-400 transition-colors duration-300">
      {title}
    </h3>

    <!-- Description -->
    <p class="text-zinc-400 text-sm leading-relaxed line-clamp-3">
      {description}
    </p>

    <!-- Action Button -->
    {#if deployUrl}
      <button
        on:click={handleVisitPrototype}
        class="w-full py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white font-medium rounded-xl hover:from-amber-600 hover:to-orange-700 transition-all duration-300 shadow-lg hover:shadow-amber-500/25 flex items-center justify-center gap-2 group"
      >
        <span>Ver Prototipo</span>
        <Icon 
          icon="lucide:external-link" 
          width={16} 
          height={16} 
          class="transition-transform duration-300 group-hover:translate-x-1 group-hover:-translate-y-1" 
        />
      </button>
    {:else}
      <div class="w-full py-3 bg-zinc-800 text-zinc-500 font-medium rounded-xl flex items-center justify-center gap-2 cursor-not-allowed">
        <Icon icon="lucide:lock" width={16} height={16} />
        <span>No disponible</span>
      </div>
    {/if}
  </div>

  <!-- Hover Effects -->
  <div class="absolute inset-0 bg-gradient-to-t from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
</div>

<style>
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
