<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { HeroResponse } from '$lib/types';
  import ImageUpload from './ImageUpload.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  let data: HeroResponse | null = null;
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // un campo por cada campo del schema Create
  let title = '';
  let subtitle = '';
  let description = '';
  let background_image = '';
  let contact_button_text = '';
  let cv_button_text = '';
  let imageFile: File | null = null;

  onMount(async () => {
    try {
      data = await fetchApi<HeroResponse>('/api/v1/heroes/latest/');
      title = data.title ?? '';
      subtitle = data.subtitle ?? '';
      description = data.description ?? '';
      background_image = data.background_image ?? '';
      contact_button_text = data.contact_button_text ?? '';
      cv_button_text = data.cv_button_text ?? '';
    } catch {
      message = 'Error al cargar los datos';
      messageType = 'error';
    } finally {
      loading = false;
    }
  });

  function handleImageChange(e: CustomEvent<{ file: File | null; preview: string | null }>) {
    imageFile = e.detail.file;
  }

  async function handleSubmit() {
    if (!data) return;
    saving = true;
    message = '';

    try {
      // SIEMPRE FormData — nunca JSON
      const formData = new FormData();
      formData.append('title', title);
      formData.append('subtitle', subtitle);
      formData.append('description', description);
      formData.append('background_image', background_image);
      formData.append('contact_button_text', contact_button_text);
      formData.append('cv_button_text', cv_button_text);
      if (imageFile) formData.append('image', imageFile);
      // NO agregar Content-Type manualmente

      const res = await fetch(`${API}/api/v1/heroes/${data.id}`, {
        method: 'PUT',
        body: formData,
      });

      if (!res.ok) throw new Error();
      data = await res.json();
      message = 'Guardado correctamente';
      messageType = 'success';
    } catch {
      message = 'Error al guardar los cambios';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }
</script>

{#if loading}
  <div class="flex items-center gap-2 text-zinc-400">
    <span
      class="animate-spin inline-block w-4 h-4 border-2
                 border-zinc-600 border-t-amber-400 rounded-full"
    ></span>
    <span class="text-sm">Cargando...</span>
  </div>
{:else}
  <form on:submit|preventDefault={handleSubmit} class="space-y-6">
    <!-- Imagen -->
    <ImageUpload
      currentImage={data?.image_url}
      label="Imagen principal"
      accept="image/*"
      maxSizeMB={5}
      on:change={handleImageChange}
    />

    <!-- Campos del formulario -->
    <div>
      <label class="block text-sm font-medium text-zinc-300 mb-2"> Título </label>
      <input
        type="text"
        bind:value={title}
        required
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="Título principal"
      />
    </div>

    <div>
      <label class="block text-sm font-medium text-zinc-300 mb-2"> Subtítulo </label>
      <textarea
        bind:value={subtitle}
        rows={3}
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500 resize-none
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="Subtítulo o descripción"
      ></textarea>
    </div>

    <div>
      <label class="block text-sm font-medium text-zinc-300 mb-2"> Descripción </label>
      <textarea
        bind:value={description}
        rows={4}
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500 resize-none
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="Descripción completa"
      ></textarea>
    </div>

    <div>
      <label class="block text-sm font-medium text-zinc-300 mb-2"> Imagen de fondo (URL) </label>
      <input
        type="text"
        bind:value={background_image}
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="URL de la imagen de fondo"
      />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-zinc-300 mb-2"> Texto botón contacto </label>
        <input
          type="text"
          bind:value={contact_button_text}
          required
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Contactar"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-zinc-300 mb-2"> Texto botón CV </label>
        <input
          type="text"
          bind:value={cv_button_text}
          required
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Descargar CV"
        />
      </div>
    </div>

    <!-- Botón guardar + mensaje -->
    <div class="flex items-center gap-4">
      <button
        type="submit"
        disabled={saving}
        class="px-6 py-2.5 rounded-lg font-medium text-sm
               bg-gradient-to-r from-amber-400 to-orange-500
               text-zinc-900 hover:from-amber-300 hover:to-orange-400
               disabled:opacity-50 disabled:cursor-not-allowed
               transition-all duration-200"
      >
        {saving ? 'Guardando...' : 'Guardar cambios'}
      </button>

      {#if message}
        <span class="text-sm {messageType === 'success' ? 'text-emerald-400' : 'text-red-400'}">
          {message}
        </span>
      {/if}
    </div>
  </form>
{/if}
