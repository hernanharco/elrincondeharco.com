<script lang="ts">
  import { Github, Linkedin, Mail, Twitter } from 'lucide-svelte';
</script>

<footer id="contact" class="bg-black text-white border-t border-white/10 pt-16 pb-8">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
      <div class="col-span-1 lg:col-span-2">
        <h2
          class="text-2xl font-bold mb-4 bg-gradient-to-r from-amber-400 to-yellow-600 bg-clip-text text-transparent"
        >
          Hernan Arango Cortes
        </h2>
        <p class="text-gray-400 max-w-sm">
          Programador Full Stack enfocado en velocidad y rendimiento. Creando el futuro de la web
          desde Asturias para el mundo.
        </p>
      </div>

      <div>
        <h3 class="text-lg font-semibold mb-4 text-white">Enlaces Rápidos</h3>
        <ul class="space-y-2 text-gray-400">
          <li><a href="#inicio" class="hover:text-amber-400 transition-colors">Inicio</a></li>
          <li><a href="#sobre-mi" class="hover:text-amber-400 transition-colors">Sobre Mí</a></li>
          <li>
            <a href="#stack" class="hover:text-amber-400 transition-colors">Stack Tecnológico</a>
          </li>
          <li><a href="#pasiones" class="hover:text-amber-400 transition-colors">Pasiones</a></li>
        </ul>
      </div>

      <div>
        <h3 class="text-lg font-semibold mb-4 text-white">Contacto</h3>
        <ul class="space-y-2 text-gray-400">
          <li>Avilés, Asturias, España</li>
          <li>hernan.arango@example.com</li>
          <li class="flex gap-4 mt-4">
            <a href="https://github.com" class="hover:text-amber-400 transition-colors"
              ><Github size={20} /></a
            >
            <a href="https://linkedin.com" class="hover:text-amber-400 transition-colors"
              ><Linkedin size={20} /></a
            >
            <a href="https://twitter.com" class="hover:text-amber-400 transition-colors"
              ><Twitter size={20} /></a
            >
            <a
              href="mailto:hernan.arango@example.com"
              class="hover:text-amber-400 transition-colors"><Mail size={20} /></a
            >
          </li>
        </ul>
      </div>
    </div>

    <div class="border-t border-white/10 pt-8 text-center text-gray-500 text-sm">
      <p>{new Date().getFullYear()} Hernan Arango Cortes. Todos los derechos reservados.</p>
    </div>
  </div>
</footer>
