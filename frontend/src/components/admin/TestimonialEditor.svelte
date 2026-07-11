<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { TestimonialResponse } from '$lib/types';

  let items: TestimonialResponse[] = [];
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';
  let showModal = false;
  let editingId: number | null = null;

  // Form
  let name = '';
  let role = '';
  let company = '';
  let content = '';
  let rating = 5;
  let avatar_url = '';
  let is_active = true;

  onMount(async () => {
    await loadItems();
  });

  async function loadItems() {
    try {
      items = await fetchApi<TestimonialResponse[]>('/api/v1/testimonials/all');
    } catch {
      items = [];
    } finally {
      loading = false;
    }
  }

  function openNew() {
    editingId = null;
    name = ''; role = ''; company = ''; content = ''; rating = 5; avatar_url = ''; is_active = true;
    showModal = true;
  }

  function openEdit(item: TestimonialResponse) {
    editingId = item.id;
    name = item.name; role = item.role || ''; company = item.company || '';
    content = item.content; rating = item.rating; avatar_url = item.avatar_url || ''; is_active = item.is_active;
    showModal = true;
  }

  function closeModal() { showModal = false; editingId = null; }

  async function handleSave() {
    if (!name || !content) { message = 'Nombre y contenido son obligatorios'; messageType = 'error'; return; }
    saving = true; message = '';

    const body = { name, role: role || null, company: company || null, content, rating, avatar_url: avatar_url || null, is_active, sort_order: editingId ? items.find(i => i.id === editingId)?.sort_order ?? 0 : items.length + 1 };

    try {
      if (editingId) {
        await fetchApi(`/api/v1/testimonials/${editingId}`, { method: 'PUT', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } });
      } else {
        await fetchApi('/api/v1/testimonials/', { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' } });
      }
      message = editingId ? 'Testimonio actualizado' : 'Testimonio creado';
      messageType = 'success'; closeModal(); await loadItems();
    } catch (e) { message = `Error: ${e.message}`; messageType = 'error'; }
    finally { saving = false; }
  }

  async function handleDelete(id: number) {
    if (!confirm('¿Eliminar este testimonio?')) return;
    try {
      await fetchApi(`/api/v1/testimonials/${id}`, { method: 'DELETE' });
      await loadItems();
      message = 'Testimonio eliminado'; messageType = 'success';
    } catch (e) { message = `Error: ${e.message}`; messageType = 'error'; }
  }

  function stars(n: number): string {
    return '★'.repeat(n) + '☆'.repeat(5 - n);
  }
</script>

<div class="space-y-6">
  {#if message}
    <div class="p-4 rounded-xl text-sm font-medium {messageType === 'success' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}">
      {message}
    </div>
  {/if}

  <div class="flex items-center justify-between">
    <div>
      <h2 class="text-xl font-bold text-zinc-100">Testimonios</h2>
      <p class="text-sm text-zinc-400">Gestioná los testimonios que se muestran en la landing page.</p>
    </div>
    <button on:click={openNew}
      class="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-black text-sm font-bold rounded-xl transition-all">
      + Nuevo Testimonio
    </button>
  </div>

  {#if loading}
    <div class="text-center py-12 text-zinc-500">Cargando...</div>
  {:else if items.length === 0}
    <div class="text-center py-12 text-zinc-500">No hay testimonios todavía. Creá el primero.</div>
  {:else}
    <div class="space-y-3">
      {#each items as item (item.id)}
        <div class="bg-zinc-900/50 border border-zinc-800 rounded-xl p-5 hover:border-zinc-700 transition-colors">
          <div class="flex items-start justify-between gap-4">
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-3 mb-1">
                <div class="w-9 h-9 rounded-full bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 font-bold text-sm">
                  {item.name.charAt(0)}
                </div>
                <div>
                  <h3 class="font-bold text-white text-sm">{item.name}</h3>
                  <p class="text-zinc-500 text-xs">{item.role}{item.company ? ` — ${item.company}` : ''}</p>
                </div>
                <span class="ml-auto text-amber-400 text-sm">{stars(item.rating)}</span>
              </div>
              <p class="text-zinc-400 text-sm leading-relaxed mt-2 line-clamp-3">"{item.content}"</p>
              <div class="flex items-center gap-3 mt-2">
                {#if !item.is_active}
                  <span class="px-2 py-0.5 text-[10px] font-medium rounded-md bg-red-500/10 text-red-400 border border-red-500/20">Inactivo</span>
                {/if}
              </div>
            </div>
            <div class="flex gap-2 shrink-0">
              <button on:click={() => openEdit(item)}
                class="px-3 py-1.5 text-xs font-medium rounded-lg bg-white/5 border border-white/10 text-zinc-400 hover:text-white hover:border-white/30 transition-all">
                Editar
              </button>
              <button on:click={() => handleDelete(item.id)}
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
      <h3 class="text-lg font-bold text-white mb-6">{editingId ? 'Editar Testimonio' : 'Nuevo Testimonio'}</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Nombre</label>
          <input bind:value={name} placeholder="Ej: Carlos Martínez"
            class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50" />
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium text-zinc-400 mb-1.5">Rol</label>
            <input bind:value={role} placeholder="Ej: Dueño"
              class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50" />
          </div>
          <div>
            <label class="block text-xs font-medium text-zinc-400 mb-1.5">Empresa</label>
            <input bind:value={company} placeholder="Ej: Café Mi Tierra"
              class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50" />
          </div>
        </div>
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Contenido del testimonio</label>
          <textarea bind:value={content} placeholder="Lo que dijo el cliente..."
            class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 resize-none" rows="3"></textarea>
        </div>
        <div>
          <label class="block text-xs font-medium text-zinc-400 mb-1.5">Calificación</label>
          <div class="flex gap-1">
            {#each [1,2,3,4,5] as n}
              <button on:click={() => rating = n}
                class="w-9 h-9 rounded-lg text-lg transition-all {n <= rating ? 'text-amber-400 bg-amber-500/10 border border-amber-500/20' : 'text-zinc-600 bg-zinc-800/50 border border-zinc-700'}">
                ★
              </button>
            {/each}
          </div>
        </div>
        <div>
          <label class="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" bind:checked={is_active}
              class="rounded border-zinc-600 bg-zinc-700 text-amber-500 focus:ring-amber-500/30" />
            <span class="text-sm text-zinc-300">Activo (visible en la web)</span>
          </label>
        </div>
      </div>
      <div class="flex justify-end gap-3 mt-8 pt-4 border-t border-zinc-800">
        <button on:click={closeModal} class="px-4 py-2 text-sm font-medium text-zinc-400 hover:text-white">Cancelar</button>
        <button on:click={handleSave} disabled={saving}
          class="px-5 py-2 bg-amber-500 hover:bg-amber-400 text-black text-sm font-bold rounded-xl disabled:opacity-50">
          {saving ? 'Guardando...' : editingId ? 'Actualizar' : 'Crear Testimonio'}
        </button>
      </div>
    </div>
  </div>
{/if}
