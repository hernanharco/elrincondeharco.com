<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { SiteSettingsResponse, SocialNetworks } from '$lib/types';
  import { dispatchDataChange } from '$lib/dataEvents';

  const API = import.meta.env.PUBLIC_API_URL;

  let data: SiteSettingsResponse | null = null;
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // Campos del formulario
  let brand_name = '';
  let site_url = '';
  let legal_name = '';
  let slogan = '';
  let copyright_notice = '';
  let contact_email = '';
  let github_url = '';
  let linkedin_url = '';
  let twitter_url = '';
  let is_active = true;

  // CTA
  let cta_title = '';
  let cta_description = '';
  let cta_features_str = '';
  let cta_primary_text = '';
  let cta_secondary_text = '';

  onMount(async () => {
    try {
      data = await fetchApi<SiteSettingsResponse>('/api/v1/site-settings/latest/');
      brand_name = data.brand_name;
      site_url = data.site_url;
      legal_name = data.legal_name;
      slogan = data.slogan || '';
      copyright_notice = data.copyright_notice;
      contact_email = data.contact_email;
      github_url = data.social_networks?.github || '';
      linkedin_url = data.social_networks?.linkedin || '';
      twitter_url = data.social_networks?.twitter || '';
      is_active = data.is_active;
      cta_title = data.cta_title ?? '';
      cta_description = data.cta_description ?? '';
      cta_features_str = (data.cta_features ?? []).join('\n');
      cta_primary_text = data.cta_primary_text ?? '';
      cta_secondary_text = data.cta_secondary_text ?? '';
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
      // SiteSettings usa FormData según el backend
      const formData = new FormData();
      formData.append('brand_name', brand_name);
      formData.append('site_url', site_url);
      formData.append('legal_name', legal_name);
      formData.append('slogan', slogan);
      formData.append('copyright_notice', copyright_notice);
      formData.append('contact_email', contact_email);

      // Social networks como JSON string
      const socialNetworks: SocialNetworks = {
        github: github_url.trim() || null,
        linkedin: linkedin_url.trim() || null,
        twitter: twitter_url.trim() || null,
      };
      formData.append('social_networks', JSON.stringify(socialNetworks));
      formData.append('is_active', is_active.toString());
      // CTA
      formData.append('cta_title', cta_title);
      formData.append('cta_description', cta_description);
      formData.append('cta_features', JSON.stringify(cta_features_str.split('\n').map(s => s.trim()).filter(s => s)));
      formData.append('cta_primary_text', cta_primary_text);
      formData.append('cta_secondary_text', cta_secondary_text);

      const res = await fetch(`${API}/api/v1/site-settings/${data.id}`, {
        method: 'PUT',
        body: formData,
      });

      if (!res.ok) throw new Error();
      data = await res.json();
      message = 'Guardado correctamente';
      messageType = 'success';

      // Disparar evento para actualizar componentes públicos
      dispatchDataChange('site-settings', 'update', data);
    } catch {
      message = 'Error al guardar los cambios';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }
</script>

<div class="p-6 md:p-10">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-zinc-100 mb-2">Configuración del Sitio</h1>
      <p class="text-zinc-400">Gestiona la configuración general de tu marca y sitio web.</p>
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
        <!-- Información de la Marca -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-amber-400 mb-4">Información de la Marca</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="brand_name" class="block text-sm font-medium text-zinc-300 mb-2">
                Nombre de la Marca
              </label>
              <input
                id="brand_name"
                type="text"
                bind:value={brand_name}
                required
                class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                       text-zinc-100 placeholder-zinc-500
                       focus:outline-none focus:border-amber-400 focus:ring-1
                       focus:ring-amber-400 transition-colors"
                placeholder="elRincondelHarco.com"
              />
            </div>

            <div>
              <label for="site_url" class="block text-sm font-medium text-zinc-300 mb-2">
                URL del Sitio
              </label>
              <input
                id="site_url"
                type="url"
                bind:value={site_url}
                required
                class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                       text-zinc-100 placeholder-zinc-500
                       focus:outline-none focus:border-amber-400 focus:ring-1
                       focus:ring-amber-400 transition-colors"
                placeholder="https://elrincondelharco.com"
              />
            </div>
          </div>

          <div>
            <label for="legal_name" class="block text-sm font-medium text-zinc-300 mb-2">
              Nombre Legal
            </label>
            <input
              id="legal_name"
              type="text"
              bind:value={legal_name}
              required
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="Hernan Arango Cortes"
            />
          </div>

          <div>
            <label for="slogan" class="block text-sm font-medium text-zinc-300 mb-2">
              Slogan
            </label>
            <input
              id="slogan"
              type="text"
              bind:value={slogan}
              class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                     text-zinc-100 placeholder-zinc-500
                     focus:outline-none focus:border-amber-400 focus:ring-1
                     focus:ring-amber-400 transition-colors"
              placeholder="Programador Full Stack enfocado en velocidad y rendimiento."
            />
          </div>
        </div>

        <!-- Contacto y Legal -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-amber-400 mb-4">Contacto y Legal</h2>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="contact_email" class="block text-sm font-medium text-zinc-300 mb-2">
                Email de Contacto
              </label>
              <input
                id="contact_email"
                type="email"
                bind:value={contact_email}
                required
                class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                       text-zinc-100 placeholder-zinc-500
                       focus:outline-none focus:border-amber-400 focus:ring-1
                       focus:ring-amber-400 transition-colors"
                placeholder="hernan.harco@gmail.com"
              />
            </div>

            <div>
              <label for="copyright_notice" class="block text-sm font-medium text-zinc-300 mb-2">
                Aviso de Copyright
              </label>
              <input
                id="copyright_notice"
                type="text"
                bind:value={copyright_notice}
                required
                class="w-full px-4 py-2.5 rounded-lg bg-zinc-800 border border-zinc-700
                       text-zinc-100 placeholder-zinc-500
                       focus:outline-none focus:border-amber-400 focus:ring-1
                       focus:ring-amber-400 transition-colors"
                placeholder="Todos los derechos reservados."
              />
            </div>
          </div>
        </div>

        <!-- Redes Sociales -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-amber-400 mb-4">Redes Sociales</h2>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
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
                placeholder="https://github.com/hernanharco"
              />
            </div>

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
                placeholder="https://www.linkedin.com/in/hernan-harco/"
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
        </div>

        <!-- ═══ CTA (Call To Action) ═══ -->
        <div class="space-y-4 p-6 rounded-xl bg-zinc-900/50 border border-zinc-800">
          <h2 class="text-xl font-semibold text-amber-400 mb-4">Sección CTA (Contacto)</h2>
          <p class="text-xs text-zinc-500 mb-4">Editá el contenido de la sección de contacto al final de la página.</p>

          <div>
            <label for="cta_title" class="block text-sm font-medium text-zinc-300 mb-2">Título (acepta HTML)</label>
            <input id="cta_title" type="text" bind:value={cta_title}
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-400 transition-colors"
              placeholder="¿Listo para construir algo grande?" />
          </div>

          <div>
            <label for="cta_description" class="block text-sm font-medium text-zinc-300 mb-2">Descripción</label>
            <textarea id="cta_description" bind:value={cta_description} rows={2}
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-400 transition-colors resize-none"
              placeholder="Tenés la idea, yo tengo la experiencia..."></textarea>
          </div>

          <div>
            <label for="cta_features" class="block text-sm font-medium text-zinc-300 mb-2">Características (una por línea)</label>
            <textarea id="cta_features" bind:value={cta_features_str} rows={3}
              class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-400 transition-colors resize-none"
              placeholder="Respuesta en 24h"></textarea>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label for="cta_primary" class="block text-sm font-medium text-zinc-300 mb-2">Texto botón principal</label>
              <input id="cta_primary" type="text" bind:value={cta_primary_text}
                class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-400 transition-colors"
                placeholder="Enviar Correo" />
            </div>
            <div>
              <label for="cta_secondary" class="block text-sm font-medium text-zinc-300 mb-2">Texto botón secundario</label>
              <input id="cta_secondary" type="text" bind:value={cta_secondary_text}
                class="w-full px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-400 transition-colors"
                placeholder="LinkedIn" />
            </div>
          </div>
        </div>

        <!-- Estado -->
        <div class="space-y-4">
          <h2 class="text-xl font-semibold text-amber-400 mb-4">Estado</h2>

          <div class="flex items-center gap-3">
            <input
              type="checkbox"
              bind:checked={is_active}
              id="is_active"
              class="w-4 h-4 text-amber-500 bg-zinc-800 border-zinc-600 rounded
                     focus:ring-amber-400 focus:ring-2"
            />
            <label for="is_active" class="text-sm font-medium text-zinc-300">
              Configuración activa
            </label>
          </div>
          <p class="text-xs text-zinc-500">
            Solo las configuraciones activas se mostrarán en el sitio público.
          </p>
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
