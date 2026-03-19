# 📁 Frontend - Portfolio Hernan Arango Cortes

## 🏗️ **Stack Tecnológico**
- **Framework**: Astro v6.0.6
- **UI Library**: Svelte 5.54.0
- **Styling**: Tailwind CSS v3.4.17 + PostCSS
- **TypeScript**: v5.9.3
- **Icons**: Lucide Svelte v0.577.0
- **Package Manager**: pnpm

## 📂 **Estructura de Archivos**

```
frontend/
├── src/
│   ├── components/          # 7 componentes Svelte migrados
│   │   ├── Navbar.svelte    # Navegación con menú móvil
│   │   ├── Hero.svelte      # Sección principal con CTA
│   │   ├── About.svelte     # Sección sobre mí
│   │   ├── Stack.svelte     # Tecnologías con filtros interactivos
│   │   ├── Projects.svelte  # Galería de proyectos
│   │   ├── Passions.svelte  # Sección pasiones
│   │   └── Footer.svelte    # Pie de página con contacto
│   ├── layouts/
│   │   └── Layout.astro     # Layout principal con fuentes
│   ├── pages/
│   │   └── index.astro     # Página principal
│   └── styles/
│       └── global.css       # Estilos globales + variables CSS
├── public/                  # Assets estáticos
├── astro.config.mjs         # Configuración Astro
├── tailwind.config.js       # Configuración Tailwind
├── postcss.config.cjs       # Configuración PostCSS
├── tsconfig.json           # Configuración TypeScript
├── svelte.config.js        # Configuración Svelte
└── package.json             # Dependencias
```

## 🎨 **Características del Diseño**

### **Colores Brand**
- **Amber**: `#fbbf24` (primary)
- **Orange**: `#fb923c` (secondary)
- **Zinc**: `#18181b` (dark backgrounds)

### **Tipografía**
- **Fuente Principal**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800, 900
- **System Fallback**: system-ui, sans-serif

### **Componentes Interactivos**
- ✅ **Navbar**: Menú móvil responsive
- ✅ **Stack**: Filtrado por categorías (Frontend/Backend/DevOps/Herramientas)
- ✅ **Projects**: Galería con hover effects
- ✅ **Smooth Scrolling**: Navegación entre secciones

## ⚡ **Configuración Técnica**

### **Tailwind CSS v3.4.17**
```javascript
// Colores personalizados
colors: {
  border: 'var(--border)',
  ring: 'var(--ring)',
  amber: { 400: '#fbbf24', 500: '#f59e0b', 600: '#d97706' },
  orange: { 400: '#fb923c', 500: '#f97316', 600: '#ea580c' }
}
```

### **Hidratación de Componentes**
```astro
<!-- Componentes interactivos -->
<Navbar client:load />
<Stack client:load />

<!-- Componentes visuales -->
<Hero client:visible />
<About client:visible />
<Projects client:visible />
<Passions client:visible />
<Footer client:visible />
```

## 🚀 **Comandos Disponibles**

```bash
# Desarrollo
pnpm dev          # Servidor en http://localhost:4321/

# Producción
pnpm build        # Build optimizado
pnpm preview      # Preview del build

# Mantenimiento
pnpm add <package>     # Agregar dependencia
pnpm remove <package>  # Remover dependencia
```

## 📊 **Migración Completada**

### **De React/Vite → Astro/Svelte 5**
- ✅ **7 componentes** migrados con 100% fidelidad visual
- ✅ **Mismo HTML** y clases Tailwind
- ✅ **Mismo diseño** y UX
- ✅ **Mejor rendimiento** (Astro SSR + Svelte 5)
- ✅ **SEO optimizado** (renderizado del lado del servidor)

### **Características Preservadas**
- 🎨 **Gradientes** amber/orange
- 🖼️ **Imágenes** Unsplash optimizadas
- 📱 **Responsive** mobile-first
- ⚡ **Animaciones** y transiciones suaves
- 🔗 **Anclas** smooth scrolling
- 🎯 **Interactividad** completa

## 🔧 **Estado Actual**

- **Servidor**: ✅ Funcionando sin errores
- **Componentes**: ✅ Todos compilados
- **Estilos**: ✅ Tailwind aplicado correctamente
- **Build**: ✅ Listo para producción
- **Performance**: ✅ Optimizado con Astro
- **Backend API**: ✅ Disponible con datos poblados
- **Endpoints**: ✅ 6 dominios listos para consumo

## 📈 **Próximos Pasos**

1. **Deploy**: Subir a Vercel/Netlify
2. **SEO**: Meta tags optimizados
3. **Analytics**: Google Analytics integrado
4. **Forms**: Backend para contacto ✅ *COMPLETADO*
5. **Blog**: Sección de artículos técnicos
6. **Integración API**: Conectar componentes con backend ✅ *DISPONIBLE*

---

## 🔗 **Integración con Backend API**

### **Endpoints Disponibles**
| Componente | Endpoint | Método | Response |
|-------------|------------|----------|-----------|
| Hero.svelte | `GET /api/v1/heroes/latest/` | fetch onMount | HeroResponse |
| About.svelte | `GET /api/v1/abouts/latest/` | fetch onMount | AboutResponse |
| Passions.svelte | `GET /api/v1/passions/latest/` | fetch onMount | PassionResponse |
| Projects.svelte | `GET /api/v1/projects/` | fetch onMount | ProjectResponse[] |
| Stack.svelte | `GET /api/v1/stacks/` | fetch onMount | StackResponse[] |
| Footer.svelte | `GET /api/v1/footers/latest/` | fetch onMount | FooterResponse |

### **Ejemplo de Integración**
```javascript
// En componente Svelte
import { onMount } from 'svelte';

let heroData = null;

onMount(async () => {
  const response = await fetch('http://localhost:8000/api/v1/heroes/latest/');
  heroData = await response.json();
});
```

### **Datos Poblados**
- ✅ **6 dominios** con datos reales del frontend
- ✅ **31 registros** totales en la base de datos
- ✅ **Endpoints funcionando** en `http://localhost:8000/docs`

## 📡 API del backend — cómo consumirla
- Base URL: `import.meta.env.PUBLIC_API_URL` (ej: http://localhost:8000)
- Secciones únicas (hero, about): usar `GET /api/v1/{dominio}s/latest/`
- Secciones múltiples (stack, projects): usar `GET /api/v1/{dominio}s/`
- Todas las actualizaciones son `multipart/form-data`, nunca JSON puro
- La imagen siempre llega como `File` separado, el resto como campos `Form`

---

**Status**: 🟢 **PRODUCCIÓN LISTA**  
**Última Actualización**: Marzo 2026  
**Versión**: 1.0.0
