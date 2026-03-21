# 📁 Frontend - Portfolio Hernan Arango Cortes

## 🏗️ **Stack Tecnológico**
- **Framework**: Astro v6.0.8
- **UI Library**: Svelte 5.54.0 (runes desactivados por compatibilidad)
- **Styling**: Tailwind CSS v3.4.17 + PostCSS
- **TypeScript**: v5.9.3
- **Icons**: Lucide Svelte v0.577.0
- **Package Manager**: pnpm

## 📂 **Estructura de Archivos**

```
frontend/
├── src/
│   ├── components/          # Componentes organizados por tipo
│   │   ├── layout/           # Componentes estructurales
│   │   │   ├── Navbar.svelte    # Navegación con menú móvil
│   │   │   ├── Footer.svelte    # Pie de página dinámico
│   │   │   └── AdminSidebar.svelte # Sidebar admin
│   │   ├── sections/         # Secciones públicas
│   │   │   ├── Hero.svelte      # Sección principal con CTA
│   │   │   ├── About.svelte     # Sección sobre mí
│   │   │   ├── Stack.svelte     # Tecnologías con filtros
│   │   │   ├── Projects.svelte  # Galería de proyectos
│   │   │   └── Passions.svelte  # Sección pasiones
│   │   ├── ui/               # Componentes reutilizables
│   │   │   └── ImageUpload.svelte # Upload mejorado
│   │   └── admin/           # Panel de administración
│   │       ├── DashboardCards.svelte    # Cards dashboard
│   │       ├── HeroEditor.svelte       # Editor Hero
│   │       ├── AboutEditor.svelte      # Editor About
│   │       ├── StackEditor.svelte      # Editor Stack
│   │       ├── ProjectsEditor.svelte   # Editor Projects
│   │       ├── PassionsEditor.svelte   # Editor Passions
│   │       └── FooterEditor.svelte     # Editor Footer
│   ├── layouts/
│   │   ├── Layout.astro       # Layout principal con fuentes
│   │   └── AdminLayout.astro   # Layout panel admin
│   ├── pages/
│   │   ├── index.astro       # Página principal
│   │   └── admin/            # Rutas admin
│   │       ├── index.astro   # Dashboard admin
│   │       ├── hero.astro    # Admin Hero
│   │       ├── about.astro   # Admin About
│   │       ├── stack.astro   # Admin Stack
│   │       ├── projects.astro # Admin Projects
│   │       ├── passions.astro # Admin Passions
│   │       └── footer.astro  # Admin Footer
│   ├── lib/
│   │   ├── config.ts         # fetchApi utility + PUBLIC_API_URL
│   │   ├── types.ts          # TypeScript interfaces
│   │   └── dataEvents.ts     # Sistema de sincronización eventos
│   └── styles/
│       └── global.css         # Estilos globales + variables CSS
├── public/                    # Assets estáticos
├── astro.config.mjs           # Configuración Astro
├── tailwind.config.js         # Configuración Tailwind
├── postcss.config.cjs         # Configuración PostCSS
├── tsconfig.json             # Configuración TypeScript
├── svelte.config.js          # Configuración Svelte (runes: false)
└── package.json              # Dependencias
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
- ✅ **Navbar**: Menú móvil responsive con navegación suave
- ✅ **Stack**: Filtrado por categorías (Frontend/Backend/DevOps/Herramientas)
- ✅ **Projects**: Galería con hover effects y tags
- ✅ **Footer**: Pie de página dinámico con datos del backend
- ✅ **Smooth Scrolling**: Navegación entre secciones
- ✅ **Panel Admin**: Sistema completo de gestión
- ✅ **ImageUpload**: Drag & drop con preview y validación
- ✅ **Sincronización**: Actualización en tiempo real
- ✅ **PDF Download**: Descarga automática de CV con nombres limpios

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
<Footer client:load />

<!-- Componentes visuales -->
<Hero client:visible />
<About client:visible />
<Projects client:visible />
<Passions client:visible />
```

### **Panel Admin**
```astro
<!-- Layout admin con estilos Tailwind -->
<AdminLayout title="Dashboard" currentPath={currentPath}>
  <HeroEditor client:load />
</AdminLayout>
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
- ✅ **Svelte 4 syntax** (runes desactivados por lucide-svelte)

### **Panel Admin Completo**
- ✅ **6 editores** para todas las secciones
- ✅ **Upload de imágenes y PDFs** con drag & drop
- ✅ **Sincronización automática** con componentes públicos
- ✅ **Formularios validados** con feedback visual
- ✅ **Sidebar responsive** con navegación intuitiva
- ✅ **Accesibilidad** mejorada con labels asociados

### **Características Preservadas**
- 🎨 **Gradientes** amber/orange
- 🖼️ **Imágenes** Unsplash optimizadas
- 📱 **Responsive** mobile-first
- ⚡ **Animaciones** y transiciones suaves
- 🔗 **Anclas** smooth scrolling
- 🎯 **Interactividad** completa
- 🔄 **Sincronización** en tiempo real

## 🔧 **Estado Actual**

- **Servidor**: ✅ Funcionando sin errores
- **Componentes**: ✅ Todos compilados con Svelte 4 syntax
- **Estilos**: ✅ Tailwind aplicado correctamente
- **Build**: ✅ Listo para producción
- **Performance**: ✅ Optimizado con Astro
- **Backend API**: ✅ Disponible con datos poblados
- **Endpoints**: ✅ 7 dominios listos para consumo
- **Panel Admin**: ✅ 100% funcional con sincronización
- **ImageUpload**: ✅ Componente reutilizable mejorado
- **Data Events**: ✅ Sistema de sincronización implementado
- **Footer Component**: ✅ Dinámico con backend integration
- **PDF Support**: ✅ Upload y descarga automática
- **Lucide Compatibility**: ✅ Funcional con Svelte 4 syntax
- **Component Organization**: ✅ Estructura optimizada por tipo

## 📈 **Próximos Pasos**

1. **Deploy**: Subir a Vercel/Netlify
2. **SEO**: Meta tags optimizados
3. **Analytics**: Google Analytics integrado
4. **Forms**: Backend para contacto ✅ *COMPLETADO*
5. **Blog**: Sección de artículos técnicos
6. **Integración API**: Conectar componentes con backend ✅ *DISPONIBLE*
7. **Panel Admin**: Sistema completo de gestión ✅ *COMPLETADO*
8. **Sincronización**: Actualización en tiempo real ✅ *COMPLETADO*

---

## 🔗 **Integración con Backend API**

### **Endpoints Disponibles**
| Componente | Endpoint | Método | Response | Características |
|-------------|------------|----------|-----------|---------------|
| Hero.svelte | `GET /api/v1/heroes/latest/` | fetch onMount | HeroResponse | CV download automático |
| About.svelte | `GET /api/v1/abouts/latest/` | fetch onMount | AboutResponse | - |
| Passions.svelte | `GET /api/v1/passions/latest/` | fetch onMount | PassionResponse | - |
| Projects.svelte | `GET /api/v1/projects/` | fetch onMount | ProjectResponse[] | - |
| Stack.svelte | `GET /api/v1/stacks/` | fetch onMount | StackResponse[] | - |
| Footer.svelte | `GET /api/v1/footers/latest/` | fetch onMount | FooterResponse | Datos dinámicos |

### **Ejemplo de Integración**
```javascript
// En componente Svelte con sincronización automática
import { onMount } from 'svelte';
import { listenForDataChange } from '$lib/dataEvents';

let heroData = null;

async function loadData() {
  const response = await fetch(`${import.meta.env.PUBLIC_API_URL}/api/v1/heroes/latest/`);
  heroData = await response.json();
}

onMount(async () => {
  await loadData();
  
  // Escuchar cambios desde el admin
  const cleanup = listenForDataChange('hero', async () => {
    await loadData();
  });
  
  return cleanup;
});
```

### **Datos Poblados**
- ✅ **7 dominios** con datos reales del frontend
- ✅ **31+ registros** totales en la base de datos
- ✅ **Endpoints funcionando** en `http://localhost:8000/docs`
- ✅ **PDF uploads** con descarga automática
- ✅ **Footer dinámico** con quick_links JSONB

## 📡 API del backend — cómo consumirla
- Base URL: `import.meta.env.PUBLIC_API_URL` (ej: http://localhost:8000)
- Secciones únicas (hero, about): usar `GET /api/v1/{dominio}s/latest/`
- Secciones múltiples (stack, projects): usar `GET /api/v1/{dominio}s/`
- Todas las actualizaciones son `multipart/form-data`, nunca JSON puro
- La imagen siempre llega como `File` separado, el resto como campos `Form`

---

## 🎯 **Panel Admin - Características Avanzadas**

### **ImageUpload.svelte**
- ✅ **Drag & Drop**: Arrastrar y soltar archivos
- ✅ **Preview Inmediato**: Vista previa de imágenes
- ✅ **Validaciones**: Tamaño máximo y tipo de archivo
- ✅ **Estados Visuales**: Loading, success, error con animaciones
- ✅ **Reutilizable**: Componente genérico para todos los editores
- ✅ **Svelte 4 Syntax**: Compatible con lucide-svelte
- ✅ **Event Handling**: `on:event` syntax para consistencia

### **Sistema de Sincronización**
- ✅ **Eventos Personalizados**: `dispatchDataChange()` y `listenForDataChange()`
- ✅ **Actualización en Tiempo Real**: Cambios del admin se reflejan instantáneamente
- ✅ **Limpieza Automática**: Sin memory leaks en componentes
- ✅ **Tipo Seguro**: TypeScript interfaces para todos los eventos

### **Editores Admin**
- ✅ **HeroEditor**: Título, subtítulo, descripción, botones, imagen, CV PDF
- ✅ **AboutEditor**: Info personal, experiencia, liderazgo, imagen
- ✅ **StackEditor**: Tecnologías con categorías, iconos, estilos
- ✅ **ProjectsEditor**: Galería con tags, URLs, imágenes
- ✅ **PassionsEditor**: Secciones familiares, juegos, coding
- ✅ **FooterEditor**: Contacto, redes sociales, enlaces rápidos
- ✅ **Accessibility**: Labels asociados con inputs (A11y)

---

**Status**: 🟢 **PRODUCCIÓN LISTA**  
**Última Actualización**: Marzo 2026  
**Versión**: 2.2.0 (con Panel Admin, Sincronización, PDF Upload y Component Organization)
