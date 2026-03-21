<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { PassionResponse } from '$lib/types';
  import ImageUpload from '../ui/ImageUpload.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  let data: PassionResponse | null = null;
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // un campo por cada campo del schema Create
  let title = '';
  let description = '';
  let family_title = '';
  let family_desc = '';
  let games_title = '';
  let games_desc = '';
  let coding_title = '';
  let coding_desc = '';
  let imageFile: File | null = null;

  onMount(async () => {
    try {
      data = await fetchApi<PassionResponse>('/api/v1/passions/latest/');
      title = data.title ?? '';
      description = data.description ?? '';
      family_title = data.family_title ?? '';
      family_desc = data.family_desc ?? '';
      games_title = data.games_title ?? '';
      games_desc = data.games_desc ?? '';
      coding_title = data.coding_title ?? '';
      coding_desc = data.coding_desc ?? '';
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
      formData.append('description', description);
      formData.append('family_title', family_title);
      formData.append('family_desc', family_desc);
      formData.append('games_title', games_title);
      formData.append('games_desc', games_desc);
      formData.append('coding_title', coding_title);
      formData.append('coding_desc', coding_desc);
      if (imageFile) formData.append('image', imageFile);

      const res = await fetch(`${API}/api/v1/passions/${data.id}`, {
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


<div class="p-6 md:p-10">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-zinc-100 mb-2">Editar Pasiones</h1>      
    </div>
      
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
      label="Imagen de pasiones"
      accept="image/*"
      maxSizeMB={5}
      on:change={handleImageChange}
    />

    <!-- Campos principales -->
    <div>
      <label 
        for="title"
        class="block text-sm font-medium text-zinc-300 mb-2"> Título principal </label>
      <input
        id="title"
        type="text"
        bind:value={title}
        required
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="Más allá del Código"
      />
    </div>

    <div>
      <label 
        for="description"
        class="block text-sm font-medium text-zinc-300 mb-2"> Descripción principal </label>
      <textarea
        id="description"
        bind:value={description}
        rows={3}
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500 resize-none
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="Mi pasión, aparte de programar y jugar videojuegos, es estar con mi familia."
      ></textarea>
    </div>

    <!-- Sección Familia -->
    <div class="bg-zinc-900/50 rounded-lg p-4 border border-zinc-800">
      <h3 class="text-amber-400 font-medium mb-3">Sección Familia</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label 
            for="family_title"
            class="block text-sm font-medium text-zinc-300 mb-2"> Título familia </label>
          <input
            id="family_title"
            type="text"
            bind:value={family_title}
            required
            class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors"
            placeholder="Mi Familia"
          />
        </div>        
      </div>

      <div class="mt-4">
        <label 
          for="family_desc"
          class="block text-sm font-medium text-zinc-300 mb-2"> Descripción familia </label>
        <textarea
          id="family_desc"
          bind:value={family_desc}
          rows={3}
          class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500 resize-none
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Son mi motor, mi pasión y la razón de querer continuar cada día y cada momento."
        ></textarea>
      </div>
    </div>

    <!-- Sección Videojuegos -->
    <div class="bg-zinc-900/50 rounded-lg p-4 border border-zinc-800">
      <h3 class="text-amber-400 font-medium mb-3">Sección Videojuegos</h3>

      <div>
          <label 
            for="games_title"
            class="block text-sm font-medium text-zinc-300 mb-2"> Título videojuegos </label>
          <input
            id="games_title"
            type="text"
            bind:value={games_title}
            required
            class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors"
            placeholder="Videojuegos"
          />
        </div>

      <div class="mt-4">
        <label 
          for="games_desc"
          class="block text-sm font-medium text-zinc-300 mb-2">
          Descripción videojuegos
        </label>
        <textarea
          id="games_desc"
          bind:value={games_desc}
          rows={3}
          class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500 resize-none
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Un hobby que me permite desconectar y explorar nuevos mundos digitales."
        ></textarea>
      </div>
    </div>

    <!-- Sección Programación -->
    <div class="bg-zinc-900/50 rounded-lg p-4 border border-zinc-800">
      <h3 class="text-amber-400 font-medium mb-3">Sección Programación</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label 
            for="coding_title"
            class="block text-sm font-medium text-zinc-300 mb-2"> Título programación </label>
          <input
            id="coding_title"
            type="text"
            bind:value={coding_title}
            required
            class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors"
            placeholder="Programación"
          />
        </div>
      </div>

      <div class="mt-4">
        <label 
          for="coding_desc"
          class="block text-sm font-medium text-zinc-300 mb-2">
          Descripción programación
        </label>
        <textarea
          id="coding_desc"
          bind:value={coding_desc}
          rows={3}
          class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500 resize-none
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="No es solo mi trabajo, es mi forma de crear y aportar valor al mundo."
        ></textarea>
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

  </div>
</div>
