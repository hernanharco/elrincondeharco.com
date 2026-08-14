<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { ProjectResponse, SectorResponse } from '$lib/types';
  import ImageUpload from '../ui/ImageUpload.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  let items: ProjectResponse[] = [];
  let sectors: SectorResponse[] = [];
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
  // Multi-image
  let existingImageUrls: string[] = [];
  let newImageFiles: File[] = [];
  let imagePreviews: string[] = [];
  let selectedSectorIds: number[] = [];

  const iconOptions = ['Layers', 'Lock', 'Calendar', 'ExternalLink', 'Github', 'Coffee', 'ShoppingBag', 'Building2', 'Bot'];

  onMount(async () => {
    await Promise.all([loadItems(), loadSectors()]);
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

  async function loadSectors() {
    try {
      sectors = await fetchApi<SectorResponse[]>('/api/v1/sectors/');
    } catch {
      sectors = [];
    }
  }

  // ── Qué sectores contiene este proyecto ─────────────────────
  function getProjectSectors(projectId: number): SectorResponse[] {
    return sectors.filter((s) => (s.project_ids || []).includes(projectId));
  }

  function resetForm() {
    title = '';
    description = '';
    tags = '';
    icon_name = '';
    color = '';
    demo_url = '';
    github_url = '';
    editingId = null;
    selectedSectorIds = [];
    existingImageUrls = [];
    newImageFiles = [];
    imagePreviews = [];
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
    existingImageUrls = [...(item.image_urls || [])];
    newImageFiles = [];
    imagePreviews = [];
    selectedSectorIds = getProjectSectors(item.id).map((s) => s.id);
  }

  // ── Multi-image: agregar archivos ──────────────────────────
  function handleImagesSelected(e: Event) {
    const files = (e.target as HTMLInputElement).files;
    if (!files) return;
    for (const file of Array.from(files)) {
      newImageFiles = [...newImageFiles, file];
      imagePreviews = [...imagePreviews, URL.createObjectURL(file)];
    }
    // Resetear el input para poder seleccionar los mismos archivos de nuevo
    (e.target as HTMLInputElement).value = '';
  }

  // ── Multi-image: arrastrar archivos desde el escritorio ────
  // Sin preventDefault el navegador intenta navegar a file:/// y Chrome
  // lo bloquea ("no puede cargar o enlazar con file:///"). Con el handler
  // agregamos las imágenes como si se hubieran seleccionado con el picker.
  function handleDrop(e: DragEvent) {
    e.preventDefault();
    const files = e.dataTransfer?.files;
    if (!files) return;
    for (const file of Array.from(files)) {
      if (!file.type.startsWith('image/')) continue;
      newImageFiles = [...newImageFiles, file];
      imagePreviews = [...imagePreviews, URL.createObjectURL(file)];
    }
  }

  function removeNewImage(index: number) {
    URL.revokeObjectURL(imagePreviews[index]);
    newImageFiles = newImageFiles.filter((_, i) => i !== index);
    imagePreviews = imagePreviews.filter((_, i) => i !== index);
  }

  function removeExistingImage(index: number) {
    existingImageUrls = existingImageUrls.filter((_, i) => i !== index);
  }

  function toggleSector(sectorId: number) {
    if (selectedSectorIds.includes(sectorId)) {
      selectedSectorIds = selectedSectorIds.filter((id) => id !== sectorId);
    } else {
      selectedSectorIds = [...selectedSectorIds, sectorId];
    }
  }

  // ── Actualizar project_ids de un sector ────────────────────
  async function updateSectorProjects(sectorId: number, projectIds: number[]) {
    await fetch(`${API}/api/v1/sectors/${sectorId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_ids: projectIds }),
    });
  }

  // ── Sincronizar sectores después de guardar proyecto ───────
  async function syncSectors(projectId: number) {
    // Para cada sector, agregar o sacar este projectId
    for (const sector of sectors) {
      const currentIds: number[] = sector.project_ids || [];
      const shouldHave = selectedSectorIds.includes(sector.id);

      if (shouldHave && !currentIds.includes(projectId)) {
        // Agregar projectId al sector
        await updateSectorProjects(sector.id, [...currentIds, projectId]);
      } else if (!shouldHave && currentIds.includes(projectId)) {
        // Sacar projectId del sector
        await updateSectorProjects(sector.id, currentIds.filter((id) => id !== projectId));
      }
    }
    await loadSectors(); // Recargar sectores para mostrar cambios
  }

  async function handleSubmit() {
    saving = true;
    message = '';

    try {
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
      // Enviar URLs existentes como JSON + nuevas imágenes como múltiples archivos
      formData.append('image_urls', JSON.stringify(existingImageUrls));
      for (const file of newImageFiles) {
        formData.append('images', file);
      }

      const url = editingId ? `${API}/api/v1/projects/${editingId}` : `${API}/api/v1/projects/`;
      const method = editingId ? 'PUT' : 'POST';

      const res = await fetch(url, { method, body: formData });
      if (!res.ok) throw new Error();

      const savedProject = await res.json();
      const projectId = savedProject.id || editingId;

      // Sincronizar sectores con el proyecto guardado
      await syncSectors(projectId);

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
      // Primero sacar el proyecto de todos los sectores
      for (const sector of sectors) {
        const currentIds: number[] = sector.project_ids || [];
        if (currentIds.includes(id)) {
          await updateSectorProjects(sector.id, currentIds.filter((pid) => pid !== id));
        }
      }

      const res = await fetch(`${API}/api/v1/projects/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error();

      message = 'Eliminado correctamente';
      messageType = 'success';
      await Promise.all([loadItems(), loadSectors()]);
    } catch {
      message = 'Error al eliminar';
      messageType = 'error';
    }
  }
</script>

<div class="p-6 md:p-10">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-zinc-100 mb-2">Editar Proyectos</h1>
      <p class="text-sm text-zinc-500">Los proyectos se asignan a rubros desde acá o desde la sección <a href="/admin/sectors" class="text-amber-400 hover:underline">Sectores</a></p>
    </div>

{#if loading}
  <div class="flex items-center gap-2 text-zinc-400">
    <span class="animate-spin inline-block w-4 h-4 border-2 border-zinc-600 border-t-amber-400 rounded-full"></span>
    <span class="text-sm">Cargando...</span>
  </div>
{:else}
  <div class="space-y-8">
    <!-- ═══ FORMULARIO ═══ -->
    <div class="bg-zinc-900 rounded-xl p-6 border border-zinc-800">
      <h2 class="text-lg font-semibold text-zinc-100 mb-4">
        {editingId ? 'Editar Proyecto' : 'Nuevo Proyecto'}
      </h2>

      {#if message}
        <div
          class="mb-4 p-3 rounded-lg text-sm font-medium flex items-center gap-2
            {messageType === 'success'
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
              : 'bg-red-500/10 text-red-400 border border-red-500/20'}"
        >
          {message}
        </div>
      {/if}

      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <div>
          <label for="title" class="block text-sm font-medium text-zinc-300 mb-2">Título</label>
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
          <label for="description" class="block text-sm font-medium text-zinc-300 mb-2">Descripción</label>
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
          <label for="tags" class="block text-sm font-medium text-zinc-300 mb-2">
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
            <label for="icon_name" class="block text-sm font-medium text-zinc-300 mb-2">Icono</label>
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
            <label for="color" class="block text-sm font-medium text-zinc-300 mb-2">Color gradiente</label>
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
            <label for="demo_url" class="block text-sm font-medium text-zinc-300 mb-2">
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
            <label for="github_url" class="block text-sm font-medium text-zinc-300 mb-2">
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

        <!-- ═══ ASIGNACIÓN A RUBROS ═══ -->
        <div class="p-4 rounded-xl bg-zinc-800/30 border border-zinc-700/50">
          <label class="block text-sm font-medium text-zinc-300 mb-2">
            Asignar a rubros
          </label>
          <p class="text-[11px] text-zinc-600 mb-3">Seleccioná en qué rubro(s) aparece este proyecto</p>
          {#if sectors.length === 0}
            <p class="text-xs text-zinc-600 italic">No hay rubros creados. Creálos primero en <a href="/admin/sectors" class="text-amber-400 hover:underline">Sectores</a>.</p>
          {:else}
            <div class="flex flex-wrap gap-2">
              {#each sectors as sector}
                <button
                  type="button"
                  on:click={() => toggleSector(sector.id)}
                  class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all active:scale-95 border
                    {selectedSectorIds.includes(sector.id)
                      ? 'bg-amber-500/20 border-amber-500/40 text-amber-400'
                      : 'bg-zinc-800 border-zinc-700 text-zinc-400 hover:border-zinc-600'}"
                >
                  {sector.name}
                </button>
              {/each}
            </div>
          {/if}
        </div>

        <!-- ═══ IMÁGENES MÚLTIPLES ═══ -->
        <div class="p-4 rounded-xl bg-zinc-800/30 border border-zinc-700/50">
          <label class="block text-sm font-medium text-zinc-300 mb-2">Imágenes del proyecto</label>
          <p class="text-[11px] text-zinc-600 mb-3">Subí varias imágenes — se mostrarán como carrusel en la web</p>

          <!-- Imágenes existentes (ya guardadas) -->
          {#if existingImageUrls.length > 0}
            <div class="flex flex-wrap gap-3 mb-4">
              {#each existingImageUrls as url, i}
                <div class="relative group w-24 h-24 rounded-lg overflow-hidden border border-zinc-700/50">
                  <img src={url} alt="Imagen {i + 1}" class="w-full h-full object-cover" loading="lazy" />
                  <button
                    on:click={() => removeExistingImage(i)}
                    class="absolute top-1 right-1 w-5 h-5 rounded-full bg-red-500/80 hover:bg-red-500 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-xs"
                    title="Eliminar imagen"
                  >✕</button>
                </div>
              {/each}
            </div>
          {:else if !editingId}
            <p class="text-xs text-zinc-600 italic mb-3">Aún no hay imágenes. Agregá algunas abajo.</p>
          {/if}

          <!-- Nuevas imágenes (sin guardar) -->
          {#if imagePreviews.length > 0}
            <div class="flex flex-wrap gap-3 mb-3">
              {#each imagePreviews as preview, i}
                <div class="relative group w-24 h-24 rounded-lg overflow-hidden border border-cyan-500/30">
                  <img src={preview} alt="Nueva {i + 1}" class="w-full h-full object-cover" />
                  <button
                    on:click={() => removeNewImage(i)}
                    class="absolute top-1 right-1 w-5 h-5 rounded-full bg-red-500/80 hover:bg-red-500 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-xs"
                    title="Quitar"
                  >✕</button>
                  <span class="absolute bottom-1 left-1 px-1 py-0.5 rounded bg-black/60 text-[8px] text-white">nueva</span>
                </div>
              {/each}
            </div>
          {/if}

          <!-- Botón de subida (también acepta arrastrar imágenes) -->
          <label
            on:dragover|preventDefault
            on:drop={handleDrop}
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-zinc-700 hover:bg-zinc-600 text-zinc-300 text-sm cursor-pointer transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            {newImageFiles.length > 0 ? 'Agregar más imágenes' : 'Seleccionar imágenes'}
            <input type="file" accept="image/*" multiple on:change={handleImagesSelected} class="hidden" />
          </label>
          <p class="text-[11px] text-zinc-600 mt-2">También podés arrastrar imágenes desde tu computadora.</p>
        </div>

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
        </div>
      </form>
    </div>

    <!-- ═══ LISTA DE PROYECTOS ═══ -->
    <div>
      <h2 class="text-lg font-semibold text-zinc-100 mb-4">
        Proyectos ({items.length})
      </h2>

      {#if items.length === 0}
        <p class="text-zinc-500 text-center py-8">No hay proyectos registrados</p>
      {:else}
        <div class="space-y-2">
          {#each items as item}
            {@const projectSectors = getProjectSectors(item.id)}
            <div class="bg-zinc-900 rounded-lg p-4 border border-zinc-800 flex items-start justify-between gap-4">
              <!-- Imagen thumbnail -->
              {#if item.image_urls && item.image_urls.length > 0}
                <div class="w-16 h-16 rounded-lg overflow-hidden shrink-0 bg-zinc-800 border border-zinc-700/50">
                  <img
                    src={item.image_urls[0]}
                    alt={item.title}
                    class="w-full h-full object-cover"
                    loading="lazy"
                  />
                </div>
              {:else}
                <div class="w-16 h-16 rounded-lg shrink-0 bg-zinc-800/50 border border-zinc-700/50 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-zinc-600"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                </div>
              {/if}

              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <span class="text-amber-400 font-medium">{item.title}</span>
                  {#each item.tags as tag}
                    <span class="text-xs px-2 py-0.5 bg-zinc-800 rounded-full text-zinc-500">{tag}</span>
                  {/each}
                </div>
                <p class="text-sm text-zinc-500 mt-1 line-clamp-1">{item.description}</p>
                <!-- Badges de sectores -->
                {#if projectSectors.length > 0}
                  <div class="flex flex-wrap gap-1.5 mt-2">
                    {#each projectSectors as s}
                      <span class="text-[10px] px-2 py-0.5 rounded-md font-medium border
                        {s.color_gradient.includes('amber') || s.color_gradient.includes('orange')
                          ? 'bg-amber-500/10 border-amber-500/20 text-amber-400/80'
                          : s.color_gradient.includes('emerald') || s.color_gradient.includes('teal')
                          ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400/80'
                          : s.color_gradient.includes('blue') || s.color_gradient.includes('cyan')
                          ? 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400/80'
                          : s.color_gradient.includes('blush') || s.color_gradient.includes('rose')
                          ? 'bg-rose-500/10 border-rose-500/20 text-rose-400/80'
                          : s.color_gradient.includes('violet') || s.color_gradient.includes('purple')
                          ? 'bg-violet-500/10 border-violet-500/20 text-violet-400/80'
                          : 'bg-zinc-700/30 border-zinc-700/50 text-zinc-400'}"
                      >
                        {s.name}
                      </span>
                    {/each}
                  </div>
                {:else}
                  <p class="text-[10px] text-zinc-600 mt-2 italic">Sin rubro asignado</p>
                {/if}
              </div>

              <div class="flex items-center gap-2 shrink-0">
                <button
                  on:click={() => editItem(item)}
                  class="px-3 py-1.5 text-sm bg-zinc-700 text-zinc-300 rounded-lg hover:bg-zinc-600 transition-colors"
                >
                  Editar
                </button>
                <button
                  on:click={() => deleteItem(item.id)}
                  class="px-3 py-1.5 text-sm bg-red-900/20 text-red-400 rounded-lg hover:bg-red-900/30 transition-colors"
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
  </div>
</div>
