<svelte:options runes={false} />

<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchApi } from '$lib/config';
  import type { ExperienceSectionResponse, SectorResponse, ProjectResponse } from '$lib/types';
  import { fallbackExperienceSection } from '$lib/fallback-data';
  import { dispatchDataChange } from '$lib/dataEvents';
  import Icon from '@iconify/svelte';
  import HtmlEditor from '../ui/HtmlEditor.svelte';

  const API = import.meta.env.PUBLIC_API_URL;

  let data: ExperienceSectionResponse | null = null;
  let sectors: SectorResponse[] = [];
  let projects: ProjectResponse[] = [];
  let loading = true;
  let saving = false;
  let message = '';
  let messageType: 'success' | 'error' = 'success';

  // Form fields
  let tagline = '';
  let title = '';
  let description = '';

  // Total projects across all sectors
  let totalAssigned = 0;
  let totalWithImages = 0;

  function loadSectors() {
    fetchApi<SectorResponse[]>('/api/v1/sectors/')
      .then((res) => { sectors = res; })
      .catch(() => { sectors = []; });
  }

  function loadProjects() {
    fetchApi<ProjectResponse[]>('/api/v1/projects/')
      .then((res) => {
        projects = res;
        totalWithImages = res.filter((p) => p.image_url).length;
      })
      .catch(() => { projects = []; });
  }

  function populateFields(src: ExperienceSectionResponse) {
    data = src;
    tagline = src.tagline ?? '';
    title = src.title ?? '';
    description = src.description ?? '';
  }

  onMount(async () => {
    await Promise.all([
      fetchApi<ExperienceSectionResponse>('/api/v1/experience/latest/')
        .then((res) => {
          if (res) populateFields(res);
          else populateFields(fallbackExperienceSection);
        })
        .catch(() => populateFields(fallbackExperienceSection)),
      fetchApi<SectorResponse[]>('/api/v1/sectors/')
        .then((res) => { sectors = res; })
        .catch(() => { sectors = []; }),
      fetchApi<ProjectResponse[]>('/api/v1/projects/')
        .then((res) => {
          projects = res;
          totalWithImages = res.filter((p) => p.image_url).length;
        })
        .catch(() => { projects = []; }),
    ]);

    totalAssigned = sectors.reduce((acc, s) => acc + (s.project_ids?.length || 0), 0);
    loading = false;
  });

  async function handleSave() {
    if (!data) return;
    saving = true;
    message = '';

    try {
      const formData = new FormData();
      formData.append('tagline', tagline);
      formData.append('title', title);
      formData.append('description', description);

      const res = await fetch(`${API}/api/v1/experience/${data.id}`, {
        method: 'PUT',
        body: formData,
      });

      if (!res.ok) throw new Error('Error en la respuesta del servidor');

      const updatedData = await res.json();
      data = updatedData;
      message = '¡Sección Experiencia actualizada con éxito!';
      messageType = 'success';

      dispatchDataChange('experience', 'update', updatedData);
    } catch (err) {
      message = 'No se pudo guardar la información';
      messageType = 'error';
    } finally {
      saving = false;
    }
  }
</script>

<div class="p-6 md:p-10">
  <div class="max-w-5xl mx-auto">
    {#if loading}
      <div class="flex items-center justify-center p-12 text-zinc-400 gap-3">
        <Icon icon="lucide:loader-2" class="animate-spin w-5 h-5 text-amber-500" />
        <span class="text-sm font-medium">Cargando sección...</span>
      </div>
    {:else}
      <!-- Mensaje -->
      {#if message}
        <div
          class="mb-6 p-4 rounded-xl text-sm font-medium flex items-center gap-2
            {messageType === 'success'
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
              : 'bg-red-500/10 text-red-400 border border-red-500/20'}"
        >
          <Icon
            icon={messageType === 'success' ? 'lucide:check-circle' : 'lucide:alert-circle'}
            class="w-4 h-4 shrink-0"
          />
          {message}
        </div>
      {/if}

      <!-- ═══ HEADER ═══ -->
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
            <Icon icon="lucide:briefcase" class="w-5 h-5 text-zinc-900" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-zinc-100">Experiencia</h1>
            <p class="text-sm text-zinc-500">La sección más importante — acá los clientes ven los trabajos realizados</p>
          </div>
        </div>
      </div>

      <!-- ═══ STATS PANEL ═══ -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <div class="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800">
          <div class="text-2xl font-bold text-amber-400">{sectors.length}</div>
          <div class="text-xs text-zinc-500 mt-1 uppercase tracking-wider">Rubros</div>
        </div>
        <div class="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800">
          <div class="text-2xl font-bold text-cyan-400">{projects.length}</div>
          <div class="text-xs text-zinc-500 mt-1 uppercase tracking-wider">Proyectos</div>
        </div>
        <div class="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800">
          <div class="text-2xl font-bold text-emerald-400">{totalAssigned}</div>
          <div class="text-xs text-zinc-500 mt-1 uppercase tracking-wider">Asignaciones</div>
        </div>
        <div class="p-4 rounded-xl bg-zinc-900/50 border border-zinc-800">
          <div class="text-2xl font-bold text-purple-400">{totalWithImages}/{projects.length}</div>
          <div class="text-xs text-zinc-500 mt-1 uppercase tracking-wider">Con imagen</div>
        </div>
      </div>

      <!-- ═══ HEADER EDITOR ═══ -->
      <div class="rounded-2xl bg-zinc-900/30 border border-zinc-800 overflow-hidden mb-8">
        <div class="px-6 py-4 border-b border-zinc-800 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <Icon icon="lucide:heading" class="w-4 h-4 text-amber-400" />
            <h2 class="text-sm font-bold text-zinc-200 uppercase tracking-wider">Encabezado de la sección</h2>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-[10px] text-zinc-600">Se ve arriba de los rubros</span>
          </div>
        </div>

        <div class="p-6 space-y-5">
          <!-- Tagline -->
          <div>
            <label for="tagline" class="block text-xs font-medium text-zinc-400 mb-1.5"
              >Tagline (frase superior)</label
            >
            <input
              id="tagline"
              type="text"
              bind:value={tagline}
              class="w-full px-4 py-2.5 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 text-sm
                     focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none"
              placeholder="Experiencia"
            />
          </div>

          <!-- Title with HtmlEditor -->
          <HtmlEditor
            bind:value={title}
            label="Título principal"
            placeholder="Seleccioná tu rubro..."
          />

          <!-- Description -->
          <div>
            <label for="description" class="block text-xs font-medium text-zinc-400 mb-1.5"
              >Descripción</label
            >
            <textarea
              id="description"
              bind:value={description}
              rows={2}
              class="w-full px-4 py-2.5 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 text-sm
                     focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none resize-none"
              placeholder="Descripción debajo del título..."
            ></textarea>
          </div>
        </div>
      </div>

      <!-- ═══ VISTA PREVIA ═══ -->
      <div class="rounded-2xl bg-zinc-900/30 border border-zinc-800 overflow-hidden mb-8">
        <div class="px-6 py-4 border-b border-zinc-800 flex items-center gap-2">
          <Icon icon="lucide:eye" class="w-4 h-4 text-zinc-500" />
          <h2 class="text-sm font-bold text-zinc-200 uppercase tracking-wider">Vista previa</h2>
        </div>
        <div class="p-6 flex items-center justify-center min-h-[160px] bg-zinc-950/50">
          <div class="text-center max-w-2xl">
            <p class="text-amber-400 text-xs font-medium tracking-[0.25em] uppercase mb-3">
              {tagline || 'tagline'}
            </p>
            <h2 class="text-3xl md:text-5xl font-bold mb-4 text-white">
              {@html title || 'título'}
            </h2>
            <p class="text-gray-500 max-w-2xl mx-auto text-lg">
              {description || 'descripción'}
            </p>
          </div>
        </div>
      </div>

      <!-- ═══ RUBROS Y PROYECTOS ═══ -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <!-- Sectores card -->
        <a
          href="/admin/sectors"
          class="group block p-6 rounded-2xl bg-zinc-900/30 border border-zinc-800 hover:border-amber-500/30 transition-all duration-300"
        >
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center">
              <Icon icon="lucide:layout-list" class="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <h3 class="font-bold text-zinc-100 group-hover:text-amber-400 transition-colors">Rubros</h3>
              <p class="text-xs text-zinc-500">{sectors.length} rubros creados</p>
            </div>
            <Icon icon="lucide:chevron-right" class="w-4 h-4 text-zinc-600 group-hover:text-amber-400 ml-auto transition-colors" />
          </div>

          {#if sectors.length === 0}
            <p class="text-xs text-zinc-600 italic">No hay rubros todavía</p>
          {:else}
            <div class="flex flex-wrap gap-2">
              {#each sectors.slice(0, 6) as s}
                <span class="px-2.5 py-1 rounded-lg text-[10px] font-medium bg-white/5 border border-white/10 text-zinc-400">
                  {s.name}
                </span>
              {/each}
              {#if sectors.length > 6}
                <span class="px-2.5 py-1 rounded-lg text-[10px] font-medium bg-amber-500/10 text-amber-400/70">
                  +{sectors.length - 6}
                </span>
              {/if}
            </div>
          {/if}
        </a>

        <!-- Proyectos card -->
        <a
          href="/admin/projects"
          class="group block p-6 rounded-2xl bg-zinc-900/30 border border-zinc-800 hover:border-cyan-500/30 transition-all duration-300"
        >
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
              <Icon icon="lucide:folder-kanban" class="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <h3 class="font-bold text-zinc-100 group-hover:text-cyan-400 transition-colors">Proyectos</h3>
              <p class="text-xs text-zinc-500">{projects.length} proyectos creados</p>
            </div>
            <Icon icon="lucide:chevron-right" class="w-4 h-4 text-zinc-600 group-hover:text-cyan-400 ml-auto transition-colors" />
          </div>

          {#if projects.length === 0}
            <p class="text-xs text-zinc-600 italic">No hay proyectos todavía</p>
          {:else}
            <div class="flex flex-wrap gap-2">
              {#each projects.slice(0, 5) as p}
                <span class="px-2.5 py-1 rounded-lg text-[10px] font-medium bg-white/5 border border-white/10 text-zinc-400">
                  {p.title}
                </span>
              {/each}
              {#if projects.length > 5}
                <span class="px-2.5 py-1 rounded-lg text-[10px] font-medium bg-cyan-500/10 text-cyan-400/70">
                  +{projects.length - 5}
                </span>
              {/if}
            </div>
          {/if}
        </a>
      </div>

      <!-- ═══ BOTÓN GUARDAR ═══ -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-zinc-800">
        <p class="text-xs text-zinc-600">
          <Icon icon="lucide:info" class="w-3 h-3 inline-block mr-1" />
          Los cambios en el encabezado se ven al recargar la página principal
        </p>
        <button
          onclick={handleSave}
          disabled={saving}
          class="w-full sm:w-auto px-10 py-4 rounded-xl font-black text-zinc-900
             bg-gradient-to-r from-amber-400 to-orange-500
             hover:from-amber-300 hover:to-orange-400
             disabled:opacity-50 disabled:cursor-not-allowed
             transition-all duration-300 flex items-center justify-center gap-2 shadow-xl shadow-amber-600/10"
        >
          {#if saving}
            <Icon icon="lucide:loader-2" class="animate-spin w-5 h-5" />
            Guardando...
          {:else}
            <Icon icon="lucide:save" class="w-5 h-5" />
            Guardar Cambios
          {/if}
        </button>
      </div>
    {/if}
  </div>
</div>
