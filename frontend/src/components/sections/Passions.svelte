<script lang="ts">
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { fetchApi } from '$lib/config';
  import type { PassionResponse } from '$lib/types';
  import { listenForDataChange } from '$lib/dataEvents';
  import { fallbackPassion } from '$lib/fallback-data';

  // ── Estado inicial: siempre con datos (fallback) ─────────────
  let data: PassionResponse = fallbackPassion;

  async function loadData() {
    try {
      const fresh = await fetchApi<PassionResponse>('/api/v1/passions/latest/');
      if (fresh) data = fresh;
    } catch {
      // fallback ya está como estado inicial — no pasa nada
    }
  }

  onMount(async () => {
    await loadData();

    const cleanup = listenForDataChange('passions', async () => {
      await loadData();
    });

    return cleanup;
  });
</script>

<section id="pasiones" class="py-20 bg-zinc-900 text-white overflow-hidden">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
      <div class="order-2 lg:order-1 space-y-8">
        <h2 class="text-3xl md:text-5xl font-bold mb-6">
          Más allá del <span class="text-amber-400">Código</span>
        </h2>

        <p class="text-xl text-gray-300">
          {data.description}
        </p>

        <div class="space-y-6">
          <div class="flex items-start gap-4">
            <div class="p-3 bg-red-500/10 rounded-lg text-red-400">
              <Icon icon="lucide:heart" width={28} height={28} />
            </div>
            <div>
              <h3 class="text-xl font-semibold text-white mb-1">
                {data.family_title}
              </h3>
              <p class="text-gray-400">
                {data.family_desc}
              </p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="p-3 bg-indigo-500/10 rounded-lg text-indigo-400">
              <Icon icon="lucide:gamepad-2" width={28} height={28} />
            </div>
            <div>
              <h3 class="text-xl font-semibold text-white mb-1">
                {data.games_title}
              </h3>
              <p class="text-gray-400">
                {data.games_desc}
              </p>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="p-3 bg-amber-500/10 rounded-lg text-amber-400">
              <Icon icon="lucide:code" width={28} height={28} />
            </div>
            <div>
              <h3 class="text-xl font-semibold text-white mb-1">
                {data.coding_title}
              </h3>
              <p class="text-gray-400">
                {data.coding_desc}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="order-1 lg:order-2 relative">
        <div
          class="relative rounded-2xl overflow-hidden shadow-2xl rotate-3 hover:rotate-0 transition-transform duration-500"
        >
          <img
            src={data?.image_url ||
              'https://images.unsplash.com/photo-1758687126556-b2d1c32e4207?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aWRlbyUyMGdhbWVzJTIwY29udHJvbGxlciUyMGZhbWlseSUyMGxpdmluZyUyMHJvb218ZW58MXx8fHwxNzcwNDgwNjI4fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral'}
            alt="Family and Gaming"
            class="w-full h-[600px] object-cover"
          />
          <div
            class="absolute inset-0 bg-gradient-to-t from-zinc-900 via-transparent to-transparent"
          ></div>
        </div>
      </div>
    </div>
  </div>
</section>
