<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { StackResponse } from '$lib/types';

  const API = import.meta.env.PUBLIC_API_URL;

  let items: StackResponse[] = [];
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';
  let editingId: number | null = null;

  // Formulario
  let name = '';
  let category = '';
  let icon = '';
  let description = '';
  let color = '';
  let border = '';
  let glow = '';

  const categories = ['Frontend', 'Backend', 'DevOps', 'Herramientas'];
  const iconOptions = [
    'Globe', 'Palette', 'FileCode2', 'Atom', 'Rocket', 'LayoutTemplate',
    'Terminal', 'Zap', 'Layers', 'Server', 'Lock', 'Database', 'Container',
    'GitBranch', 'Github', 'Triangle', 'Cloud', 'Code2', 'Send', 'BrainCircuit',
    'Gauge', 'Monitor', 'HardDrive', 'Settings'
  ];

  onMount(async () => {
    await loadItems();
  });

  async function loadItems() {
    try {
      items = await fetchApi<StackResponse[]>('/api/v1/stacks/');
    } catch {
      items = [];
    } finally {
      loading = false;
    }
  }

  function resetForm() {
    name = '';
    category = '';
    icon = '';
    description = '';
    color = '';
    border = '';
    glow = '';
    editingId = null;
  }

  function editItem(item: StackResponse) {
    name = item.name;
    category = item.category;
    icon = item.icon;
    description = item.description;
    color = item.color;
    border = item.border;
    glow = item.glow;
    editingId = item.id;
  }

  async function handleSubmit() {
    saving = true;
    message = '';

    try {
      const data = {
        name,
        category,
        icon,
        description,
        color,
        border,
        glow
      };

      const url = editingId 
        ? `${API}/api/v1/stacks/${editingId}`
        : `${API}/api/v1/stacks/`;
      
      const method = editingId ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
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
    if (!confirm('¿Estás seguro de eliminar este item?')) return;

    try {
      const res = await fetch(`${API}/api/v1/stacks/${id}`, {
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
    <span class="animate-spin inline-block w-4 h-4 border-2
                 border-zinc-600 border-t-amber-400 rounded-full"></span>
    <span class="text-sm">Cargando...</span>
  </div>
{:else}
  <div class="space-y-8">
    <!-- Formulario -->
    <div class="bg-zinc-900 rounded-xl p-6 border border-zinc-800">
      <h2 class="text-lg font-semibold text-zinc-100 mb-4">
        {editingId ? 'Editar Tecnología' : 'Nueva Tecnología'}
      </h2>
      
      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-300 mb-2">
              Nombre
            </label>
            <input
              type="text"
              bind:value={name}
              required
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="HTML5"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-zinc-300 mb-2">
              Categoría
            </label>
            <select
              bind:value={category}
              required
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
            >
              <option value="">Seleccionar</option>
              {#each categories as cat}
                <option value={cat}>{cat}</option>
              {/each}
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-zinc-300 mb-2">
            Icono
          </label>
          <select
            bind:value={icon}
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
          <label class="block text-sm font-medium text-zinc-300 mb-2">
            Descripción
          </label>
          <input
            type="text"
            bind:value={description}
            required
            class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors"
            placeholder="Estructura Web"
          />
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-zinc-300 mb-2">
              Color
            </label>
            <input
              type="text"
              bind:value={color}
              required
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="text-orange-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-zinc-300 mb-2">
              Border
            </label>
            <input
              type="text"
              bind:value={border}
              required
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="group-hover:border-orange-500/50"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-zinc-300 mb-2">
              Glow
            </label>
            <input
              type="text"
              bind:value={glow}
              required
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]"
            />
          </div>
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
            {saving ? 'Guardando...' : (editingId ? 'Actualizar' : 'Agregar')}
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
            <span
              class="text-sm {messageType === 'success'
                ? 'text-emerald-400'
                : 'text-red-400'}"
            >
              {message}
            </span>
          {/if}
        </div>
      </form>
    </div>

    <!-- Lista de items -->
    <div>
      <h2 class="text-lg font-semibold text-zinc-100 mb-4">
        Tecnologías ({items.length})
      </h2>
      
      {#if items.length === 0}
        <p class="text-zinc-500 text-center py-8">
          No hay tecnologías registradas
        </p>
      {:else}
        <div class="space-y-2">
          {#each items as item}
            <div class="bg-zinc-900 rounded-lg p-4 border border-zinc-800 flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-3">
                  <span class="text-amber-400 font-medium">{item.name}</span>
                  <span class="text-xs px-2 py-1 bg-zinc-800 rounded-full text-zinc-400">
                    {item.category}
                  </span>
                </div>
                <p class="text-sm text-zinc-500 mt-1">{item.description}</p>
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
