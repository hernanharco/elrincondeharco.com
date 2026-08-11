<svelte:options runes={false} />

<script lang="ts">
  /**
   * HtmlEditor.svelte — Editor visual para HTML simple
   *
   * Props:
   *   value: string  — el HTML a editar
   *   label: string  — label del campo
   *   placeholder: string — placeholder del textarea
   *
   * Bindings:
   *   bind:value — two-way binding con el HTML
   *
   * Toolbar:
   *   - Botones para wrap en span con colores
   *   - Botón para insertar <br />
   *   - Toggle preview / editor
   */
  import Icon from '@iconify/svelte';

  export let value: string = '';
  export let label: string = 'Contenido HTML';
  export let placeholder: string = 'Escribí el contenido aquí...';

  let textareaEl: HTMLTextAreaElement;
  let showPreview = false;

  // ── Insertar span alrededor de selección ──────────────────────
  function wrapSelection(openTag: string, closeTag: string) {
    const ta = textareaEl;
    if (!ta) return;

    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const selectedText = value.substring(start, end);
    const before = value.substring(0, start);
    const after = value.substring(end);

    // Si hay selección, la envuelve; si no, inserta el span vacío
    if (selectedText) {
      value = `${before}${openTag}${selectedText}${closeTag}${after}`;
    } else {
      value = `${before}${openTag}texto${closeTag}${after}`;
    }

    // Poner el foco de vuelta y seleccionar el texto insertado
    requestAnimationFrame(() => {
      ta.focus();
      if (selectedText) {
        ta.setSelectionRange(start + openTag.length, start + openTag.length + selectedText.length);
      } else {
        ta.setSelectionRange(start + openTag.length, start + openTag.length + 5);
      }
    });
  }

  function wrapAmber() {
    wrapSelection('<span class="text-amber-400">', '</span>');
  }

  function wrapCyan() {
    wrapSelection('<span class="text-cyan-400">', '</span>');
  }

  // ── Insertar <br /> ───────────────────────────────────────
  function insertBreak() {
    const ta = textareaEl;
    if (!ta) return;

    const pos = ta.selectionStart;
    const before = value.substring(0, pos);
    const after = value.substring(ta.selectionEnd);
    value = `${before}<br />${after}`;

    requestAnimationFrame(() => {
      ta.focus();
      ta.selectionStart = ta.selectionEnd = pos + 6;
    });
  }

  // ── Limpiar formato (quitar spans) ─────────────────────────
  function stripFormatting() {
    value = value
      .replace(/<span[^>]*>/gi, '')
      .replace(/<\/span>/gi, '');
  }
</script>

<div class="html-editor">
  <label class="block text-sm font-medium text-zinc-400 mb-2">{label}</label>

  <!-- Toolbar -->
  <div class="flex items-center gap-1.5 mb-2 flex-wrap">
    <button
      onclick={wrapAmber}
      title="Envolver en color ámbar (text-amber-400)"
      class="px-2.5 py-1.5 rounded-md bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 text-xs font-mono
             border border-amber-500/20 hover:border-amber-500/40 transition-all active:scale-95"
    >
      <span class="font-bold">A</span><span class="opacity-60">mbar</span>
    </button>

    <button
      onclick={wrapCyan}
      title="Envolver en color cian (text-cyan-400)"
      class="px-2.5 py-1.5 rounded-md bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 text-xs font-mono
             border border-cyan-500/20 hover:border-cyan-500/40 transition-all active:scale-95"
    >
      <span class="font-bold">C</span><span class="opacity-60">ian</span>
    </button>

    <div class="w-px h-6 bg-zinc-700 mx-1"></div>

    <button
      onclick={insertBreak}
      title="Insertar salto de línea (&lt;br /&gt;)"
      class="px-2.5 py-1.5 rounded-md bg-zinc-700/50 hover:bg-zinc-600/50 text-zinc-300 text-xs font-mono
             border border-zinc-700 hover:border-zinc-600 transition-all active:scale-95"
    >
      &lt;br /&gt;
    </button>

    <div class="w-px h-6 bg-zinc-700 mx-1"></div>

    <button
      onclick={stripFormatting}
      title="Quitar todos los spans/contenedores"
      class="px-2.5 py-1.5 rounded-md bg-red-500/5 hover:bg-red-500/10 text-red-400/70 hover:text-red-400 text-xs
             border border-red-500/10 hover:border-red-500/30 transition-all active:scale-95"
    >
      Limpiar
    </button>

    <div class="flex-1"></div>

    <!-- Toggle preview -->
    <button
      onclick={() => { showPreview = !showPreview; }}
      class="px-2.5 py-1.5 rounded-md text-xs font-medium transition-all active:scale-95
             {showPreview
               ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
               : 'bg-zinc-700/30 text-zinc-500 hover:text-zinc-300 border border-zinc-700/50'}"
    >
      {#if showPreview}
        <Icon icon="lucide:pencil" class="w-3.5 h-3.5" />
        Editar
      {:else}
        <Icon icon="lucide:eye" class="w-3.5 h-3.5" />
        Vista previa
      {/if}
    </button>
  </div>

  <!-- Editor / Preview -->
  {#if showPreview}
    <div class="min-h-[100px] p-4 rounded-xl bg-zinc-900/80 border border-zinc-700/50
                text-white text-center flex items-center justify-center">
      <div class="text-5xl sm:text-6xl md:text-7xl font-bold tracking-tight leading-[1.1]">
        {@html value || '<span class="text-zinc-600">— vista previa vacía —</span>'}
      </div>
    </div>
  {:else}
    <textarea
      bind:this={textareaEl}
      bind:value={value}
      rows={3}
      class="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100
             font-mono text-sm leading-relaxed
             focus:border-amber-400 focus:ring-1 focus:ring-amber-400 transition-all outline-none resize-y"
      placeholder={placeholder}
    ></textarea>
  {/if}

  <!-- Mini helper -->
  <div class="flex items-center gap-2 mt-1.5">
    <span class="text-[10px] text-zinc-600">
      Seleccioná texto y tocalo con <span class="text-amber-500/80">Ambar</span> o
      <span class="text-cyan-500/80">Cian</span> para colorearlo
    </span>
  </div>
</div>
