<script lang="ts">
  import {
    Zap,
    Rocket,
    Database,
    Server,
    Atom,
    LayoutTemplate,
    GitBranch,
    Github,
    Triangle,
    Cloud,
    Send,
    BrainCircuit,
    Gauge,
    Layers,
    Monitor,
    HardDrive,
    Settings,
    Container,
    Code2,
    FileCode2,
    Palette,
    Hash,
    Lock,
    Globe,
    Terminal,
  } from 'lucide-svelte';

  let activeCategory = 'Todos';

  const categories = ['Todos', 'Frontend', 'Backend', 'DevOps', 'Herramientas'];

  const technologies = [
    // Frontend
    {
      name: 'HTML5',
      category: 'Frontend',
      icon: 'Globe',
      description: 'Estructura Web',
      color: 'text-orange-500',
      border: 'group-hover:border-orange-500/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]',
    },
    {
      name: 'CSS3',
      category: 'Frontend',
      icon: 'Palette',
      description: 'Estilos Modernos',
      color: 'text-blue-500',
      border: 'group-hover:border-blue-500/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]',
    },
    {
      name: 'Tailwind CSS',
      category: 'Frontend',
      icon: 'Palette',
      description: 'Estilos Utilitarios',
      color: 'text-cyan-400',
      border: 'group-hover:border-cyan-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]',
    },
    {
      name: 'JavaScript',
      category: 'Frontend',
      icon: 'FileCode2',
      description: 'Interactividad',
      color: 'text-yellow-400',
      border: 'group-hover:border-yellow-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]',
    },
    {
      name: 'TypeScript',
      category: 'Frontend',
      icon: 'FileCode2',
      description: 'JS Tipado',
      color: 'text-blue-400',
      border: 'group-hover:border-blue-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]',
    },
    {
      name: 'React',
      category: 'Frontend',
      icon: 'Atom',
      description: 'Interfaces interactivas',
      color: 'text-cyan-400',
      border: 'group-hover:border-cyan-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]',
    },
    {
      name: 'Astro',
      category: 'Frontend',
      icon: 'Rocket',
      description: 'Webs ultra rápidas',
      color: 'text-orange-400',
      border: 'group-hover:border-orange-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(251,146,60,0.3)]',
    },
    {
      name: 'Next.js',
      category: 'Frontend',
      icon: 'LayoutTemplate',
      description: 'Framework de producción',
      color: 'text-white',
      border: 'group-hover:border-white/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]',
    },

    // Backend
    {
      name: 'Python',
      category: 'Backend',
      icon: 'Terminal',
      description: 'Lenguaje Versátil',
      color: 'text-yellow-300',
      border: 'group-hover:border-yellow-300/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(253,224,71,0.3)]',
    },
    {
      name: 'FastAPI',
      category: 'Backend',
      icon: 'Zap',
      description: 'APIs rápidas con Python',
      color: 'text-teal-400',
      border: 'group-hover:border-teal-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(45,212,191,0.3)]',
    },
    {
      name: 'Django',
      category: 'Backend',
      icon: 'Layers',
      description: 'Framework Web Robusto',
      color: 'text-green-600',
      border: 'group-hover:border-green-600/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(22,163,74,0.3)]',
    },
    {
      name: 'API REST',
      category: 'Backend',
      icon: 'Server',
      description: 'Arquitectura de APIs',
      color: 'text-indigo-400',
      border: 'group-hover:border-indigo-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(129,140,248,0.3)]',
    },
    {
      name: 'JWT',
      category: 'Backend',
      icon: 'Lock',
      description: 'Seguridad & Auth',
      color: 'text-pink-500',
      border: 'group-hover:border-pink-500/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(236,72,153,0.3)]',
    },
    {
      name: 'MongoDB',
      category: 'Backend',
      icon: 'Database',
      description: 'NoSQL escalable',
      color: 'text-green-400',
      border: 'group-hover:border-green-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(74,222,128,0.3)]',
    },
    {
      name: 'NEON',
      category: 'Backend',
      icon: 'Server',
      description: 'Postgres Serverless',
      color: 'text-blue-400',
      border: 'group-hover:border-blue-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]',
    },

    // DevOps
    {
      name: 'Docker',
      category: 'DevOps',
      icon: 'Container',
      description: 'Contenedorización',
      color: 'text-blue-500',
      border: 'group-hover:border-blue-500/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]',
    },
    {
      name: 'Git',
      category: 'DevOps',
      icon: 'GitBranch',
      description: 'Control de versiones',
      color: 'text-red-500',
      border: 'group-hover:border-red-500/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(239,68,68,0.3)]',
    },
    {
      name: 'GitHub',
      category: 'DevOps',
      icon: 'Github',
      description: 'Colaboración',
      color: 'text-white',
      border: 'group-hover:border-white/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]',
    },
    {
      name: 'Vercel',
      category: 'DevOps',
      icon: 'Triangle',
      description: 'Deploy Frontend',
      color: 'text-gray-200',
      border: 'group-hover:border-gray-200/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(229,231,235,0.2)]',
    },
    {
      name: 'Render',
      category: 'DevOps',
      icon: 'Cloud',
      description: 'Cloud Hosting',
      color: 'text-purple-400',
      border: 'group-hover:border-purple-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(192,132,252,0.3)]',
    },

    // Herramientas
    {
      name: 'VS Code',
      category: 'Herramientas',
      icon: 'Code2',
      description: 'Editor de Código',
      color: 'text-blue-500',
      border: 'group-hover:border-blue-500/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]',
    },
    {
      name: 'Postman',
      category: 'Herramientas',
      icon: 'Send',
      description: 'Testing de APIs',
      color: 'text-orange-500',
      border: 'group-hover:border-orange-500/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]',
    },
    {
      name: 'IA & LLMs',
      category: 'Herramientas',
      icon: 'BrainCircuit',
      description: 'Inteligencia Artificial',
      color: 'text-rose-400',
      border: 'group-hover:border-rose-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(251,113,133,0.3)]',
    },
    {
      name: 'Optimización',
      category: 'Herramientas',
      icon: 'Gauge',
      description: 'Performance Web',
      color: 'text-yellow-400',
      border: 'group-hover:border-yellow-400/50',
      glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]',
    },
  ];

  $: filteredTech =
    activeCategory === 'Todos'
      ? technologies
      : technologies.filter((t) => t.category === activeCategory);

  function getCategoryIcon(cat: string) {
    switch (cat) {
      case 'Frontend':
        return Monitor;
      case 'Backend':
        return HardDrive;
      case 'DevOps':
        return Layers;
      case 'Herramientas':
        return Settings;
      default:
        return Layers;
    }
  }

  function getIcon(iconName: string, size: number = 24) {
    const iconMap: Record<string, any> = {
      Globe,
      Palette,
      FileCode2,
      Atom,
      Rocket,
      LayoutTemplate,
      Terminal,
      Zap,
      Layers,
      Server,
      Lock,
      Database,
      Container,
      GitBranch,
      Github,
      Triangle,
      Cloud,
      Code2,
      Send,
      BrainCircuit,
      Gauge,
      Monitor,
      HardDrive,
      Settings,
    };
    return iconMap[iconName];
  }

  function setCategory(cat: string) {
    activeCategory = cat;
  }
</script>

<section id="stack" class="py-24 bg-zinc-950 text-white relative">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
      <div class="space-y-2">
        <h2 class="text-3xl md:text-5xl font-bold">
          Arsenal <span class="text-amber-400">Técnico</span>
        </h2>
        <p class="text-gray-400 max-w-lg text-lg">
          Herramientas modernas para soluciones rápidas y escalables.
        </p>
      </div>

      <!-- Category Filter -->
      <div class="flex flex-wrap gap-2">
        {#each categories as cat}
          <button
            on:click={() => setCategory(cat)}
            class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 flex items-center gap-2 border {activeCategory ===
            cat
              ? 'bg-amber-400 text-black border-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.4)]'
              : 'bg-white/5 text-gray-400 border-white/10 hover:border-white/30 hover:text-white'}"
          >
            {#if cat !== 'Todos'}
              <svelte:component this={getCategoryIcon(cat)} size={16} />
            {/if}
            {cat}
          </button>
        {/each}
      </div>
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
      {#each filteredTech as tech (tech.name)}
        <div
          class="group relative p-4 h-32 flex flex-col justify-between bg-zinc-900/50 rounded-xl border border-white/5 transition-all duration-300 hover:-translate-y-1 {tech.border} {tech.glow}"
        >
          <div class="flex justify-between items-start">
            <div class="p-2 rounded-lg bg-white/5 {tech.color}">
              <svelte:component this={getIcon(tech.icon)} size={24} />
            </div>
            <span class="text-[10px] uppercase tracking-wider text-gray-500 font-semibold">
              {tech.category}
            </span>
          </div>
          <div>
            <h3 class="font-bold text-white tracking-wide">{tech.name}</h3>
            <p class="text-xs text-gray-400 mt-1 line-clamp-1">{tech.description}</p>
          </div>
        </div>
      {/each}
    </div>

    <div class="mt-12 text-center">
      <p class="text-zinc-500 text-sm">Optimizado para rendimiento y experiencia de usuario.</p>
    </div>
  </div>
</section>
