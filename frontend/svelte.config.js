import { vitePreprocess } from '@astrojs/svelte';

export default {
	preprocess: vitePreprocess(),
	compilerOptions: {
		runes: false // Disable global runes mode until lucide-svelte is compatible
	}
}
