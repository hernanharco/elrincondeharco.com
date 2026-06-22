<script lang="ts">
  import Icon from '@iconify/svelte';

  let {
    currentImage = null,
    label = 'Subir imagen',
    accept = 'image/*',
    maxSizeMB = 10,
    onChange,
  }: {
    currentImage?: string | null;
    label?: string;
    accept?: string;
    maxSizeMB?: number;
    onChange?: (detail: { file: File | null; preview: string | null }) => void;
  } = $props();

  let file: File | null = $state(null);
  let preview: string | null = $state(currentImage);
  let isDragging = $state(false);
  let isUploading = $state(false);
  let error = $state('');

  function handleFileSelect(selectedFile: File) {
    error = '';

    // Validar tamaño
    const maxSize = maxSizeMB * 1024 * 1024;
    if (selectedFile.size > maxSize) {
      error = `El archivo no debe superar ${maxSizeMB}MB`;
      return;
    }

    // Validar tipo
    if (!selectedFile.type.startsWith('image/')) {
      error = 'El archivo debe ser una imagen';
      return;
    }

    file = selectedFile;

    // Crear preview
    const reader = new FileReader();
    reader.onload = (e) => {
      preview = e.target?.result as string;
    };
    reader.readAsDataURL(selectedFile);

    onChange?.({ file: selectedFile, preview });
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    isDragging = false;

    const droppedFile = e.dataTransfer?.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  }

  function handleDragOver(e: DragEvent) {
    e.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  function handleInputChange(e: Event) {
    const input = e.target as HTMLInputElement;
    const selectedFile = input.files?.[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  }

  function removeImage() {
    file = null;
    preview = null;
    error = '';
    onChange?.({ file: null, preview: null });
  }

  function openFileDialog() {
    const input = document.getElementById('file-input') as HTMLInputElement;
    input?.click();
  }
</script>

<div class="space-y-4">
  <label class="block text-sm font-medium text-zinc-300 mb-2" for="file-input">{label}</label>

  <!-- Upload Area -->
  <div
    role="button"
    tabindex="0"
    class="relative group"
    ondrop={handleDrop}
    ondragover={handleDragOver}
    ondragleave={handleDragLeave}
    onkeydown={(e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openFileDialog();
      }
    }}
  >
    {#if preview}
      <!-- Image Preview -->
      <div class="relative rounded-xl overflow-hidden bg-zinc-900 border border-zinc-800">
        <img src={preview} alt="Preview" class="w-full h-64 object-cover" />

        <!-- Overlay with actions -->
        <div
          class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center gap-4"
        >
          <button
            type="button"
            onclick={openFileDialog}
            class="p-3 bg-amber-500/90 text-white rounded-full hover:bg-amber-500 transition-colors shadow-lg"
          >
            <Icon icon="lucide:upload" width={20} height={20} />
          </button>
          <button
            type="button"
            onclick={removeImage}
            class="p-3 bg-red-500/90 text-white rounded-full hover:bg-red-500 transition-colors shadow-lg"
          >
            <Icon icon="lucide:x" width={20} height={20} />
          </button>
        </div>

        <!-- Success indicator -->
        <div class="absolute top-4 right-4 p-2 bg-emerald-500/90 text-white rounded-full">
          <Icon icon="lucide:check" width={16} height={16} />
        </div>
      </div>
    {:else}
      <!-- Drop Zone -->
      <div
        role="button"
        tabindex="0"
        onkeydown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            openFileDialog();
          }
        }}
        class={`
          relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer 
          ${
            isDragging
              ? 'border-amber-400 bg-amber-400/10 scale-[1.02]'
              : 'border-zinc-700 hover:border-amber-400/50 hover:bg-zinc-800/50'
          }
        `}
        onclick={openFileDialog}
      >
        <input id="file-input" type="file" {accept} onchange={handleInputChange} class="hidden" />

        <div class="space-y-4">
          <div
            class="mx-auto w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center text-white shadow-lg"
          >
            {#if isUploading}
              <div
                class="animate-spin w-8 h-8 border-2 border-white border-t-transparent rounded-full"
              ></div>
            {:else}
              <Icon icon="lucide:image" width={32} height={32} />
            {/if}
          </div>

          <div class="space-y-2">
            <p class="text-white font-medium">
              {isDragging
                ? 'Suelta la imagen aquí'
                : 'Arrastra una imagen o haz clic para seleccionar'}
            </p>
            <p class="text-zinc-500 text-sm">
              PNG, JPG, GIF hasta {maxSizeMB}MB
            </p>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <!-- Error Message -->
  {#if error}
    <div
      class="flex items-center gap-2 p-3 bg-red-900/20 border border-red-500/30 rounded-lg text-red-400 text-sm"
    >
      <Icon icon="lucide:x" width={16} height={16} />
      <span>{error}</span>
    </div>
  {/if}

  <!-- Current Image Info -->
  {#if currentImage && !preview}
    <div class="flex items-center gap-3 p-3 bg-zinc-800/50 border border-zinc-700 rounded-lg">
      <Icon icon="lucide:image" width={16} height={16} class="text-zinc-400" />
      <span class="text-zinc-400 text-sm">Imagen actual guardada</span>
    </div>
  {/if}
</div>
