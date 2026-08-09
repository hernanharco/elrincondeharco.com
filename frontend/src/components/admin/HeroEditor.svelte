<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { HeroResponse } from '$lib/types';
  import { fallbackHero } from '$lib/fallback-data';
  import { dispatchDataChange } from '$lib/dataEvents';
  import Icon from '@iconify/svelte';
  import HtmlEditor from '../ui/HtmlEditor.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  let data: HeroResponse | null = null;
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // Estados para los campos del formulario
  let title = '';
  let subtitle = '';
  let description = '';
  let primary_button_text = '';
  let contact_button_text = '';

  function populateFields(src: HeroResponse) {
    data = src;
    title = src.title ?? '';
    subtitle = src.subtitle ?? '';
    description = src.description ?? '';
    primary_button_text = src.primary_button_text ?? '';
    contact_button_text = src.contact_button_text ?? '';
  }

  onMount(async () => {
    try {
      const res = await fetchApi<HeroResponse>('/api/v1/heroes/latest/');
      if (res) {
        populateFields(res);
      } else {
        // API respondió pero sin datos — usamos fallback
        populateFields(fallbackHero);
      }
    } catch (err) {
      // API no disponible — usamos fallback para que se vean los datos igual
      populateFields(fallbackHero);
      message = 'Usando datos de respaldo (API no disponible)';
      messageType = 'error';
    } finally {
      loading = false;
    }
  });

  async function handleSubmit() {
    if (!data) return;
    saving = true;
    message = '';

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('subtitle', subtitle);
      formData.append('description', description);
      formData.append('primary_button_text', primary_button_text);
      formData.append('contact_button_text', contact_button_text);

      const res = await fetch(`${API}/api/v1/heroes/${data.id}`, {
        method: 'PUT',
        body: formData,
      });

      if (!res.ok) throw new Error('Error en la respuesta del servidor');

      const updatedData = await res.json();
      data = updatedData;
      message = '¡Hero actualizado con éxito!';
      messageType = 'success';

      dispatchDataChange('hero', 'update', updatedData);
    } catch (err) {
      message = 'No se pudo guardar la información';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }
</script>

<div class="p-6 md:p-10">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-zinc-100 mb-2">Hero — Modo Cliente</h1>
      <p class="text-sm text-zinc-500">Editá el contenido del Hero que ven tus clientes en la página principal.</p>
    </div>

    {#if loading}
      <div class="flex items-center justify-center p-12 text-zinc-400 gap-3">
        <Icon icon="lucide:loader-2" class="animate-spin w-5 h-5 text-amber-500" />
        <span class="text-sm font-medium">Cargando Hero...</span>
      </div>
    {:else}
      <form
        on:submit|preventDefault={handleSubmit}
        class="space-y-8 animate-in fade-in duration-500"
      >
        <div class="space-y-6">
          <h3 class="text-xs font-bold uppercase tracking-widest text-zinc-500">Contenido</h3>

          <div class="grid grid-cols-1 gap-6">
            <div>
              <label for="title" class="block text-sm font-medium text-zinc-400 mb-2"
                >Frase Superior (tagline)</label
              >
              <input
                id="title"
                type="text"
                bind:value={title}
                required
                class="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none"
                placeholder="Ej: Soluciones Digitales para tu Negocio"
              />
            </div>

            <div>
              <HtmlEditor
                bind:value={subtitle}
                label="Título Principal"
                placeholder='Ej: El Rincom...'
              />
            </div>

            <div>
              <label for="description" class="block text-sm font-medium text-zinc-400 mb-2"
                >Descripción (usá Enter para saltos de línea)</label
              >
              <textarea
                id="description"
                bind:value={description}
                rows={4}
                class="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none resize-none"
                placeholder="Creo la web que tu negocio necesita para crecer.&#10;Sitios que venden · Sistemas que automatizan · Experiencias que enamoran"
              ></textarea>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-5 rounded-xl bg-zinc-900/30 border border-zinc-800/50">
          <div>
            <label
              for="primary_btn"
              class="block text-xs font-bold text-zinc-500 mb-2 uppercase tracking-wider"
              >Botón Principal (naranja)</label
            >
            <p class="text-[11px] text-zinc-600 mb-3">Redirige a #experiencia (rubros)</p>
            <input
              id="primary_btn"
              type="text"
              bind:value={primary_button_text}
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-500 outline-none"
              placeholder="Ver mi rubro"
            />
          </div>

          <div>
            <label
              for="contact_btn"
              class="block text-xs font-bold text-zinc-500 mb-2 uppercase tracking-wider"
              >Botón "Contacto"</label
            >
            <p class="text-[11px] text-zinc-600 mb-3">Redirige a la sección #contacto</p>
            <input
              id="contact_btn"
              type="text"
              bind:value={contact_button_text}
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-500 outline-none"
              placeholder="Contacto"
            />
          </div>
        </div>

        <div class="flex flex-col sm:flex-row items-center gap-6 pt-4">
          <button
            type="submit"
            disabled={saving}
            class="w-full sm:w-auto px-10 py-4 rounded-xl font-black text-zinc-900
               bg-gradient-to-r from-amber-400 to-orange-500
               hover:from-amber-300 hover:to-orange-400
               disabled:opacity-50 disabled:cursor-not-allowed
               transition-all duration-300 flex items-center justify-center gap-2 shadow-xl shadow-amber-600/10"
          >
            {#if saving}
              <Icon icon="lucide:loader-2" class="animate-spin w-5 h-5" />
              Guardando...
            {:else}
              <Icon icon="lucide:save" class="w-5 h-5" />
              Guardar Cambios
            {/if}
          </button>

          {#if message}
            <div
              class="flex items-center gap-2 {messageType === 'success'
                ? 'text-emerald-400'
                : 'text-red-400'} animate-bounce"
            >
              <span class="text-sm font-bold">{message}</span>
            </div>
          {/if}
        </div>
      </form>
    {/if}
  </div>
</div>
