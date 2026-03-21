<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { ProjectResponse } from '$lib/types';
  import ImageUpload from '../ui/ImageUpload.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  let items: ProjectResponse[] = [];
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';
  let editingId: number | null = null;

  // Formulario
  let title = '';
  let description = '';
  let tags = '';
  let icon_name = '';
  let color = '';
  let demo_url = '';
  let github_url = '';
  let imageFile: File | null = null;

  const iconOptions = ['Layers', 'Lock', 'Calendar', 'ExternalLink', 'Github'];

  onMount(async () => {
    await loadItems();
  });

  async function loadItems() {
    try {
      items = await fetchApi<ProjectResponse[]>('/api/v1/projects/');
    } catch {
      items = [];
    } finally {
      loading = false;
    }
  }

  function resetForm() {
    title = '';
    description = '';
    tags = '';
    icon_name = '';
    color = '';
    demo_url = '';
    github_url = '';
    imageFile = null;
    editingId = null;
  }

  function editItem(item: ProjectResponse) {
    title = item.title;
    description = item.description;
    tags = item.tags.join(', ');
    icon_name = item.icon_name;
    color = item.color;
    demo_url = item.demo_url || '';
    github_url = item.github_url || '';
    editingId = item.id;
  }

  function handleImageChange(e: CustomEvent<{ file: File | null; preview: string | null }>) {
    imageFile = e.detail.file;
  }

  async function handleSubmit() {
    saving = true;
    message = '';

    try {
      // SIEMPRE FormData para proyectos (tienen imagen)
      const formData = new FormData();
      formData.append('title', title);
      formData.append('description', description);
      formData.append(
        'tags',
        JSON.stringify(
          tags
            .split(',')
            .map((t) => t.trim())
            .filter((t) => t),
        ),
      );
      formData.append('icon_name', icon_name);
      formData.append('color', color);
      formData.append('demo_url', demo_url);
      formData.append('github_url', github_url);
      if (imageFile) formData.append('image', imageFile);

      const url = editingId ? `${API}/api/v1/projects/${editingId}` : `${API}/api/v1/projects/`;

      const method = editingId ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        body: formData,
      });

      if (!res.ok) throw new Error();

      message = editingId ? 'Actualizado correctamente' : 'Creado correctamente';
      messageType = 'success';
      resetForm();
      await loadItems();
    } catch {
      message = 'Error al guardar';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }

  async function deleteItem(id: number) {
    if (!confirm('¿Estás seguro de eliminar este proyecto?')) return;

    try {
      const res = await fetch(`${API}/api/v1/projects/${id}`, {
        method: 'DELETE',
      });

      if (!res.ok) throw new Error();

      message = 'Eliminado correctamente';
      messageType = 'success';
      await loadItems();
    } catch {
      message = 'Error al eliminar';
      messageType = 'error';
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
  <div class="space-y-8">
    <!-- Formulario -->
    <div class="bg-zinc-900 rounded-xl p-6 border border-zinc-800">
      <h2 class="text-lg font-semibold text-zinc-100 mb-4">
        {editingId ? 'Editar Proyecto' : 'Nuevo Proyecto'}
      </h2>

      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <div>
          <label 
            for="title"
            class="block text-sm font-medium text-zinc-300 mb-2"> Título </label>
          <input
            id="title"
            type="text"
            bind:value={title}
            required
            class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors"
            placeholder="Tapicería Moderna"
          />
        </div>

        <div>
          <label 
            for="description"
            class="block text-sm font-medium text-zinc-300 mb-2"> Descripción </label>
          <textarea
            id="description"
            bind:value={description}
            rows={3}
            required
            class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500 resize-none
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors"
            placeholder="Plataforma de gestión para taller de tapicería..."
          ></textarea>
        </div>

        <div>
          <label 
            for="tags"
            class="block text-sm font-medium text-zinc-300 mb-2">
            Tags (separados por coma)
          </label>
          <input
            id="tags"
            type="text"
            bind:value={tags}
            required
            class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors"
            placeholder="Vite, Neon, Django, Tailwind"
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label 
              for="icon_name"
              class="block text-sm font-medium text-zinc-300 mb-2"> Icono </label>
            <select
              id="icon_name"
              bind:value={icon_name}
              required
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
            >
              <option value="">Seleccionar</option>
              {#each iconOptions as iconName}
                <option value={iconName}>{iconName}</option>
              {/each}
            </select>
          </div>

          <div>
            <label 
              for="color"
              class="block text-sm font-medium text-zinc-300 mb-2"> Color gradiente </label>
            <input
              id="color"
              type="text"
              bind:value={color}
              required
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="from-amber-500/20 to-orange-600/20"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label 
              for="demo_url"
              class="block text-sm font-medium text-zinc-300 mb-2">
              URL Demo (opcional)
            </label>
            <input
              id="demo_url"
              type="url"
              bind:value={demo_url}
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="https://demo.ejemplo.com"
            />
          </div>

          <div>
            <label 
              for="github_url"
              class="block text-sm font-medium text-zinc-300 mb-2">
              URL GitHub (opcional)
            </label>
            <input
              id="github_url"
              type="url"
              bind:value={github_url}
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="https://github.com/usuario/repo"
            />
          </div>
        </div>

        <!-- Imagen -->
        <ImageUpload
          currentImage={editingId ? items.find((i) => i.id === editingId)?.image_url : null}
          label="Imagen del proyecto"
          accept="image/*"
          maxSizeMB={5}
          on:change={handleImageChange}
        />

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
            {saving ? 'Guardando...' : editingId ? 'Actualizar' : 'Agregar'}
          </button>

          {#if editingId}
            <button
              type="button"
              on:click={resetForm}
              class="px-6 py-2.5 rounded-lg font-medium text-sm
                     bg-zinc-700 text-zinc-300 hover:bg-zinc-600
                     transition-all duration-200"
            >
              Cancelar
            </button>
          {/if}

          {#if message}
            <span class="text-sm {messageType === 'success' ? 'text-emerald-400' : 'text-red-400'}">
              {message}
            </span>
          {/if}
        </div>
      </form>
    </div>

    <!-- Lista de items -->
    <div>
      <h2 class="text-lg font-semibold text-zinc-100 mb-4">
        Proyectos ({items.length})
      </h2>

      {#if items.length === 0}
        <p class="text-zinc-500 text-center py-8">No hay proyectos registrados</p>
      {:else}
        <div class="space-y-2">
          {#each items as item}
            <div
              class="bg-zinc-900 rounded-lg p-4 border border-zinc-800 flex items-center justify-between"
            >
              <div class="flex-1">
                <div class="flex items-center gap-3">
                  <span class="text-amber-400 font-medium">{item.title}</span>
                  <div class="flex gap-1">
                    {#each item.tags as tag}
                      <span class="text-xs px-2 py-1 bg-zinc-800 rounded-full text-zinc-400">
                        {tag}
                      </span>
                    {/each}
                  </div>
                </div>
                <p class="text-sm text-zinc-500 mt-1 line-clamp-1">{item.description}</p>
              </div>

              <div class="flex items-center gap-2">
                <button
                  on:click={() => editItem(item)}
                  class="px-3 py-1.5 text-sm bg-zinc-700 text-zinc-300 rounded-lg
                         hover:bg-zinc-600 transition-colors"
                >
                  Editar
                </button>
                <button
                  on:click={() => deleteItem(item.id)}
                  class="px-3 py-1.5 text-sm bg-red-900/20 text-red-400 rounded-lg
                         hover:bg-red-900/30 transition-colors"
                >
                  Eliminar
                </button>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
{/if}
