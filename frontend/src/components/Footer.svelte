<script lang="ts">
  import { onMount } from 'svelte';
  import { Github, Linkedin, Mail, Twitter, MapPin } from 'lucide-svelte';
  import { fetchApi } from '$lib/config';
  import type { FooterResponse, SiteSettingsResponse } from '$lib/types';
  import { listenForDataChange } from '$lib/dataEvents';

  let footerData: FooterResponse | null = null;
  let siteSettings: SiteSettingsResponse | null = null;
  let loading = true;

  async function loadAllData() {
    try {
      // Cargamos ambos en paralelo para mayor velocidad
      const [fResponse, sResponse] = await Promise.all([
        fetchApi<FooterResponse>('/api/v1/footers/latest/'),
        fetchApi<SiteSettingsResponse>('/api/v1/site-settings/latest/')
      ]);
      footerData = fResponse;
      siteSettings = sResponse;
    } catch (error) {
      console.error("Error cargando el footer:", error);
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    await loadAllData();

    // Suscripción a cambios en ambos dominios
    const cleanupFooter = listenForDataChange('footer', loadAllData);
    const cleanupSettings = listenForDataChange('site-settings', loadAllData);

    return () => {
      cleanupFooter();
      cleanupSettings();
    };
  });

  // Valores por defecto inteligentes si la DB está vacía
  $: brandName = siteSettings?.brand_name || 'elRincondelHarco.com';
  // $: legalName = siteSettings?.legal_name || 'Hernan Arango Cortes';
  $: contactEmail = siteSettings?.contact_email || footerData?.email || 'hernan.harco@gmail.com';
  $: currentYear = new Date().getFullYear();
</script>

<footer id="contact" class="bg-black text-white border-t border-white/10 pt-16 pb-8 transition-opacity duration-500 {loading ? 'opacity-50' : 'opacity-100'}">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
      
      <div class="col-span-1 lg:col-span-2">
        <h2 class="text-2xl font-bold mb-4 bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
          {brandName}
        </h2>
        <p class="text-gray-400 max-w-sm leading-relaxed">
          {siteSettings?.slogan || footerData?.description || 'Desarrollando soluciones modulares con FastAPI y Astro.'}
        </p>
      </div>

      <div>
        <h3 class="text-lg font-semibold mb-6 text-white/90 border-b border-amber-400/30 w-fit">Navegación</h3>
        <ul class="space-y-3 text-gray-400">
          {#each footerData?.quick_links || [
            { text: 'Inicio', href: '#home' }, 
            { text: 'Proyectos', href: '#projects' }, 
            { text: 'Stack', href: '#stack' }
          ] as link}
            <li>
              <a href={link.href} class="hover:text-amber-400 hover:translate-x-1 inline-block transition-all underline-offset-4 hover:underline">
                {link.text}
              </a>
            </li>
          {/each}
        </ul>
      </div>

      <div>
        <h3 class="text-lg font-semibold mb-6 text-white/90 border-b border-amber-400/30 w-fit">Contacto</h3>
        <ul class="space-y-4 text-gray-400">
          <li class="flex items-center gap-3">
            <MapPin size={18} class="text-amber-400" />
            <span>{footerData?.location || 'Avilés, Asturias'}</span>
          </li>
          <li class="flex items-center gap-3">
            <Mail size={18} class="text-amber-400" />
            <a href="mailto:{contactEmail}" class="hover:text-amber-400 transition-colors truncate">
              {contactEmail}
            </a>
          </li>
          
          <li class="flex gap-5 mt-6">
            {#if siteSettings?.social_networks?.github}
              <a href={siteSettings.social_networks.github.toString()} target="_blank" rel="noopener" class="hover:text-amber-400 transition-transform hover:scale-110" aria-label="GitHub">
                <Github size={22} />
              </a>
            {/if}
            {#if siteSettings?.social_networks?.linkedin}
              <a href={siteSettings.social_networks.linkedin.toString()} target="_blank" rel="noopener" class="hover:text-amber-400 transition-transform hover:scale-110" aria-label="LinkedIn">
                <Linkedin size={22} />
              </a>
            {/if}
            {#if siteSettings?.social_networks?.twitter}
              <a href={siteSettings.social_networks.twitter.toString()} target="_blank" rel="noopener" class="hover:text-amber-400 transition-transform hover:scale-110" aria-label="Twitter">
                <Twitter size={22} />
              </a>
            {/if}
          </li>
        </ul>
      </div>
    </div>

    <div class="border-t border-white/5 pt-8 text-center text-gray-500 text-xs tracking-wider">
      <p>
        © {currentYear} <strong>{brandName}</strong>. 
        {siteSettings?.copyright_notice || 'Casi todos los derechos reservados.'}
      </p>
    </div>
  </div>
</footer>