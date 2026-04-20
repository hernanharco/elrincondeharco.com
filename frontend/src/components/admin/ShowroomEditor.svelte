<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import ImageUpload from '../ui/ImageUpload.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  interface ShowroomResponse {
    id: number;
    title: string;
    description: string;
    category: string;
    deploy_url: string | null;
    image_url: string | null;
  }

  let items: ShowroomResponse[] = [];
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';
  let editingId: number | null = null;

  // Formulario
  let title = '';
  let description = '';
  let category = '';
  let deploy_url = '';
  let imageFile: File | null = null;
  let currentImage: string | null = null;

  const categoryOptions = ['Web App', 'SaaS', 'Portfolio', 'Mobile', 'Desktop', 'API'];

  onMount(async () => {
    await loadItems();
  });

  async function loadItems() {
    try {
      items = await fetchApi<ShowroomResponse[]>('/api/v1/showrooms/');
    } catch {
      items = [];
    } finally {
      loading = false;
    }
  }

  function resetForm() {
    title = '';
    description = '';
    category = '';
    deploy_url = '';
    imageFile = null;
    currentImage = null;
    editingId = null;
    message = '';
  }

  function editItem(item: ShowroomResponse) {
    title = item.title;
    description = item.description;
    category = item.category;
    deploy_url = item.deploy_url || '';
    currentImage = item.image_url;
    editingId = item.id;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function handleImageChange(e: CustomEvent<{ file: File | null; preview: string | null }>) {
    imageFile = e.detail.file;
    currentImage = e.detail.preview;
  }

  async function handleSubmit() {
    saving = true;
    message = '';

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('description', description);
      formData.append('category', category);
      formData.append('deploy_url', deploy_url);
      if (imageFile) formData.append('image', imageFile);

      const url = editingId ? `${API}/api/v1/showrooms/${editingId}` : `${API}/api/v1/showrooms/`;
      const method = editingId ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        body: formData,
      });

      if (!res.ok) throw new Error();

      message = editingId ? '✨ ¡Actualizado con éxito!' : '🚀 ¡Proyecto creado con éxito!';
      messageType = 'success';
      resetForm();
      await loadItems();
    } catch {
      message = '❌ Error al procesar la solicitud';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }

  async function deleteItem(id: number) {
    if (!confirm('¿Estás seguro de eliminar este elemento?')) return;

    try {
      const res = await fetch(`${API}/api/v1/showrooms/${id}`, {
        method: 'DELETE',
      });

      if (!res.ok) throw new Error();

      message = '🗑️ Eliminado correctamente';
      messageType = 'success';
      await loadItems();
    } catch {
      message = '❌ Error al eliminar';
      messageType = 'error';
    }
  }
</script>

<div class="p-6 md:p-10">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-zinc-100 mb-2">Editor de Showroom</h1>
      <p class="text-zinc-400">Publica tus diseños de Figma ya desplegados en Vercel</p>
    </div>

    {#if loading}
      <div class="flex items-center gap-2 text-zinc-400">
        <span class="animate-spin inline-block w-4 h-4 border-2 border-zinc-600 border-t-amber-400 rounded-full"></span>
        <span class="text-sm">Cargando base de datos...</span>
      </div>
    {:else}
      <div class="space-y-8">
        <div class="bg-zinc-900 rounded-xl p-6 border border-zinc-800 shadow-xl">
          <h2 class="text-lg font-semibold text-zinc-100 mb-4">
            {editingId ? '📝 Editar Proyecto' : '🆕 Nuevo Proyecto'}
          </h2>

          <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <div>
              <label for="title" class="block text-sm font-medium text-zinc-300 mb-2">Nombre del Proyecto</label>
              <input
                id="title"
                type="text"
                bind:value={title}
                required
                class="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none"
                placeholder="Ej: Dashboard Logística"
              />
            </div>

            <div>
              <label for="description" class="block text-sm font-medium text-zinc-300 mb-2">Descripción corta</label>
              <textarea
                id="description"
                bind:value={description}
                rows="3"
                required
                class="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 transition-all outline-none resize-none"
                placeholder="Explica brevemente qué resuelve este diseño..."
              ></textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="category" class="block text-sm font-medium text-zinc-300 mb-2">Categoría</label>
                <select
                  id="category"
                  bind:value={category}
                  required
                  class="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 outline-none"
                >
                  <option value="">Seleccionar...</option>
                  {#each categoryOptions as cat}
                    <option value={cat}>{cat}</option>
                  {/each}
                </select>
              </div>

              <div>
                <label for="deploy_url" class="block text-sm font-medium text-zinc-300 mb-2">URL de Vercel</label>
                <input
                  id="deploy_url"
                  type="url"
                  bind:value={deploy_url}
                  required
                  class="w-full px-4 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 focus:border-amber-400 outline-none"
                  placeholder="https://proyecto.vercel.app"
                />
              </div>
            </div>

            <div class="py-2">
              <ImageUpload 
                currentImage={currentImage} 
                label="Miniatura del Prototipo"
                on:change={handleImageChange}
              />
            </div>

            <div class="flex gap-3 pt-4 border-t border-zinc-800">
              <button
                type="submit"
                disabled={saving}
                class="px-6 py-2 bg-amber-500 hover:bg-amber-600 text-black font-bold rounded-lg disabled:opacity-50 transition-all"
              >
                {saving ? 'Guardando...' : (editingId ? 'Actualizar Proyecto' : 'Publicar en Showroom')}
              </button>
              
              {#if editingId}
                <button
                  type="button"
                  on:click={resetForm}
                  class="px-6 py-2 bg-zinc-700 text-white rounded-lg hover:bg-zinc-600 transition-all"
                >
                  Cancelar
                </button>
              {/if}
            </div>
          </form>

          {#if message}
            <div class={`mt-4 p-4 rounded-lg text-sm font-medium ${
              messageType === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'
            }`}>
              {message}
            </div>
          {/if}
        </div>

        <div class="bg-zinc-900 rounded-xl p-6 border border-zinc-800 shadow-xl">
          <h2 class="text-lg font-semibold text-zinc-100 mb-6">Prototipos en Vivo</h2>
          
          {#if items.length === 0}
            <div class="text-center py-10 border-2 border-dashed border-zinc-800 rounded-xl">
              <p class="text-zinc-500">Aún no has subido ningún prototipo al showroom.</p>
            </div>
          {:else}
            <div class="grid gap-4">
              {#each items as item}
                <div class="flex items-center justify-between p-4 bg-zinc-800/50 rounded-xl border border-zinc-700 hover:border-zinc-600 transition-all">
                  <div class="flex gap-4 items-center">
                    {#if item.image_url}
                      <img src={item.image_url} alt="" class="w-16 h-10 object-cover rounded border border-zinc-700" />
                    {/if}
                    <div>
                      <h3 class="font-bold text-zinc-100">{item.title}</h3>
                      <p class="text-xs text-zinc-500 uppercase tracking-tighter">{item.category}</p>
                    </div>
                  </div>
                  
                  <div class="flex gap-2">
                    <button
                      on:click={() => editItem(item)}
                      class="p-2 text-amber-400 hover:bg-amber-400/10 rounded-lg transition-colors"
                      title="Editar"
                    >
                      Editar
                    </button>
                    <button
                      on:click={() => deleteItem(item.id)}
                      class="p-2 text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
                      title="Eliminar"
                    >
                      Borrar
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>
</div>