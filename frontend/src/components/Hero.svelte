<script lang="ts">
  import { onMount } from 'svelte';
  import { Github, Download, ArrowRight } from 'lucide-svelte';
  import { fetchApi } from '$lib/config';
  import type { HeroResponse } from '$lib/types';
  import { listenForDataChange } from '$lib/dataEvents';

  let data: HeroResponse | null = null;
  let loading = true;

  async function loadData() {
    try {
      data = await fetchApi<HeroResponse>('/api/v1/heroes/latest/');
    } catch {
      // mantener null — el template maneja el estado vacío
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    await loadData();

    // Escuchar cambios desde el admin
    const cleanup = listenForDataChange('hero', async () => {
      loading = true;
      await loadData();
    });

    return cleanup;
  });
</script>

<section
  id="inicio"
  class="relative min-h-screen flex items-center justify-center overflow-hidden bg-black text-white"
>
  <!-- Background Image with Overlay -->
  <div class="absolute inset-0 z-0">
    <img
      src={data?.background_image ||
        'https://images.unsplash.com/photo-1761599821310-da0d6356b4f3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBhYnN0cmFjdCUyMHRlY2hub2xvZ3klMjBiYWNrZ3JvdW5kJTIwY29kZSUyMGRhcmt8ZW58MXx8fHwxNzcwNDgwNjI4fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral'}
      alt="Background"
      class="w-full h-full object-cover opacity-20"
    />
    <div class="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black"></div>
  </div>

  <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
    <div>
      <h2 class="text-amber-500 font-medium tracking-wide text-lg mb-4 uppercase">
        Desarrollador Full Stack
      </h2>
      <h1 class="text-5xl md:text-7xl font-bold tracking-tight mb-6 text-white">
        Hernan Arango Cortes
      </h1>
      <p class="max-w-2xl mx-auto text-xl text-gray-300 mb-10">
        {data?.description ||
          'Transformando 14+ años de experiencia en liderazgo y análisis en soluciones tecnológicas innovadoras. Mi familia es mi motor, la tecnología mi pasión, y el emprendimiento mi camino hacia el futuro.'}
      </p>

      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a
          href="#contact"
          class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-black bg-amber-400 hover:bg-amber-500 transition-all shadow-[0_0_20px_rgba(251,191,36,0.3)]"
        >
          {data?.contact_button_text || 'Contactar'}
          <ArrowRight class="ml-2 h-5 w-5" />
        </a>
        <button
          class="inline-flex items-center px-8 py-3 border border-white/20 text-base font-medium rounded-full text-white hover:bg-white/10 transition-all backdrop-blur-sm"
        >
          {data?.cv_button_text || 'Descargar CV'}
          <Download class="ml-2 h-5 w-5" />
        </button>
      </div>
    </div>
  </div>

  <!-- Decorative Elements -->
  <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce">
    <div class="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center pt-2">
      <div class="w-1 h-3 bg-amber-400 rounded-full"></div>
    </div>
  </div>
</section>
