<script lang="ts">
  import { onMount } from 'svelte';
  // 1. IMPORTANTE: Agregamos los iconos que faltaban
  import {
    Github,
    Linkedin,
    Mail,
    Twitter,
    MapPin, // <--- Faltaba
    Award, // <--- Faltaba
    Briefcase, // <--- Faltaba
  } from 'lucide-svelte';

  import { fetchApi } from '$lib/config';
  import type { AboutResponse } from '$lib/types';
  import { listenForDataChange } from '$lib/dataEvents';

  let data: AboutResponse | null = null;
  let loading = true;

  async function loadData() {
    try {
      data = await fetchApi<AboutResponse>('/api/v1/abouts/latest/');
    } catch (err) {
      console.error('Error cargando About:', err);
      data = null;
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadData();

    // 2. Escuchar cambios desde el admin
    // Guardamos la función de limpieza para que Svelte la ejecute al destruir el componente
    const cleanup = listenForDataChange('about', async () => {
      loading = true;
      await loadData();
    });

    return () => {
      cleanup();
    };
  });
</script>

<section id="sobre-mi" class="py-20 bg-zinc-900 text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <div class="relative">
        <div class="relative h-[500px] w-full rounded-2xl overflow-hidden shadow-2xl group">
          <img
            src={data?.image_url ||
              'https://images.unsplash.com/photo-1631624220291-8f191fbdb543?q=80&w=1080'}
            alt="Hernan Arango Cortes"
            class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
          />
          <div
            class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-60"
          ></div>
          <div class="absolute bottom-6 left-6 text-white">
            <p class="flex items-center gap-2 text-amber-400 font-medium">
              <MapPin size={18} />
              {data?.location || 'Avilés, Asturias, España'}
            </p>
          </div>
        </div>

        <div
          class="absolute -bottom-6 -right-6 w-48 h-48 bg-amber-500/10 border border-amber-500/30 rounded-2xl -z-10 hidden lg:block"
        ></div>
      </div>

      <div class="space-y-6">
        <h2 class="text-3xl md:text-4xl font-bold">
          <span class="text-amber-400">{data?.years_experience || '14+ Años'}</span> de Trayectoria Profesional
        </h2>

        <div class="space-y-4 text-gray-300 leading-relaxed">
          <p>{data?.description || ''}</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
          <div
            class="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-amber-500/50 transition-colors"
          >
            <Award class="text-amber-400 mb-2" size={24} />
            <h3 class="font-semibold text-white">{data?.leadership_title || 'Liderazgo'}</h3>
            <p class="text-sm text-gray-400">
              {data?.leadership_desc || 'Formación de equipos...'}
            </p>
          </div>

          <div
            class="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-amber-500/50 transition-colors"
          >
            <Briefcase class="text-amber-400 mb-2" size={24} />
            <h3 class="font-semibold text-white">{data?.experience_title || 'Experiencia'}</h3>
            <p class="text-sm text-gray-400">{data?.experience_desc || 'Más de una década...'}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
