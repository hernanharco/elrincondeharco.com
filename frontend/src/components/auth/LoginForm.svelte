<script lang="ts">
  import { authService, type LoginRequest } from '../../services/authService';

  // Props (Svelte 4 syntax — runes disabled en este proyecto)
  export let redirectParam: string = '/admin';

  // Estado local (Svelte 4: let normal, reactivo por asignación)
  let form: LoginRequest = {
    username: '',
    password: ''
  };

  let isLoading = false;
  let error: string | null = null;

  function handleNavigation() {
    const fromQuery = new URLSearchParams(window.location.search).get('redirect');
    const destination = fromQuery || redirectParam;
    window.location.href = destination;
  }

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();

    isLoading = true;
    error = null;

    try {
      await authService.login(form);
      // La cookie httpOnly la setea el backend — no hay que guardar nada en localStorage
      handleNavigation();
    } catch (err) {
      error = err instanceof Error ? err.message : 'Credenciales inválidas';
    } finally {
      isLoading = false;
    }
  }

  function clearMessages() {
    if (error) error = null;
  }
</script>

<div class="w-full max-w-md mx-auto">
  <!-- Google Login -->
  <a
    href="http://localhost:8000/api/v1/auth/google?redirect_to=http://localhost:4322/api/auth/callback"
    class="w-full py-2.5 px-4 bg-white hover:bg-gray-100 text-zinc-800 font-medium
           rounded-lg transition-all active:scale-[0.98] border border-zinc-300
           flex justify-center items-center gap-3 mb-6"
  >
    <svg class="w-5 h-5" viewBox="0 0 24 24">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/>
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
    </svg>
    Ingresar con Google
  </a>

  <!-- Separador -->
  <div class="relative mb-6">
    <div class="absolute inset-0 flex items-center">
      <div class="w-full border-t border-zinc-700"></div>
    </div>
    <div class="relative flex justify-center text-sm">
      <span class="px-3 bg-zinc-900 text-zinc-400">o con credenciales</span>
    </div>
  </div>

  <form onsubmit={handleSubmit} class="space-y-6">
    <!-- Usuario -->
    <div>
      <label for="username" class="block text-sm font-medium text-zinc-300 mb-1.5">
        Usuario
      </label>
      <input
        id="username"
        type="text"
        bind:value={form.username}
        oninput={clearMessages}
        class="w-full px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100
               focus:ring-2 focus:ring-amber-500 focus:border-transparent outline-none
               transition-all placeholder:text-zinc-500"
        placeholder="Tu usuario de authCore..."
        required
        disabled={isLoading}
      />
    </div>

    <!-- Contraseña -->
    <div>
      <label for="password" class="block text-sm font-medium text-zinc-300 mb-1.5">
        Contraseña
      </label>
      <input
        id="password"
        type="password"
        bind:value={form.password}
        oninput={clearMessages}
        class="w-full px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100
               focus:ring-2 focus:ring-amber-500 focus:border-transparent outline-none
               transition-all placeholder:text-zinc-500"
        placeholder="••••••••"
        required
        disabled={isLoading}
      />
    </div>

    <!-- Error -->
    {#if error}
      <div class="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
        {error}
      </div>
    {/if}

    <!-- Botón login con credenciales -->
    <button
      type="submit"
      disabled={isLoading || !form.username || !form.password}
      class="w-full py-2.5 px-4 bg-amber-500 hover:bg-amber-600 text-zinc-900 font-semibold
             rounded-lg transition-all active:scale-[0.98]
             disabled:opacity-50 disabled:cursor-not-allowed
             flex justify-center items-center gap-2"
    >
      {#if isLoading}
        <svg class="animate-spin h-5 w-5 text-zinc-900" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        Ingresando...
      {:else}
        Ingresar
      {/if}
    </button>
  </form>
</div>
