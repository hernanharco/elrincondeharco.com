<svelte:options runes={false} />

<script lang="ts">
  let showModal = false;
  let name = '';
  let role = '';
  let company = '';
  let content = '';
  let rating = 5;
  let sending = false;
  let sent = false;
  let error = '';

  const API = import.meta.env.PUBLIC_API_URL || 'http://localhost:8001';

  function openForm() {
    showModal = true;
    sent = false;
    error = '';
  }

  function closeForm() {
    showModal = false;
    // Reset form si no se envió
    if (!sent) {
      name = ''; role = ''; company = ''; content = ''; rating = 5;
    }
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    if (!name.trim() || !content.trim()) return;

    sending = true;
    error = '';

    try {
      const res = await fetch(`${API}/api/v1/testimonials/public`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          role: role.trim() || null,
          company: company.trim() || null,
          content: content.trim(),
          rating,
        }),
      });

      if (!res.ok) throw new Error('Error al enviar');

      sent = true;
    } catch (err) {
      error = 'No se pudo enviar. ¿Estás conectado a internet?';
    } finally {
      sending = false;
    }
  }
</script>

<div class="text-center mt-16 pt-16 border-t border-white/5">
  <button
    on:click={openForm}
    class="inline-flex items-center gap-2 px-6 py-3 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-xl transition-all shadow-lg hover:shadow-amber-500/20"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
    Dejá tu testimonio
  </button>
</div>

<!-- Modal -->
{#if showModal}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
    on:click={closeForm}
    role="dialog"
    aria-modal="true"
  >
    <div
      class="bg-zinc-900 border border-zinc-800 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto p-6 shadow-2xl"
      on:click|stopPropagation
    >
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h3 class="text-lg font-bold text-white">Dejá tu testimonio</h3>
          <p class="text-sm text-zinc-500">Si trabajamos juntos, me encantaría saber tu experiencia</p>
        </div>
        <button on:click={closeForm} class="p-1.5 rounded-lg hover:bg-zinc-800 text-zinc-500 hover:text-zinc-300 transition-all" aria-label="Cerrar">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>
      </div>

      {#if sent}
        <!-- Success -->
        <div class="py-8 text-center">
          <div class="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-emerald-400"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <p class="text-emerald-400 font-bold text-xl mb-1">¡Gracias por tu testimonio!</p>
          <p class="text-emerald-400/70 text-sm mb-6">Será revisado y publicado pronto.</p>
          <button on:click={closeForm}
            class="px-6 py-2.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-sm font-medium rounded-xl transition-all">
            Cerrar
          </button>
        </div>
      {:else}
        <!-- Form -->
        <form on:submit={handleSubmit} class="space-y-4">
          {#if error}
            <div class="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">{error}</div>
          {/if}

          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div>
              <label for="tf-name" class="block text-xs font-medium text-zinc-400 mb-1">Nombre *</label>
              <input id="tf-name" bind:value={name} required
                class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 transition-colors"
                placeholder="Tu nombre" />
            </div>
            <div>
              <label for="tf-role" class="block text-xs font-medium text-zinc-400 mb-1">Rol</label>
              <input id="tf-role" bind:value={role}
                class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 transition-colors"
                placeholder="Ej: Dueño" />
            </div>
            <div>
              <label for="tf-company" class="block text-xs font-medium text-zinc-400 mb-1">Empresa</label>
              <input id="tf-company" bind:value={company}
                class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 transition-colors"
                placeholder="Ej: Café Mi Tierra" />
            </div>
          </div>

          <div>
            <label for="tf-content" class="block text-xs font-medium text-zinc-400 mb-1">Tu experiencia *</label>
            <textarea id="tf-content" bind:value={content} required rows={3}
              class="w-full px-3 py-2.5 rounded-xl bg-zinc-800/50 border border-zinc-700 text-white text-sm placeholder-zinc-600 focus:outline-none focus:border-amber-500/50 transition-colors resize-none"
              placeholder="Contame cómo fue trabajar conmigo..."></textarea>
          </div>

          <div class="flex items-center justify-between gap-4 pt-2">
            <div class="flex items-center gap-2">
              <span class="text-xs text-zinc-400">Calificación:</span>
              <div class="flex gap-0.5">
                {#each [1,2,3,4,5] as n}
                  <button type="button" on:click={() => rating = n}
                    class="p-0.5 transition-all {n <= rating ? 'text-amber-400' : 'text-zinc-700 hover:text-zinc-500'}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill={n <= rating ? 'currentColor' : 'none'} stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                  </button>
                {/each}
              </div>
            </div>

            <button type="submit" disabled={sending}
              class="px-6 py-2.5 bg-amber-500 hover:bg-amber-400 text-black text-sm font-bold rounded-xl transition-all disabled:opacity-50 shrink-0">
              {sending ? 'Enviando...' : 'Enviar testimonio'}
            </button>
          </div>
        </form>
      {/if}
    </div>
  </div>
{/if}
