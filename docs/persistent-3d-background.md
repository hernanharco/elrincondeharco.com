# 🎬 Persistent 3D Background (Fixed Canvas)

> Efecto visual donde el fondo 3D se queda `position: fixed` y **nunca se mueve** mientras scrolleás. El contenido pasa por encima como si el 3D fuera un escenario de fondo.

---

## ✨ Cómo se ve

- Al entrar: formas geométricas flotando en **caos** (rojo/naranja)
- A los 2.5s o al hacer scroll: **transición** a orden (ámbar/cyan) con líneas de conexión
- Después de la transición: las formas flotan suavemente, partículas brillan, cámara se mueve leve
- **TODO eso se queda de fondo mientras navegás la página**

---

## 🧠 Cómo funciona

```
position: fixed   → pegado a la ventana, NO scrollea
inset: 0          → ocupa toda la pantalla
z-index: 0        → atrás de todo
pointer-events: none → no interfiere con clicks
```

El contenido tiene `z-index: 10` y pasa por encima. Simple pero efectivo.

---

## 🏷️ Nombres que se usan

| Término | Qué significa |
|---------|--------------|
| **Fixed Canvas** | Canvas pegado a la ventana |
| **Persistent 3D** | El 3D persiste mientras scrolleás |
| **Ambient 3D Background** | Fondo 3D ambiental que te acompaña |
| **Sticky Canvas** | Canvas que no se mueve al scrollear |
| **Hero Persistent** | El fondo del Hero se mantiene en toda la página |

---

## ⚙️ Cómo se controla

- Se activa **solo en la página de inicio** (checkea `window.location.pathname`)
- En **móvil no se activa** (rendimiento)
- Se puede ajustar: velocidad de transición, colores, cantidad de formas, etc.

---

## 🔗 Para buscar inspiración

Buscá en Google o en sitios como Awwwards:

- "three.js fixed canvas background"
- "persistent 3D background website"
- "ambient 3D scene scroll"
- "sticky canvas three.js"

---

## 📁 Archivo donde está

```
frontend/src/components/effects/CaosOrden.astro
```
