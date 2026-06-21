import { vitePreprocess } from '@astrojs/svelte';

export default {
	preprocess: vitePreprocess(),
	compilerOptions: {
		// false = Svelte 4 syntax (export let, let, $:, <slot />)
		// @iconify/svelte v4 usa esta sintaxis
		runes: false
	}
}
