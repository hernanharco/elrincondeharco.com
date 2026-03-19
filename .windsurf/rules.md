# 📋 Reglas de Orquestación del Proyecto

## 🎯 Propósito
Este archivo sirve como orquestador central para guiar las interacciones con el proyecto, asegurando que se consulten las referencias correctas y se mantenga la coherencia entre frontend y backend.

## 📁 Estructura del Proyecto

### Frontend
- **Ubicación**: `/frontend/`
- **Documentación**: `.windsurf/frontend.md`
- **Tecnologías**: Svelte, TypeScript, TailwindCSS
- **Estado**: Componentes principales, estructura base

### Backend  
- **Ubicación**: `/backend/`
- **Documentación**: `.windsurf/backend.md`
- **Tecnologías**: FastAPI, PostgreSQL (Neon), psycopg 3
- **Estado**: API funcional, configuración segura lista

## 🔍 Reglas de Consulta

### 1. Consultas Específicas de Backend
- **Siempre consultar**: `.windsurf/backend.md` primero
- **Contexto**: Estructura de carpetas, endpoints, configuración
- **Archivos relevantes**: `backend/app/`, `backend/pyproject.toml`, `backend/package.json`

### 2. Consultas Específicas de Frontend
- **Siempre consultar**: `.windsurf/frontend.md` primero  
- **Contexto**: Componentes Svelte, estilos, configuración
- **Archivos relevantes**: `frontend/src/`, `frontend/tailwind.config.js`

### 3. Consultas Integradas (Frontend + Backend)
- **Consultar ambos**: `.windsurf/backend.md` y `.windsurf/frontend.md`
- **Contexto**: Conexión API, tipos compartidos, flujo de datos
- **Puntos de integración**:
  - API endpoints (`/api/v1/*`)
  - Tipos TypeScript vs Pydantic schemas
  - Autenticación y manejo de errores
  - Variables de entorno compartidas

## 🔄 Flujo de Trabajo

### Desarrollo Backend
1. Revisar `.windsurf/backend.md` para estructura actual
2. Modificar archivos en `/backend/app/`
3. Actualizar documentación si hay cambios estructurales
4. Considerar impacto en frontend si se modifican endpoints

### Desarrollo Frontend  
1. Revisar `.windsurf/frontend.md` para componentes existentes
2. Modificar archivos en `/frontend/src/`
3. Actualizar documentación si se agregan componentes
4. Verificar compatibilidad con endpoints del backend

### Desarrollo Integrado
1. **Primero**: Consultar ambos archivos de documentación
2. **Después**: Identificar puntos de conexión necesarios
3. **Luego**: Implementar cambios coordinados
4. **Finalmente**: Actualizar ambas documentaciones

## 📋 Checklist Antes de Modificar

### Para Backend
- [ ] He leído `.windsurf/backend.md`
- [ ] Conozco la estructura actual de endpoints
- [ ] Verifico impacto en frontend
- [ ] Actualizo la documentación si es necesario

### Para Frontend
- [ ] He leído `.windsurf/frontend.md`
- [ ] Conozco los componentes existentes
- [ ] Verifico compatibilidad con backend
- [ ] Actualizo la documentación si es necesario

### Para Integración
- [ ] He leído ambas documentaciones
- [ ] Identifiqué los puntos de conexión
- [ ] Verifico tipos y formatos de datos
- [ ] Actualizo ambas documentaciones

## 🎯 Preguntas Guía

### Sobre Backend
- "¿Cuál es la estructura actual de la API?"
- "¿Qué endpoints están disponibles?"
- "¿Cómo está configurada la conexión a la base de datos?"
- "¿Qué modelos y schemas existen?"

### Sobre Frontend
- "¿Qué componentes Svelte están disponibles?"
- "¿Cómo está configurado TailwindCSS?"
- "¿Qué estructura de carpetas sigue el frontend?"
- "¿Qué tipos TypeScript están definidos?"

### Sobre Integración
- "¿Cómo se conecta el frontend con la API?"
- "¿Qué endpoints consume el frontend?"
- "¿Cómo se manejan los errores entre frontend y backend?"
- "¿Qué tipos de datos se comparten?"

## 🚨 Reglas Importantes

1. **NUNCA modificar sin consultar primero la documentación relevante**
2. **SIEMPRE actualizar la documentación después de cambios estructurales**
3. **VERIFICAR compatibilidad entre frontend y backend**
4. **MANTENER coherencia en nombres y formatos**
5. **DOCUMENTAR nuevos endpoints y componentes**

## 📞 Comandos Rápidos

### Backend
```bash
cd backend
pnpm dev          # Iniciar servidor de desarrollo
pnpm test         # Ejecutar tests
pnpm lint         # Formatear y lintear código
```

### Frontend
```bash
cd frontend  
npm run dev       # Iniciar servidor de desarrollo
npm run build     # Construir para producción
npm run test      # Ejecutar tests
```

---

**Nota**: Este archivo debe ser la primera referencia ante cualquier duda sobre la estructura o estado del proyecto.
