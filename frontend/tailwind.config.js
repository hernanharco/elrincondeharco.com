/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,sss,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Aquí defines "background" para que Tailwind genere "bg-background"
        background: 'var(--background)', 
        foreground: 'var(--foreground)',
        border: 'var(--border)',
        ring: 'var(--ring)',
        // Colores brand del portfolio
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
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};