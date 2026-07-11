<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { SectorResponse, ProjectResponse } from '$lib/types';

  const API = import.meta.env.PUBLIC_API_URL;

  let sectors: SectorResponse[] = [];
  let projects: ProjectResponse[] = [];
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // Modal
  let showModal = false;
  let editingId: number | null = null;

  // Formulario
  let name = '';
  let client_name = '';
  let description = '';
  let icon_path = '';
  let color_gradient = '';
  let selectedProjects: number[] = [];

  const iconPresets = [
    { label: 'Hostelería', path: 'M17 8h1a4 4 0 1 1 0 8h-1 M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z' },
    { label: 'Inmobiliaria', path: 'M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2' },
    { label: 'Talleres', path: 'M12 2 2 7l10 5 10-5-10-5Z m2 17 10 5 10-5' },
    { label: 'Salud', path: 'M22 12h-4l-3 9L9 3l-3 9H2' },
    { label: 'Belleza', path: 'M12 20h9 M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z' },
    { label: 'Logística', path: 'M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16' },
    { label: 'General', path: 'M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z' },
  ];

  const gradientPresets = [
    'from-amber-700/30 to-red-800/30',
    'from-emerald-500/30 to-teal-600/30',
    'from-amber-500/20 to-orange-600/20',
    'from-blue-500/20 to-cyan-600/20',
    'from-blush-400/30 to-rose-500/30',
    'from-violet-500/30 to-purple-700/30',
    'from-gray-500/20 to-zinc-600/20',
  ];

  onMount(async () => {
    await Promise.all([loadSectors(), loadProjects()]);
  });

  async function loadSectors() {
    try {
      sectors = await fetchApi<SectorResponse[]>('/api/v1/sectors/');
    } catch {
      sectors = [];
    } finally {
      loading = false;
    }
  }

  async function loadProjects() {
    try {
      projects = await fetchApi<ProjectResponse[]>('/api/v1/projects/');
    } catch {
      projects = [];
    }
  }

  function openNew() {
    editingId = null;
    name = '';
    client_name = '';
    description = '';
    icon_path = iconPresets[0].path;
    color_gradient = gradientPresets[0];
    selectedProjects = [];
    showModal = true;
  }

  function openEdit(sector: SectorResponse) {
    editingId = sector.id;
    name = sector.name;
    client_name = sector.client_name;
    description = sector.description || '';
    icon_path = sector.icon_path;
    color_gradient = sector.color_gradient;
    selectedProjects = [...sector.project_ids];
    showModal = true;
  }

  function closeModal() {
    showModal = false;
    editingId = null;
  }

  function toggleProject(projectId: number) {
    if (selectedProjects.includes(projectId)) {
      selectedProjects = selectedProjects.filter(id => id !== projectId);
    } else {
      selectedProjects = [...selectedProjects, projectId];
    }
  }

  async function handleSave() {
    if (!name || !client_name) {
      message = 'Nombre y cliente son obligatorios';
      messageType = 'error';
      return;
    }

    saving = true;
    message = '';

    const body = {
      name,
      client_name,
      description: description || null,
      icon_path,
      color_gradient,
      sort_order: editingId
        ? sectors.find(s => s.id === editingId)?.sort_order ?? 0
        : sectors.length + 1,
      project_ids: selectedProjects,
    };

    try {
      if (editingId) {
        await fetchApi(`/api/v1/sectors/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(body),
          headers: { 'Content-Type': 'application/json' },
        });
      } else {
        await fetchApi('/api/v1/sectors/', {
          method: 'POST',
          body: JSON.stringify(body),
          headers: { 'Content-Type': 'application/json' },
        });
      }
      message = editingId ? 'Sector actualizado' : 'Sector creado';
      messageType = 'success';
      closeModal();
      await loadSectors();
    } catch (e) {
      message = `Error: ${e.message}`;
      messageType = 'error';
    } finally {
      saving = false;
    }
  }

  async function handleDelete(id: number) {
    if (!confirm('¿Eliminar este sector? Los proyectos asignados no se eliminan.')) return;

    try {
      await fetchApi(`/api/v1/sectors/${id}`, { method: 'DELETE' });
      await loadSectors();
      message = 'Sector eliminado';
      messageType = 'success';
    } catch (e) {
      message = `Error: ${e.message}`;
      messageType = 'error';
    }
  }

  async function moveUp(index: number) {
    if (index === 0) return;
    const arr = [...sectors];
    [arr[index - 1], arr[index]] = [arr[index], arr[index - 1]];
    await saveOrder(arr);
  }

  async function moveDown(index: number) {
    if (index === sectors.length - 1) return;
    const arr = [...sectors];
    [arr[index], arr[index + 1]] = [arr[index + 1], arr[index]];
    await saveOrder(arr);
  }

  async function saveOrder(arr: SectorResponse[]) {
    try {
      await Promise.all(arr.map((s, i) =>
        fetchApi(`/api/v1/sectors/${s.id}`, {
          method: 'PUT',
          body: JSON.stringify({ sort_order: i + 1 }),
          headers: { 'Content-Type': 'application/json' },
        })
      ));
      sectors = arr;
      message = 'Orden actualizado';
      messageType = 'success';
    } catch (e) {
      message = `Error al ordenar: ${e.message}`;
      messageType = 'error';
    }
  }

  function getSectorProjects(sector: SectorResponse): ProjectResponse[] {
    return projects.filter(p => sector.project_ids.includes(p.id));
  }
</script>

<div class="space-y-6">
  <!-- Mensaje -->
  {#if message}
    <div class="p-4 rounded-xl text-sm font-medium {messageType === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}">
      {message}
    </div>
  {/if}

  <!-- Header -->
  <div class="flex items-center justify-between">
    <div>
      <h2 class="text-xl font-bold text-zinc-100">Sectores</h2>
      <p class="text-sm text-zinc-400">Gestioná los rubros y qué proyectos se muestran en cada uno.</p>
    </div>
    <button
      on:click={openNew}
      class="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-black text-sm font-bold rounded-xl transition-all"
    >
      + Nuevo Sector
    </button>
  </div>

  <!-- Lista -->
  {#if loading}
    <div class="text-center py-12 text-zinc-500">Cargando...</div>
  {:else if sectors.length === 0}
    <div class="text-center py-12 text-zinc-500">No hay sectores todavía. Creá el primero.</div>
  {:else}
    <div class="space-y-3">
      {#each sectors as sector, i (sector.id)}
        <div class="bg-zinc-900/50 border border-zinc-800 rounded-xl p-5 hover:border-zinc-700 transition-colors">
          <div class="flex items-start justify-between gap-4">
            <div class="flex items-center gap-4 min-w-0">
              <!-- Reorder buttons -->
              <div class="flex flex-col gap-0.5 shrink-0">
                <button on:click={() => moveUp(i)} disabled={i === 0}
                  class="p-0.5 rounded text-zinc-600 hover:text-zinc-300 disabled:opacity-20 disabled:cursor-not-allowed">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m18 15-6-6-6 6"/></svg>
                </button>
                <button on:click={() => moveDown(i)} disabled={i === sectors.length - 1}
                  class="p-0.5 rounded text-zinc-600 hover:text-zinc-300 disabled:opacity-20 disabled:cursor-not-allowed">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
                </button>
              </div>

              <!-- Icon -->
              <div class="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber-400"><path d={sector.icon_path} /></svg>
              </div>

              <!-- Info -->
              <div class="min-w-0">
                <h3 class="font-bold text-white text-sm">{sector.name}</h3>
                <p class="text-zinc-500 text-xs truncate">{sector.client_name}</p>
                {#if sector.description}
                  <p class="text-zinc-600 text-xs mt-1 truncate max-w-md">{sector.description}</p>
                {/if}
                <!-- Projects badges -->
                {#if getSectorProjects(sector).length > 0}
                  <div class="flex flex-wrap gap-1.5 mt-2">
                    {#each getSectorProjects(sector) as p}
                      <span class="px-2 py-0.5 text-[10px] font-medium rounded-md bg-white/5 border border-white/10 text-zinc-400">{p.title}</span>
                    {/each}
                  </div>
                {:else}
                  <p class="text-zinc-600 text-xs mt-2 italic">Sin proyectos asignados</p>
                {/if}
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 shrink-0">
              <button on:click={() => openEdit(sector)}
                class="px-3 py-1.5 text-xs font-medium rounded-lg bg-white/5 border border-white/10 text-zinc-400 hover:text-white hover:border-white/30 transition-all">
                Editar
              </button>
              <button on:click={() => handleDelete(sector.id)}
                class="px-3 py-1.5 text-xs font-medium rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 hover:bg-red-500/20 transition-all">
                Eliminar
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<!-- Modal -->
{#if showModal}
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" on:click={closeModal}>
    <div class="bg-zinc-900 border border-zinc-800 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto p-6" on:click|stopPropagation>
      <h3 class="text-lg font-bold text-white mb-6">{editingId ? 'Editar Sector' : 'Nuevo Sector'}</h3>

      <div class="space-y-4">
        <!-- Nombre -->
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Nombre del rubro</label>
          <input bind:value={name} placeholder="Ej: Hostelería"
            class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 transition-colors" />
        </div>

        <!-- Cliente -->
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Nombre del cliente</label>
          <input bind:value={client_name} placeholder="Ej: Café Mi Tierra"
            class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 transition-colors" />
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Descripción (opcional)</label>
          <textarea bind:value={description} placeholder="Breve descripción del rubro..."
            class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 transition-colors resize-none" rows="2"></textarea>
        </div>

        <!-- Icono -->
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Ícono SVG</label>
          <div class="flex flex-wrap gap-2 mb-2">
            {#each iconPresets as preset}
              <button on:click={() => icon_path = preset.path}
                class="px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all
                  {icon_path === preset.path ? 'bg-amber-500/20 border border-amber-500/30 text-amber-400' : 'bg-zinc-800/50 border border-zinc-700 text-zinc-400 hover:border-zinc-600'}">
                {preset.label}
              </button>
            {/each}
          </div>
          <input bind:value={icon_path} placeholder="SVG path data"
            class="w-full px-3 py-2 rounded-lg bg-zinc-800/50 border border-zinc-700 text-zinc-300 text-xs font-mono focus:outline-none focus:border-amber-500/50 transition-colors" />
        </div>

        <!-- Gradiente -->
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Color de fondo</label>
          <div class="flex flex-wrap gap-2">
            {#each gradientPresets as g}
              <button on:click={() => color_gradient = g}
                class="w-8 h-8 rounded-lg border-2 transition-all {color_gradient === g ? 'border-amber-400 scale-110' : 'border-transparent'} bg-gradient-to-br {g}">
              </button>
            {/each}
          </div>
        </div>

        <!-- Proyectos asignados -->
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Proyectos asignados</label>
          {#if projects.length === 0}
            <p class="text-zinc-600 text-xs italic">No hay proyectos creados. Creá proyectos primero en la sección Proyectos.</p>
          {:else}
            <div class="max-h-40 overflow-y-auto space-y-1.5 rounded-xl bg-zinc-800/30 border border-zinc-800 p-2">
              {#each projects as project}
                <label class="flex items-center gap-3 px-2 py-1.5 rounded-lg hover:bg-white/5 cursor-pointer transition-colors">
                  <input type="checkbox" checked={selectedProjects.includes(project.id)} on:change={() => toggleProject(project.id)}
                    class="rounded border-zinc-600 bg-zinc-700 text-amber-500 focus:ring-amber-500/30" />
                  <span class="text-sm text-zinc-300">{project.title}</span>
                </label>
              {/each}
            </div>
          {/if}
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-3 mt-8 pt-4 border-t border-zinc-800">
        <button on:click={closeModal}
          class="px-4 py-2 text-sm font-medium text-zinc-400 hover:text-white transition-colors">
          Cancelar
        </button>
        <button on:click={handleSave} disabled={saving}
          class="px-5 py-2 bg-amber-500 hover:bg-amber-400 text-black text-sm font-bold rounded-xl transition-all disabled:opacity-50">
          {saving ? 'Guardando...' : editingId ? 'Actualizar' : 'Crear Sector'}
        </button>
      </div>
    </div>
  </div>
{/if}
