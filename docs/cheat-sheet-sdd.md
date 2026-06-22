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

> **Recordá:** No necesitás memorizarte esto. Cuando quieras consultarlo, decime "acordate del cheat sheet" y yo lo busco en memoria.
