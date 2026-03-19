Convierte estos componentes React (.tsx) a componentes Svelte (.svelte) compatibles con Astro + Tailwind v3.

REGLAS ESTRICTAS:
- Mantén **EXACTAMENTE** las mismas clases Tailwind y estructura HTML/JSX (no cambies ni una clase, ni orden, ni anidamiento).
- Conserva TypeScript completo (types, interfaces, generics).
- Convierte props React → export let en Svelte.
- Eventos: on:click, on:submit, bind:value, etc.
- Estado: usa $state, $derived, $effect si es necesario (Svelte 5 runes si el proyecto las usa).
- No agregues <style> ni imports de CSS dentro del .svelte → los estilos son globales vía Tailwind v3.
- Si el componente es interactivo o tiene hidración, sugiere client:load o client:visible al final (pero no lo incluyas en el código .svelte).
- Devuelve SOLO el código completo de cada .svelte, separados por --- y con nombre de archivo como comentario arriba.
- No explicaciones, no markdown.

Archivos a convertir:
@Navbar.tsx
@About.tsx
@Hero.tsx
@Stack.tsx
@Projects.tsx
@Passions.tsx
@Footer.tsx
