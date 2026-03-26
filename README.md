# Portfolio elRincondeHarco.com

## 📋 Descripción

Portfolio personal profesional desarrollado con **Astro + Svelte 5** en el frontend y **FastAPI + PostgreSQL** en el backend.

## 🚀 Stack Tecnológico

### Frontend
- **Astro 6.0** - Framework de sitios estáticos
- **Svelte 5** - Componentes reactivos con Runes
- **TypeScript** - Tipado estático
- **TailwindCSS** - Framework de CSS
- **Lucide Icons** - Sistema de iconos

### Backend
- **FastAPI** - Framework API Python
- **PostgreSQL** - Base de datos
- **SQLAlchemy** - ORM Python
- **Alembic** - Migraciones de BD
- **Pydantic** - Validación de datos
- **Poetry** - Gestión de dependencias

### DevOps
- **Docker** - Contenerización
- **Docker Compose** - Orquestación
- **GitHub Actions** - CI/CD
- **Nginx** - Servidor web

## 📁 Estructura del Proyecto

```
Portfolioelrincondeharco.com/
├── frontend/                 # Aplicación Astro + Svelte
│   ├── src/
│   │   ├── components/      # Componentes Svelte
│   │   ├── lib/            # Utilidades y tipos
│   │   └── pages/          # Páginas Astro
│   ├── tests/              # Tests frontend
│   └── scripts/            # Scripts de automatización
├── backend/                  # Aplicación FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints API
│   │   ├── core/           # Configuración
│   │   ├── db/             # Base de datos
│   │   └── models/         # Modelos SQLAlchemy
│   ├── tests/              # Tests backend
│   ├── scripts/            # Scripts de setup
│   └── alembic/            # Migraciones
├── .windsurf/               # Documentación del proyecto
├── docker-compose.yml       # Servicios Docker
└── README.md               # Este archivo
```

## 🛠️ Instalación y Setup

### Prerrequisitos
- Node.js 22+
- Python 3.12+
- Docker y Docker Compose
- pnpm y Poetry

### Backend Setup
```bash
cd backend
./scripts/poetry-setup.sh
```

### Frontend Setup
```bash
cd frontend
pnpm install
```

### Docker Setup
```bash
cd backend
./scripts/setup.sh dev
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
./scripts/run-tests.sh coverage
```

### Frontend Tests
```bash
cd frontend
./scripts/run-tests.sh coverage
```

## 🚀 Desarrollo

### Iniciar Desarrollo Local
```bash
# Terminal 1: Backend
cd backend && poetry run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && pnpm run dev
```

### URLs de Desarrollo
- Frontend: http://localhost:4321
- Backend API: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📦 Despliegue

### Producción con Docker
```bash
cd backend
./scripts/setup.sh prod
```

### Variables de Entorno
Copiar y configurar:
- `backend/.env` - Configuración backend
- `frontend/.env` - Configuración frontend

## 📚 Documentación

- **[Backend](.windsurf/backend.md)** - Arquitectura y configuración
- **[Frontend](.windsurf/frontend.md)** - Componentes y estilos
- **[Docker](.windsurf/docker.md)** - Contenedores y despliegue
- **[Tests Backend](.windsurf/test-backend.md)** - Estrategia de tests backend
- **[Tests Frontend](.windsurf/test-frontend.md)** - Estrategia de tests frontend
- **[Rules](.windsurf/rules.md)** - Orquestación del proyecto

## 🎯 Características

### ✅ Implementadas
- Portfolio responsive y moderno
- Sistema de administración de contenido
- Integración con Cloudinary para imágenes
- Tests completos (80%+ coverage)
- Dockerizado para producción
- CI/CD automatizado

### 🔄 En Desarrollo
- Sistema de blog
- Portfolio multilingüe
- Optimización SEO avanzada

## 🤝 Contribución

1. Fork del proyecto
2. Feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT - ver [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Hernán Harco** - [GitHub](https://github.com/hernanharco)

## 📞 Contacto

- Email: hernan@elrincondeharco.com
- Web: [elRincondeHarco.com](https://elrincondeharco.com)

---

⚡ **Desarrollado con ❤️ y ☕**
