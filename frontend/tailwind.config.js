/** @type {import('tailwindcss').Config} */
export default {
  // 1. Rastreo de archivos (incluyendo .sss por tu configuración previa)
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,sss,svelte,ts,tsx,vue}'],

  // 2. Safelist: Aquí protegemos las clases que vienen de la Base de Datos
  safelist: [
    // Colores de texto (ej: text-orange-500)
    {
      pattern: /^text-(orange|blue|cyan|yellow|teal|green|indigo|pink|red|purple|gray|rose|white)-(300|400|500|600)$/,
    },
    // Bordes con opacidad (ej: group-hover:border-orange-500/50)
    // Nota: El patrón NO lleva el prefijo 'group-hover:', se define en 'variants'
    {
      pattern: /^border-(orange|blue|cyan|yellow|teal|green|indigo|pink|red|purple|gray|rose|white)-(300|400|500|600)\/50$/,
      variants: ['group-hover'],
    },
  ],

  theme: {
    extend: {
      colors: {
        // Variables CSS para compatibilidad con temas o Shadcn (opcional)
        background: 'var(--background)', 
        foreground: 'var(--foreground)',
        border: 'var(--border)',
        ring: 'var(--ring)',

        // Tus colores brand personalizados
        amber: {
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
        },
        orange: {
          400: '#fb923c',
          500: '#f97316',
          600: '#ea580c',
        },
        zinc: {
          900: '#18181b',
          950: '#09090b',
        }
      },
      fontFamily: {
        // Fuente principal del proyecto
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },

  plugins: [
    // Aquí podrías añadir plugins como @tailwindcss/typography si los necesitas
  ],
};