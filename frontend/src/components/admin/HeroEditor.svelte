<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { HeroResponse } from '$lib/types';
  import ImageUpload from '../ui/ImageUpload.svelte';
  import { dispatchDataChange } from '$lib/dataEvents';
  import { FileText, CheckCircle, Save, Loader2 } from 'lucide-svelte';

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
  let background_image = '';
  let contact_button_text = '';
  let cv_button_text = '';

  // Referencias a archivos
  let imageFile: File | null = null;
  let cvFile: File | null = null;

  onMount(async () => {
    try {
      const res = await fetchApi<HeroResponse>('/api/v1/heroes/latest/');
      if (res) {
        data = res;
        title = res.title ?? '';
        subtitle = res.subtitle ?? '';
        description = res.description ?? '';
        background_image = res.background_image ?? '';
        contact_button_text = res.contact_button_text ?? '';
        cv_button_text = res.cv_button_text ?? '';
      }
    } catch (err) {
      message = 'Error al conectar con la API';
      messageType = 'error';
    } finally {
      loading = false;
    }
  });

  function handleImageChange(e: CustomEvent<{ file: File | null; preview: string | null }>) {
    imageFile = e.detail.file;
  }

  function handleCVChange(e: Event) {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      cvFile = target.files[0];
    }
  }

  async function handleSubmit() {
    if (!data) return;
    saving = true;
    message = '';

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('subtitle', subtitle);
      formData.append('description', description);
      formData.append('background_image', background_image);
      formData.append('contact_button_text', contact_button_text);
      formData.append('cv_button_text', cv_button_text);

      if (imageFile) formData.append('image', imageFile);
      if (cvFile) formData.append('cv_file', cvFile);

      const res = await fetch(`${API}/api/v1/heroes/${data.id}`, {
        method: 'PUT',
        body: formData,
      });

      if (!res.ok) throw new Error('Error en la respuesta del servidor');

      const updatedData = await res.json();
      data = updatedData;
      message = '¡Hero y CV actualizados con éxito!';
      messageType = 'success';

      dispatchDataChange('hero', 'update', updatedData);
      cvFile = null;
    } catch (err) {
      message = 'No se pudo guardar la información';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }

  // --- PARCHE DINÁMICO: COMPATIBILIDAD CON BACKEND ---
  const getDownloadUrl = (url: string | null | undefined) => {
    if (!url) return '#';
    // Si la URL ya trae el parche fl_attachment del backend, la dejamos pasar.
    // Si no, lo agregamos preventivamente.
    if (url.includes('cloudinary.com') && !url.includes('fl_attachment')) {
      return url.replace('/upload/', '/upload/fl_attachment/');
    }
    return url;
  };
</script>

{#if loading}
  <div class="flex items-center justify-center p-12 text-zinc-400 gap-3">
    <Loader2 class="animate-spin w-5 h-5 text-amber-500" />
    <span class="text-sm font-medium">Cargando configuración del Hero...</span>
  </div>
{:else}
  <form on:submit|preventDefault={handleSubmit} class="space-y-8 animate-in fade-in duration-500">
    <div class="space-y-4">
      <h3 class="text-xs font-bold uppercase tracking-widest text-zinc-500">Visuales</h3>
      <ImageUpload
        currentImage={data?.image_url}
        label="Foto de Perfil / Hero Image"
        accept="image/*"
        maxSizeMB={5}
        on:change={handleImageChange}
      />
    </div>

    <div class="p-5 rounded-xl bg-zinc-900/50 border border-zinc-800 space-y-4">
      <div class="flex items-center justify-between">
        <label for="cv_upload" class="flex items-center gap-2 text-sm font-semibold text-zinc-200">
          <FileText class="w-4 h-4 text-amber-400" />
          Archivo de Currículum (PDF)
        </label>
        {#if data?.cv_url}
          <a
            href={getDownloadUrl(data.cv_url)}
            target="_blank"
            class="text-[10px] text-amber-500 hover:underline"
          >
            Ver actual ↗
          </a>
        {/if}
      </div>

      <div class="flex flex-col gap-3">
        <input
          id="cv_upload"
          type="file"
          accept=".pdf"
          on:change={handleCVChange}
          class="block w-full text-xs text-zinc-400
                 file:mr-4 file:py-2 file:px-4
                 file:rounded-lg file:border-0
                 file:text-xs file:font-bold
                 file:bg-zinc-800 file:text-zinc-200
                 hover:file:bg-zinc-700 transition-all cursor-pointer"
        />

        {#if data?.cv_url}
          <div class="flex items-center gap-1.5 text-[11px] text-emerald-400 font-medium">
            <CheckCircle class="w-3.5 h-3.5" />
            Hay un archivo vinculado en Cloudinary
          </div>
        {/if}
      </div>
    </div>

    <div class="space-y-6">
      <h3 class="text-xs font-bold uppercase tracking-widest text-zinc-500">Contenido</h3>

      <div class="grid grid-cols-1 gap-6">
        <div>
          <label for="title" class="block text-sm font-medium text-zinc-400 mb-2"
            >Título Principal</label
          >
          <input
            id="title"
            type="text"
            bind:value={title}
            required
            class="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none"
            placeholder="Ej: Desarrollador Full Stack"
          />
        </div>

        <div>
          <label for="subtitle" class="block text-sm font-medium text-zinc-400 mb-2"
            >Subtítulo (Nombre)</label
          >
          <input
            id="subtitle"
            type="text"
            bind:value={subtitle}
            class="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none"
            placeholder="Ej: Hernan Arango Cortes"
          />
        </div>

        <div>
          <label for="description" class="block text-sm font-medium text-zinc-400 mb-2"
            >Descripción Biográfica</label
          >
          <textarea
            id="description"
            bind:value={description}
            rows={4}
            class="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none resize-none"
            placeholder="Cuéntale al mundo quién eres..."
          ></textarea>
        </div>
      </div>
    </div>

    <div
      class="grid grid-cols-1 md:grid-cols-2 gap-6 p-5 rounded-xl bg-zinc-900/30 border border-zinc-800/50"
    >
      <div>
        <label
          for="contact_btn"
          class="block text-xs font-bold text-zinc-500 mb-2 uppercase tracking-wider"
          >Botón Contacto</label
        >
        <input
          id="contact_btn"
          type="text"
          bind:value={contact_button_text}
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-500 outline-none"
        />
      </div>

      <div>
        <label
          for="cv_btn"
          class="block text-xs font-bold text-zinc-500 mb-2 uppercase tracking-wider"
          >Botón Descarga CV</label
        >
        <input
          id="cv_btn"
          type="text"
          bind:value={cv_button_text}
          class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-500 outline-none"
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
          <Loader2 class="animate-spin w-5 h-5" />
          Subiendo Archivos...
        {:else}
          <Save class="w-5 h-5" />
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
