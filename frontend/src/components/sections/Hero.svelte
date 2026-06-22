<script lang="ts">
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { fetchApi } from '$lib/config';
  import type { HeroResponse } from '$lib/types';
  import { listenForDataChange } from '$lib/dataEvents';
  import { fallbackHero } from '$lib/fallback-data';

  // ── Estado inicial: siempre con datos (fallback) ─────────────
  // La API actualiza en segundo plano. Si falla, los datos estáticos persisten.
  let data: HeroResponse = fallbackHero;
  let hydrated = false;

  // Función para forzar la descarga en URLs de Cloudinary
  const getDownloadUrl = (url: string | null | undefined) => {
    if (!url) return '#';
    if (url.includes('cloudinary.com')) {
      if (url.includes('fl_attachment:')) return url;
      if (url.includes('/fl_attachment/')) return url;
      return url.replace('/upload/', '/upload/fl_attachment/');
    }
    return url;
  };

  async function loadData() {
    try {
      const response = await fetchApi<HeroResponse | HeroResponse[]>('/api/v1/heroes/latest/');
      const fresh = Array.isArray(response) ? response[0] : response;
      if (fresh) data = fresh;
    } catch {
      // fallback ya está como estado inicial — no pasa nada
    }
  }

  onMount(async () => {
    hydrated = true;
    await loadData();

    // Escuchar cambios desde el admin
    const cleanup = listenForDataChange('hero', async () => {
      await loadData();
    });

    return cleanup;
  });
</script>

<section
  id="inicio"
  class="relative min-h-screen flex items-center justify-center overflow-hidden bg-black text-white"
  class:hydrated={hydrated}
>
  <div class="absolute inset-0 z-0">
    {#if data.background_image}
      <img
        src={data.background_image}
        alt="Background"
        class="w-full h-full object-cover opacity-20 transition-opacity duration-1000"
      />
    {:else}
      <img
        src="https://images.unsplash.com/photo-1761599821310-da0d6356b4f3?q=80&w=1080"
        alt="Default Background"
        class="w-full h-full object-cover opacity-10"
      />
    {/if}
    <div class="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black"></div>
  </div>

  <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
    <div class="animate-in fade-in slide-in-from-bottom-8 duration-1000">
      <h2 class="text-amber-500 font-medium tracking-wide text-lg mb-4 uppercase">
        {data.title}
      </h2>
      <h1 class="text-5xl md:text-7xl font-bold tracking-tight mb-6 text-white">
        {data.subtitle}
      </h1>
      <p class="max-w-2xl mx-auto text-xl text-gray-300 mb-10 leading-relaxed">
        {data.description}
      </p>

      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <a
          href="#contact"
          class="inline-flex items-center px-8 py-3 border border-transparent text-base font-bold rounded-full text-black bg-amber-400 hover:bg-amber-500 transition-all shadow-[0_0_20px_rgba(251,191,36,0.3)] hover:scale-105 active:scale-95"
        >
          {data.contact_button_text}
          <Icon icon="lucide:arrow-right" class="ml-2 h-5 w-5" />
        </a>

        {#if data.cv_url}
          <a
            href={getDownloadUrl(data.cv_url)}
            target="_blank"
            rel="noopener noreferrer"
            download
            class="inline-flex items-center px-8 py-3 border border-white/20 text-base font-medium rounded-full text-white hover:bg-white/10 transition-all backdrop-blur-sm hover:border-amber-400/50 group"
          >
            {data.cv_button_text}
            <Icon
              icon="lucide:download"
              class="ml-2 h-5 w-5 group-hover:translate-y-0.5 transition-transform"
            />
          </a>
        {/if}
      </div>
    </div>
  </div>

  <div
    class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce opacity-50 hover:opacity-100 transition-opacity"
  >
    <div class="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center pt-2">
      <div class="w-1 h-3 bg-amber-400 rounded-full"></div>
    </div>
  </div>
</section>
