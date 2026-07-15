<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { FooterResponse } from '$lib/types';
  import { dispatchDataChange } from '$lib/dataEvents';

  const API = import.meta.env.PUBLIC_API_URL;

  let data: FooterResponse | null = null;
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // un campo por cada campo del schema Create
  let name = '';
  let description = '';
  let location = '';
  let email = '';
  let github_url = '';
  let linkedin_url = '';
  let twitter_url = '';
  let quick_links: { text: string; href: string }[] = [];

  onMount(async () => {
    try {
      data = await fetchApi<FooterResponse>('/api/v1/footers/latest/');
      name = data.name ?? '';
      description = data.description ?? '';
      location = data.location ?? '';
      email = data.email ?? '';
      github_url = data.github_url ?? '';
      linkedin_url = data.linkedin_url ?? '';
      twitter_url = data.twitter_url ?? '';
      quick_links = data.quick_links ?? [
        { text: 'Inicio', href: '#inicio' },
        { text: 'Sobre Mí', href: '#sobre-mi' },
        { text: 'Stack Tecnológico', href: '#stack' },
        { text: 'Pasiones', href: '#pasiones' },
      ];
    } catch {
      message = 'Error al cargar los datos';
      messageType = 'error';
    } finally {
      loading = false;
    }
  });

  async function handleSubmit() {
    if (!data) return;
    saving = true;
    message = '';

    try {
      // Footer usa FormData (no JSON) según el backend
      const formData = new FormData();
      formData.append('name', name);
      formData.append('description', description);
      formData.append('location', location);
      formData.append('email', email);
      formData.append('github_url', github_url || '');
      formData.append('linkedin_url', linkedin_url || '');
      formData.append('twitter_url', twitter_url || '');
      formData.append('quick_links', JSON.stringify(quick_links));

      const res = await fetch(`${API}/api/v1/footers/${data.id}`, {
        method: 'PUT',
        body: formData,
        // NO agregar Content-Type manualmente para FormData
      });

      if (!res.ok) throw new Error();
      data = await res.json();
      message = 'Guardado correctamente';
      messageType = 'success';

      // Disparar evento para actualizar componentes públicos
      dispatchDataChange('footer', 'update', data);
    } catch {
      message = 'Error al guardar los cambios';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }

  function addQuickLink() {
    quick_links = [...quick_links, { text: '', href: '' }];
  }

  function removeQuickLink(index: number) {
    quick_links = quick_links.filter((_, i) => i !== index);
  }

  function updateQuickLink(index: number, field: 'text' | 'href', value: string) {
    quick_links = quick_links.map((link, i) => (i === index ? { ...link, [field]: value } : link));
  }
</script>

<div class="p-6 md:p-10">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-zinc-100 mb-2">Footer</h1>
      <p class="text-zinc-400">Gestiona la información del pie de página y enlaces rápidos.</p>
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
        <!-- Información principal -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="name" class="block text-sm font-medium text-zinc-300 mb-2"> Nombre </label>
            <input
              id="name"
              type="text"
              bind:value={name}
              required
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="Tu nombre completo"
            />
          </div>

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
              placeholder="Ciudad, País"
            />
          </div>
        </div>

        <!-- Descripción -->
        <div>
          <label for="description" class="block text-sm font-medium text-zinc-300 mb-2">
            Descripción
          </label>
          <textarea
            id="description"
            bind:value={description}
            required
            rows={3}
            class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                   text-zinc-100 placeholder-zinc-500
                   focus:outline-none focus:border-amber-400 focus:ring-1
                   focus:ring-amber-400 transition-colors resize-none"
            placeholder="Breve descripción profesional..."
          ></textarea>
        </div>

        <!-- Email y redes sociales -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="email" class="block text-sm font-medium text-zinc-300 mb-2"> Email </label>
            <input
              id="email"
              type="email"
              bind:value={email}
              required
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="tu@email.com"
            />
          </div>

          <div>
            <label for="github_url" class="block text-sm font-medium text-zinc-300 mb-2">
              GitHub URL
            </label>
            <input
              id="github_url"
              type="url"
              bind:value={github_url}
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="https://github.com/usuario"
            />
          </div>
        </div>

        <!-- Redes sociales adicionales -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="linkedin_url" class="block text-sm font-medium text-zinc-300 mb-2">
              LinkedIn URL
            </label>
            <input
              id="linkedin_url"
              type="url"
              bind:value={linkedin_url}
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="https://linkedin.com/in/usuario"
            />
          </div>

          <div>
            <label for="twitter_url" class="block text-sm font-medium text-zinc-300 mb-2">
              Twitter URL
            </label>
            <input
              id="twitter_url"
              type="url"
              bind:value={twitter_url}
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="https://twitter.com/usuario"
            />
          </div>
        </div>

        <!-- Enlaces rápidos -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <label for="quick_links" class="text-sm font-medium text-zinc-300">
              Enlaces Rápidos
            </label>
            <button
              type="button"
              on:click={addQuickLink}
              class="px-3 py-1.5 text-sm bg-amber-500 text-zinc-900 rounded-lg
                     hover:bg-amber-400 transition-colors font-medium"
            >
              + Agregar enlace
            </button>
          </div>

          <div class="space-y-3">
            {#each quick_links as link, index}
              <div class="flex gap-3 items-center">
                <input
                  type="text"
                  bind:value={link.text}
                  placeholder="Texto del enlace"
                  class="flex-1 px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                         text-zinc-100 placeholder-zinc-500
                         focus:outline-none focus:border-amber-400 focus:ring-1
                         focus:ring-amber-400 transition-colors"
                />
                <input
                  type="text"
                  bind:value={link.href}
                  placeholder="#sección o /ruta"
                  class="flex-1 px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700
                         text-zinc-100 placeholder-zinc-500
                         focus:outline-none focus:border-amber-400 focus:ring-1
                         focus:ring-amber-400 transition-colors"
                />
                <button
                  type="button"
                  on:click={() => removeQuickLink(index)}
                  class="p-2 text-red-400 hover:bg-red-500/10 rounded-lg
                         transition-colors"
                  title="Eliminar enlace"
                >
                  <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path d="M18 6L6 18M6 6l12 12" />
                  </svg>
                </button>
              </div>
            {/each}
          </div>

          {#if quick_links.length === 0}
            <p class="text-zinc-500 text-sm italic">
              No hay enlaces configurados. Agrega algunos para que aparezcan en el footer.
            </p>
          {/if}
        </div>

        <!-- Botones de acción -->
        <div class="flex items-center gap-4 pt-6 border-t border-zinc-800">
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
        </div>
      </form>

      <!-- Mensaje de feedback -->
      {#if message}
        <div
          class="mt-4 p-4 rounded-lg border {messageType === 'success'
            ? 'bg-emerald-900/20 border-emerald-500/30 text-emerald-400'
            : 'bg-red-900/20 border-red-500/30 text-red-400'}"
        >
          {message}
        </div>
      {/if}
    {/if}
  </div>
</div>
