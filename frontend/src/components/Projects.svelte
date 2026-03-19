<script lang="ts">
  import { ExternalLink, Github, Layers, Lock, Calendar } from 'lucide-svelte';

  const projects = [
    {
      title: 'Tapicería Moderna',
      description:
        'Plataforma de gestión para taller de tapicería. Permite seguimiento de pedidos, inventario y catálogo digital.',
      image:
        'https://images.unsplash.com/photo-1762803841043-bee9f5691411?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBmdXJuaXR1cmUlMjB1cGhvbHN0ZXJ5JTIwd29ya3Nob3B8ZW58MXx8fHwxNzcwNDgzNjg3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      tags: ['Vite', 'Neon', 'Django', 'Tailwind'],
      iconName: 'Layers',
      color: 'from-amber-500/20 to-orange-600/20',
    },
    {
      title: 'Sistema de Autenticación',
      description:
        'Módulo de seguridad robusto con JWT, OAuth2 y recuperación de contraseñas. Diseñado para integración escalable.',
      image:
        'https://images.unsplash.com/photo-1614064642261-3ccbfafa481b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjeWJlcnNlY3VyaXR5JTIwbG9jayUyMGF1dGhlbnRpY2F0aW9uJTIwY29kZXxlbnwxfHx8fDE3NzA0ODM2ODd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      tags: ['FastAPI', 'JWT', 'PostgreSQL', 'Security'],
      iconName: 'Lock',
      color: 'from-blue-500/20 to-cyan-600/20',
    },
    {
      title: 'Gestor de Citas',
      description:
        'Aplicación para reserva y administración de citas. Incluye recordatorios automatizados y calendario interactivo.',
      image:
        'https://images.unsplash.com/photo-1617131633412-39437b40a16b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjYWxlbmRhciUyMHNjaGVkdWxlJTIwYXBwb2ludG1lbnQlMjBkaWdpdGFsfGVufDF8fHx8MTc3MDQ4MzY4OHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
      tags: ['React', 'Node.js', 'MongoDB', 'Calendar API'],
      iconName: 'Calendar',
      color: 'from-green-500/20 to-teal-600/20',
    },
  ];

  function getIcon(iconName: string, size: number = 20) {
    const iconMap: Record<string, any> = {
      Layers,
      Lock,
      Calendar,
      ExternalLink,
      Github,
    };
    return iconMap[iconName];
  }
</script>

<section id="proyectos" class="py-24 bg-zinc-900 text-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-16">
      <h2 class="text-3xl md:text-5xl font-bold mb-4">
        Proyectos <span class="text-amber-400">Destacados</span>
      </h2>
      <p class="text-gray-400 max-w-2xl mx-auto text-lg">
        Soluciones reales que demuestran la capacidad de entrega y calidad técnica.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {#each projects as project, index}
        <div
          class="group bg-black border border-white/10 rounded-2xl overflow-hidden hover:border-amber-500/30 transition-all duration-500 hover:shadow-[0_0_30px_-5px_rgba(251,191,36,0.15)] flex flex-col h-full"
        >
          <!-- Image Container -->
          <div class="relative h-48 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-tr {project.color} opacity-60 z-10"></div>
            <img
              src={project.image}
              alt={project.title}
              class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700"
            />
            <div
              class="absolute top-4 right-4 z-20 bg-black/50 backdrop-blur-md p-2 rounded-lg border border-white/10 text-white"
            >
              <svelte:component this={getIcon(project.iconName)} size={20} />
            </div>
          </div>

          <!-- Content -->
          <div class="p-6 flex-1 flex flex-col">
            <h3
              class="text-xl font-bold text-white mb-2 group-hover:text-amber-400 transition-colors"
            >
              {project.title}
            </h3>
            <p class="text-gray-400 mb-6 text-sm leading-relaxed flex-1">
              {project.description}
            </p>

            <!-- Tags -->
            <div class="flex flex-wrap gap-2 mb-6">
              {#each project.tags as tag}
                <span
                  class="px-3 py-1 text-xs font-medium rounded-full bg-white/5 border border-white/10 text-gray-300"
                >
                  {tag}
                </span>
              {/each}
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-4 pt-4 border-t border-white/5 mt-auto">
              <button
                class="flex items-center gap-2 text-sm font-medium text-white hover:text-amber-400 transition-colors"
              >
                <ExternalLink size={16} /> Ver Demo
              </button>
              <button
                class="flex items-center gap-2 text-sm font-medium text-gray-400 hover:text-white transition-colors"
              >
                <Github size={16} /> Código
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>
