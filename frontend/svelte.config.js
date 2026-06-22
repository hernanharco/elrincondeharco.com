import { vitePreprocess } from '@astrojs/svelte';

export default {
	preprocess: vitePreprocess(),
	compilerOptions: {
		// true = Svelte 5 runes ($state, $derived, $effect, $props)
		// Los componentes legacy tienen <svelte:options runes={false} />
		runes: true
	}
}
