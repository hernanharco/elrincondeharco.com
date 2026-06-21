<script lang="ts">
  /**
   * AuthGuard — Guard client-side para rutas /admin.
   *
   * NOTA: La protección principal la hace el SSR middleware (middleware.ts).
   * AuthGuard es un respaldo client-side que verifica contra el backend.
   * La cookie httpOnly no se puede leer desde JS, así que preguntamos al backend.
   */
  import { onMount } from 'svelte';
  import { authService } from '../../services/authService';

  let checking = true;

  onMount(async () => {
    const user = await authService.isLoggedIn();
    if (!user) {
      const currentPath = window.location.pathname + window.location.search;
      window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`;
    } else {
      checking = false;
    }
  });
</script>

{#if checking}
  <div class="flex items-center justify-center min-h-[50vh]">
    <div class="text-zinc-500 text-sm">Verificando sesión...</div>
  </div>
{:else}
  <slot />
{/if}
