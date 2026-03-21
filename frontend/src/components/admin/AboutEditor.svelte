<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { AboutResponse } from '$lib/types';
  import ImageUpload from '../ui/ImageUpload.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  let data: AboutResponse | null = null;
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // un campo por cada campo del schema Create
  let title = '';
  let description = '';
  let location = '';
  let years_experience = '';
  let team_name = '';
  let leadership_title = '';
  let leadership_desc = '';
  let experience_title = '';
  let experience_desc = '';
  let imageFile: File | null = null;

  onMount(async () => {
    try {
      data = await fetchApi<AboutResponse>('/api/v1/abouts/latest/');
      title = data.title ?? '';
      description = data.description ?? '';
      location = data.location ?? '';
      years_experience = data.years_experience ?? '';
      team_name = data.team_name ?? '';
      leadership_title = data.leadership_title ?? '';
      leadership_desc = data.leadership_desc ?? '';
      experience_title = data.experience_title ?? '';
      experience_desc = data.experience_desc ?? '';
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
      formData.append('location', location);
      formData.append('years_experience', years_experience);
      formData.append('team_name', team_name);
      formData.append('leadership_title', leadership_title);
      formData.append('leadership_desc', leadership_desc);
      formData.append('experience_title', experience_title);
      formData.append('experience_desc', experience_desc);
      if (imageFile) formData.append('image', imageFile);

      const res = await fetch(`${API}/api/v1/abouts/${data.id}`, {
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
      label="Foto personal"
      accept="image/*"
      maxSizeMB={5}
      on:change={handleImageChange}
    />

    <!-- Campos del formulario -->
    <div>
      <label for="title" class="block text-sm font-medium text-zinc-300 mb-2"> Título </label>
      <input
        id="title"
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
      <label for="description" class="block text-sm font-medium text-zinc-300 mb-2">
        Descripción
      </label>
      <textarea
        id="description"
        bind:value={description}
        rows={4}
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500 resize-none
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="Descripción completa"
      ></textarea>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label for="location" class="block text-sm font-medium text-zinc-300 mb-2">
          Ubicación
        </label>
        <input
          id="location"
          type="text"
          bind:value={location}
          required
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Avilés, Asturias, España"
        />
      </div>

      <div>
        <label for="years_experience" class="block text-sm font-medium text-zinc-300 mb-2">
          Años de experiencia
        </label>
        <input
          id="years_experience"
          type="text"
          bind:value={years_experience}
          required
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="14+ Años"
        />
      </div>
    </div>

    <div>
      <label for="team_name" class="block text-sm font-medium text-zinc-300 mb-2">
        Nombre del equipo
      </label>
      <input
        id="team_name"
        type="text"
        bind:value={team_name}
        required
        class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
               text-zinc-100 placeholder-zinc-500
               focus:outline-none focus:border-amber-400 focus:ring-1
               focus:ring-amber-400 transition-colors"
        placeholder="Equipo de Oro"
      />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label for="leadership_title" class="block text-sm font-medium text-zinc-300 mb-2">
          Título liderazgo
        </label>
        <input
          id="leadership_title"
          type="text"
          bind:value={leadership_title}
          required
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Liderazgo"
        />
      </div>

      <div>
        <label for="experience_title" class="block text-sm font-medium text-zinc-300 mb-2">
          Título experiencia
        </label>
        <input
          id="experience_title"
          type="text"
          bind:value={experience_title}
          required
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Experiencia"
        />
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label for="leadership_desc" class="block text-sm font-medium text-zinc-300 mb-2">
          Descripción liderazgo
        </label>
        <textarea
          id="leadership_desc"
          bind:value={leadership_desc}
          rows={3}
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500 resize-none
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Formación de equipos de alto rendimiento."
        ></textarea>
      </div>

      <div>
        <label for="experience_desc" class="block text-sm font-medium text-zinc-300 mb-2">
          Descripción experiencia
        </label>
        <textarea
          id="experience_desc"
          bind:value={experience_desc}
          rows={3}
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                 text-zinc-100 placeholder-zinc-500 resize-none
                 focus:outline-none focus:border-amber-400 focus:ring-1
                 focus:ring-amber-400 transition-colors"
          placeholder="Más de una década entregando soluciones."
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
