<script lang="ts">
  import { onMount } from 'svelte';
  import { Calendar, MapPin, Award, Briefcase } from 'lucide-svelte';
  import { fetchApi } from '$lib/config';
  import type { AboutResponse } from '$lib/types';

  let data: AboutResponse | null = null;
  let loading = true;

  onMount(async () => {
    try {
      data = await fetchApi<AboutResponse>('/api/v1/abouts/latest/');
    } catch {
      // mantener null — el template maneja el estado vacío
    } finally {
      loading = false;
    }
  });
</script>

<section id="sobre-mi" class="py-20 bg-zinc-900 text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <!-- Image Column -->
      <div class="relative">
        <div class="relative h-[500px] w-full rounded-2xl overflow-hidden shadow-2xl group">
          <img
            src={data?.image_url ||
              'https://images.unsplash.com/photo-1631624220291-8f191fbdb543?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBkZXZlbG9wZXIlMjBtYW4lMjBjb2RpbmclMjBvZmZpY2V8ZW58MXx8fHwxNzcwNDgwNjI4fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral'}
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
        <!-- Decorative box -->
        <div
          class="absolute -bottom-6 -right-6 w-48 h-48 bg-amber-500/10 border border-amber-500/30 rounded-2xl -z-10 hidden lg:block"
        ></div>
      </div>

      <!-- Text Column -->
      <div class="space-y-6">
        <h2 class="text-3xl md:text-4xl font-bold">
          <span class="text-amber-400">{data?.years_experience || '14+ Años'}</span> de Trayectoria Profesional
        </h2>

        <div class="space-y-4 text-gray-300 leading-relaxed">
          <p>
            Mi nombre es Hernan Arango Cortes. Hace aproximadamente 5 años que resido en
            <span class="text-white font-medium"> {data?.location || 'Avilés, Asturias'}</span>,
            donde me he especializado en las tecnologías más modernas para ofrecer los mejores
            servicios a mis futuros clientes.
          </p>

          <p>
            Mi carrera comenzó en Colombia a los 18 años. Durante 14 años trabajé en una empresa
            donde escalé posiciones hasta formar un equipo competitivo y ágil, al que con orgullo
            llamé el
            <span class="text-amber-400 font-bold"> "{data?.team_name || 'Equipo de Oro'}"</span>.
          </p>

          <p>
            Nos caracterizábamos por presentar soluciones rápidas y efectivas, una filosofía que
            mantengo hoy en día utilizando herramientas como FastAPI y Astro.
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
          <div
            class="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-amber-500/50 transition-colors"
          >
            <Award class="text-amber-400 mb-2" size={24} />
            <h3 class="font-semibold text-white">{data?.leadership_title || 'Liderazgo'}</h3>
            <p class="text-sm text-gray-400">
              {data?.leadership_desc || 'Formación de equipos de alto rendimiento.'}
            </p>
          </div>
          <div
            class="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-amber-500/50 transition-colors"
          >
            <Briefcase class="text-amber-400 mb-2" size={24} />
            <h3 class="font-semibold text-white">{data?.experience_title || 'Experiencia'}</h3>
            <p class="text-sm text-gray-400">
              {data?.experience_desc || 'Más de una década entregando soluciones.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
