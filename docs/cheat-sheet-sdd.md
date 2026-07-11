# 🗂️ Cheat Sheet SDD — Cómo pedir las cosas

> No son comandos, es conversación natural. Vos decís el QUÉ, el agente maneja el CÓMO.

---

## 🔧 SETUP DEL PROYECTO (una vez)

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Inicializá SDD" o "Prepará el proyecto" | `sdd-init` — escanea tu stack, configura Engram, deja todo listo |

## 🔍 ENTENDER CÓDIGO

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Analizá el proyecto" | `sdd-explore` — estudio profundo del código |
| "Cómo está estructurado esto?" | Investigación rápida inline |
| "Qué tecnologías usa?" | Te tiro el stack al toque |

## 💡 PROPONER IDEAS

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Tengo una idea..." | Escucha y si es grande activa `sdd-propose` |
| "Quiero hacer X funcionalidad" | Se define alcance juntos |

## 📝 ESPECIFICAR

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Escribamos los requisitos" | `sdd-spec` — requisitos detallados y escenarios |
| "Qué tiene que cumplir esto?" | Lo mismo pero más exploratorio |

## 🏗️ DISEÑAR

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Diseñemos la arquitectura" | `sdd-design` — decisiones técnicas, patrones |
| "Cómo lo implementamos?" | Diseño orientado a implementación |

## 📋 TAREAS

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Partí esto en tareas" | `sdd-tasks` — checklist de implementación |
| "Qué hay que hacer exactamente?" | Desglose de trabajo |

## 💻 CODEAR

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Implementá la tarea 1" | `sdd-apply` — codea los cambios |
| "Hacé tal cosa en el código" | Codeo directo sin SDD |

## ✅ REVISAR

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Juzgá esto" o "hacé judgment day" | **2 jueces paralelos** revisan el código y corrigen |
| "Revisá lo que hicimos" | `sdd-verify` — chequea contra las specs |
| "Está bien esto?" | Revisión rápida directa |

## 🏁 CERRAR

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Cerremos este cambio" | `sdd-archive` — persiste todo y cierra el ciclo |
| "Terminamos por hoy" | Guarda TODO en Engram para la próxima sesión |

## 📌 CONSULTAR MEMORIA

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Acordate de cómo escribir las cosas" | Busca en Engram y te muestra este cuadro |
| "Cómo resolvimos X la vez pasada?" | Busca en Engram y trae el contexto |
| "Acordate de lo que hablamos sobre X" | Lo mismo |

---

## 🚀 El flujo más común

```
1. "Inicializá SDD"                          → Una vez al arrancar el proyecto
2. "Analizá el proyecto"                     → Cuando necesites entender algo
3. [Trabajo normal: pedidos, cambios, etc.]  → El día a día
4. "Juzgá esto"                              → Cuando termines algo importante
5. "Listo, cerramos"                         → Fin de sesión
```

---

---

## 📸 DEPURACIÓN VISUAL CON PLAYWRIGHT

Si hay problemas visuales en móvil o querés ver cómo se ve una página sin usar el navegador:

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Tomá captura de [URL] en móvil" | Playwright abre la URL en modo Android, toma captura de toda la página y la guarda |
| "Inspeccioná [URL]" | Analiza el DOM, busca errores de JS, detecta problemas de hidratación |
| "Compará [URL] con y sin JS" | Toma 2 capturas: una sin JavaScript (solo SSR) y otra con JS, las compara |

**Requiere:** Playwright instalado en el proyecto (`pnpm add -D @playwright/test` + `npx playwright install chromium`).

---

## 👁️ VISIÓN — Analizar imágenes y videos con Gemini

El pipeline de visión permite que modelos text-only (deepseek-v4-flash) "vean" imágenes a través de Gemini.

| Decime esto | Lo que pasa |
|-------------|-------------|
| *Pegar imagen (Ctrl+Shift+V)* | El plugin **Vision Assistant** la describe automáticamente con Gemini |
| "Analizá la última captura" | Busca la última imagen en `~/Imágenes/Capturas de pantalla/` y la analiza |
| "Usá vision_describe con la imagen X" | Tool directo para describir una imagen específica |
| "Usá vision_analyze con la imagen X" | Análisis completo (metadatos + descripción + texto) |
| "Usá analyze_video con URL de YouTube" | Analiza un video de YouTube usando Gemini (sin descargar nada) |

### Herramientas CLI (terminal)

| Comando | Qué hace |
|---------|----------|
| `ultima` | Copia la ruta de la última captura al portapapeles |
| `vi` | Analiza la última captura desde la terminal |
| `Ctrl+Shift+U` (WezTerm) | Keybinding directo para `ultima` |

### Cómo funciona

```
Plugin Vision Assistant (vision-assistant.ts)
  ├── hook "chat.message" → detecta imágenes pegadas → Gemini → texto descriptivo
  ├── tool "vision_describe" → describe cualquier imagen
  ├── tool "vision_analyze" → análisis completo
  └── tool "analyze_video" → analiza videos de YouTube por URL
```

**Requerimiento:** API key de Google en `~/.config/opencode/.env` (`GOOGLE_API_KEY=...`)
**Modelo:** Gemini 2.5 Flash (1,500 requests/día gratis, 1M tokens de contexto)

---

## 🧩 PLUGINS DE OPENCODE

Los plugins reemplazan a los MCP servers en muchos casos. Se cargan automáticamente desde `~/.config/opencode/plugins/`.

| Plugin | Qué hace |
|--------|----------|
| `vision-assistant.ts` | Tools de visión + auto-descripción de imágenes pegadas |
| `engram.ts` | Memoria persistente entre sesiones |
| `background-agents.ts` | Delegación de tareas en segundo plano |

**Ventaja de plugins vs MCP:** Los plugins corren DENTRO del proceso de OpenCode. No necesitan ser spawneados como procesos separados, evitando problemas de pipes/stdio que tienen los MCP servers locales.

---

## 🎯 DISEÑO 3D INMERSIVO — Three.js + GSAP + Lenis

El skill `immersive-3d-web` se activa automáticamente cuando mencionés efectos 3D, Three.js o animaciones inmersivas.

| Decime esto | Lo que pasa |
|-------------|-------------|
| "Quiero un efecto 3D como las páginas japonesas" | Activa el skill con patrones de breakout frame |
| "Hacé que un objeto salga de la pantalla" | Aplica parallax 3D con depth layers |
| "Animá este modelo 3D con el scroll" | GSAP ScrollTrigger + Three.js integration |
| "Poné smooth scrolling" | Agrega Lenis con configuración óptima |
| "Que la hamburguesa/auto se arme parte por parte" | Patrón de assembly animation con stagger |
| "Optimizá esto 3D para mobile" | Cap de pixel ratio, LOD, fog adjustments |
| "Cargá un modelo GLB y que reaccione al scroll" | GLTFLoader + ScrollTrigger onUpdate |
| "Quiero una cámara que viaje por la escena" | Patrón cameraTravel con waypoints |
| "Que las partículas se dispersen con el scroll" | Patrón particleScrollEffect |

### Stack que usa

| Tecnología | Para qué |
|------------|----------|
| **Three.js** | Renderizado 3D en el navegador |
| **GSAP + ScrollTrigger** | Animaciones sincronizadas con scroll |
| **Lenis** | Smooth scrolling a 60fps con física |

### Templates disponibles

| Template | Ruta |
|----------|------|
| 🚀 **Proyecto Vite listo para usar** | `~/.config/opencode/skills/immersive-3d-web/assets/breakout-project/` (corré `npm run dev`) |
| 📄 Standalone HTML | `~/.config/opencode/skills/immersive-3d-web/assets/breakout-frame.html` (necesita server HTTP) |
| 🔧 Setup reutilizable | `~/.config/opencode/skills/immersive-3d-web/assets/smooth-scroll-setup.ts` |
| 🎬 8 patrones de animación | `~/.config/opencode/skills/immersive-3d-web/assets/scroll-3d-animation.ts` |

> **Recordá:** No necesitás memorizarte esto. Cuando quieras consultarlo, decime "acordate del cheat sheet" y yo lo busco en memoria.
