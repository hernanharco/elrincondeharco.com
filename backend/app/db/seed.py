import asyncio
from sqlalchemy import delete
from app.db.session import AsyncSessionLocal
from app.models.hero import Hero
from app.models.about import About
from app.models.passions import Passion
from app.models.projects import Project
from app.models.stack import Stack
from app.models.footer import Footer

async def seed_heroes(db):
    """Borra e inserta datos de heroes"""
    await db.execute(delete(Hero))
    items = [
        Hero(
            title="Desarrollador Full Stack",
            subtitle="Hernan Arango Cortes",
            description="Transformando 14+ años de experiencia en liderazgo y análisis en soluciones tecnológicas innovadoras. Mi familia es mi motor, la tecnología mi pasión, y el emprendimiento mi camino hacia el futuro.",
            background_image=None,
            contact_button_text="Contactar",
            cv_button_text="Descargar CV",
            image_url=None,
        ),
    ]
    db.add_all(items)

async def seed_abouts(db):
    """Borra e inserta datos de abouts"""
    await db.execute(delete(About))
    items = [
        About(
            title="14+ Años de Trayectoria Profesional",
            description="Mi nombre es Hernan Arango Cortes. Hace aproximadamente 5 años que resido en Avilés, Asturias, donde me he especializado en las tecnologías más modernas para ofrecer los mejores servicios a mis futuros clientes. Mi carrera comenzó en Colombia a los 18 años. Durante 14 años trabajé en una empresa donde escalé posiciones hasta formar un equipo competitivo y ágil, al que con orgullo llamé el 'Equipo de Oro'. Nos caracterizábamos por presentar soluciones rápidas y efectivas, una filosofía que mantengo hoy en día utilizando herramientas como FastAPI y Astro.",
            location="Avilés, Asturias, España",
            years_experience="14+ Años",
            team_name="Equipo de Oro",
            leadership_title="Liderazgo",
            leadership_desc="Formación de equipos de alto rendimiento.",
            experience_title="Experiencia",
            experience_desc="Más de una década entregando soluciones.",
            image_url=None,
        ),
    ]
    db.add_all(items)

async def seed_passions(db):
    """Borra e inserta datos de passions"""
    await db.execute(delete(Passion))
    items = [
        Passion(
            title="Más allá del Código",
            description="Mi pasión, aparte de programar y jugar videojuegos, es estar con mi familia.",
            family_title="Mi Familia",
            family_desc="Son mi motor, mi pasión y la razón de querer continuar cada día y cada momento.",
            games_title="Videojuegos",
            games_desc="Un hobby que me permite desconectar y explorar nuevos mundos digitales.",
            coding_title="Programación",
            coding_desc="No es solo mi trabajo, es mi forma de crear y aportar valor al mundo.",
            image_url=None,
        ),
    ]
    db.add_all(items)

async def seed_projects(db):
    """Borra e inserta datos de projects"""
    await db.execute(delete(Project))
    items = [
        Project(
            title="Tapicería Moderna",
            description="Plataforma de gestión para taller de tapicería. Permite seguimiento de pedidos, inventario y catálogo digital.",
            tags=["Vite", "Neon", "Django", "Tailwind"],
            icon_name="Layers",
            color="from-amber-500/20 to-orange-600/20",
            demo_url=None,
            github_url=None,
            image_url=None,
        ),
        Project(
            title="Sistema de Autenticación",
            description="Módulo de seguridad robusto con JWT, OAuth2 y recuperación de contraseñas. Diseñado para integración escalable.",
            tags=["FastAPI", "JWT", "PostgreSQL", "Security"],
            icon_name="Lock",
            color="from-blue-500/20 to-cyan-600/20",
            demo_url=None,
            github_url=None,
            image_url=None,
        ),
        Project(
            title="Gestor de Citas",
            description="Aplicación para reserva y administración de citas. Incluye recordatorios automatizados y calendario interactivo.",
            tags=["React", "Node.js", "MongoDB", "Calendar API"],
            icon_name="Calendar",
            color="from-green-500/20 to-teal-600/20",
            demo_url=None,
            github_url=None,
            image_url=None,
        ),
    ]
    db.add_all(items)

async def seed_stacks(db):
    """Borra e inserta datos de stacks"""
    await db.execute(delete(Stack))
    items = [
        # Frontend
        Stack(name="HTML5", category="Frontend", icon="Globe", description="Estructura Web", color="text-orange-500", border="group-hover:border-orange-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]"),
        Stack(name="CSS3", category="Frontend", icon="Palette", description="Estilos Modernos", color="text-blue-500", border="group-hover:border-blue-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"),
        Stack(name="Tailwind CSS", category="Frontend", icon="Palette", description="Estilos Utilitarios", color="text-cyan-400", border="group-hover:border-cyan-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]"),
        Stack(name="JavaScript", category="Frontend", icon="FileCode2", description="Interactividad", color="text-yellow-400", border="group-hover:border-yellow-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]"),
        Stack(name="TypeScript", category="Frontend", icon="FileCode2", description="JS Tipado", color="text-blue-400", border="group-hover:border-blue-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]"),
        Stack(name="React", category="Frontend", icon="Atom", description="Interfaces interactivas", color="text-cyan-400", border="group-hover:border-cyan-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]"),
        Stack(name="Astro", category="Frontend", icon="Rocket", description="Webs ultra rápidas", color="text-orange-400", border="group-hover:border-orange-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(251,146,60,0.3)]"),
        Stack(name="Next.js", category="Frontend", icon="LayoutTemplate", description="Framework de producción", color="text-white", border="group-hover:border-white/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]"),
        
        # Backend
        Stack(name="Python", category="Backend", icon="Terminal", description="Lenguaje Versátil", color="text-yellow-300", border="group-hover:border-yellow-300/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(253,224,71,0.3)]"),
        Stack(name="FastAPI", category="Backend", icon="Zap", description="APIs rápidas con Python", color="text-teal-400", border="group-hover:border-teal-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(45,212,191,0.3)]"),
        Stack(name="Django", category="Backend", icon="Layers", description="Framework Web Robusto", color="text-green-600", border="group-hover:border-green-600/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(22,163,74,0.3)]"),
        Stack(name="API REST", category="Backend", icon="Server", description="Arquitectura de APIs", color="text-indigo-400", border="group-hover:border-indigo-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(129,140,248,0.3)]"),
        Stack(name="JWT", category="Backend", icon="Lock", description="Seguridad & Auth", color="text-pink-500", border="group-hover:border-pink-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(236,72,153,0.3)]"),
        Stack(name="MongoDB", category="Backend", icon="Database", description="NoSQL escalable", color="text-green-400", border="group-hover:border-green-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(74,222,128,0.3)]"),
        Stack(name="NEON", category="Backend", icon="Server", description="Postgres Serverless", color="text-blue-400", border="group-hover:border-blue-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]"),
        
        # DevOps
        Stack(name="Docker", category="DevOps", icon="Container", description="Contenedorización", color="text-blue-500", border="group-hover:border-blue-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"),
        Stack(name="Git", category="DevOps", icon="GitBranch", description="Control de versiones", color="text-red-500", border="group-hover:border-red-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(239,68,68,0.3)]"),
        Stack(name="GitHub", category="DevOps", icon="Github", description="Colaboración", color="text-white", border="group-hover:border-white/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]"),
        Stack(name="Vercel", category="DevOps", icon="Triangle", description="Deploy Frontend", color="text-gray-200", border="group-hover:border-gray-200/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(229,231,235,0.2)]"),
        Stack(name="Render", category="DevOps", icon="Cloud", description="Cloud Hosting", color="text-purple-400", border="group-hover:border-purple-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(192,132,252,0.3)]"),
        
        # Herramientas
        Stack(name="VS Code", category="Herramientas", icon="Code2", description="Editor de Código", color="text-blue-500", border="group-hover:border-blue-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"),
        Stack(name="Postman", category="Herramientas", icon="Send", description="Testing de APIs", color="text-orange-500", border="group-hover:border-orange-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]"),
        Stack(name="IA & LLMs", category="Herramientas", icon="BrainCircuit", description="Inteligencia Artificial", color="text-rose-400", border="group-hover:border-rose-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(251,113,133,0.3)]"),
        Stack(name="Optimización", category="Herramientas", icon="Gauge", description="Performance Web", color="text-yellow-400", border="group-hover:border-yellow-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]"),
    ]
    db.add_all(items)

async def seed_footers(db):
    """Borra e inserta datos de footers"""
    await db.execute(delete(Footer))
    items = [
        Footer(
            name="Hernan Arango Cortes",
            description="Programador Full Stack enfocado en velocidad y rendimiento. Creando el futuro de la web desde Asturias para el mundo.",
            location="Avilés, Asturias, España",
            email="hernan.arango@example.com",
            github_url=None,
            linkedin_url=None,
            twitter_url=None,
            quick_links=[
                {"text": "Inicio", "href": "#inicio"},
                {"text": "Sobre Mí", "href": "#sobre-mi"},
                {"text": "Stack Tecnológico", "href": "#stack"},
                {"text": "Pasiones", "href": "#pasiones"}
            ],
        ),
    ]
    db.add_all(items)

async def main():
    async with AsyncSessionLocal() as db:
        # ejecutar en orden para respetar dependencias
        await seed_heroes(db)
        await seed_abouts(db)
        await seed_passions(db)
        await seed_projects(db)
        await seed_stacks(db)
        await seed_footers(db)
        await db.commit()
        print("✅ Seed completado")

if __name__ == "__main__":
    asyncio.run(main())
