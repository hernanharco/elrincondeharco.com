import asyncio
from sqlalchemy import delete
from app.db.session import AsyncSessionLocal

# --- IMPORTS DE MODELOS ---
from app.models.hero import Hero
from app.models.about import About
from app.models.passions import Passion
from app.models.projects import Project
from app.models.stack import Stack
from app.models.site_settings import SiteSettings
from app.models.footer import Footer


def fix_cloudinary_pdf(url: str) -> str:
    """
    Asegura que el flag de descarga /fl_attachment/ esté presente EXACTAMENTE UNA VEZ.
    Evita URLs corruptas como /fl_attachment/fl_attachment/ (Error 404 en Cloudinary).
    """
    if not url or "cloudinary.com" not in url or ".pdf" not in url.lower():
        return url

    if "/fl_attachment/" in url:
        return url

    return url.replace("/upload/", "/upload/fl_attachment/")


async def seed_site_settings(db):
    print("  🌐 Seeding SiteSettings (Configuración de Marca)...")
    await db.execute(delete(SiteSettings))
    item = SiteSettings(
        brand_name="elRincondelHarco.com",
        site_url="https://elrincondeharco.com",
        legal_name="Hernan Arango Cortes",
        slogan="Programador Full Stack enfocado en velocidad y rendimiento.",
        copyright_notice="© 2026 Todos los derechos reservados.",
        contact_email="hernan.harco@gmail.com",
        social_networks={
            "github": "https://github.com/hernanharco",
            "linkedin": "https://www.linkedin.com/in/hernan-harco/",
        },
        is_active=True
    )
    db.add(item)


async def seed_heroes(db):
    print("  🦸 Seeding Hero...")
    await db.execute(delete(Hero))

    # URL limpia (sin duplicar fl_attachment)
    cv_url = "https://res.cloudinary.com/dxyk76jhu/image/upload/v1774016513/elrincondelharco/k7zq6qe4xryb9qahiahj.pdf"
    # Opcional: aplicar fix si quieres
    # cv_url = fix_cloudinary_pdf(cv_url)

    item = Hero(
        title="Desarrollador Full Stack",
        subtitle="Hernan Arango Cortes",
        description="Transformando 14+ años de experiencia en liderazgo y análisis en soluciones tecnológicas innovadoras. Mi familia es mi motor, la tecnología mi pasión, y el emprendimiento mi camino hacia el futuro.",
        contact_button_text="Contactar",
        cv_button_text="Descargar CV",
        cv_url=cv_url
    )
    db.add(item)


async def seed_abouts(db):
    print("  ℹ️  Seeding About...")
    await db.execute(delete(About))
    item = About(
        title="Mi Trayectoria Profesional",
        description="Más de una década dedicada al desarrollo de software, liderazgo de equipos y optimización de procesos técnicos.",
        years_experience="14+ Años",
        location="Avilés, Asturias, España",
        team_name="Equipo de Oro",
        leadership_title="Liderazgo",
        leadership_desc="Formación de equipos de alto rendimiento.",
        experience_title="Experiencia",
        experience_desc="Más de una década entregando soluciones tecnológicas.",
    )
    db.add(item)


async def seed_passions(db):
    print("  🔥 Seeding Passions...")
    await db.execute(delete(Passion))
    item = Passion(
        title="Más allá del Código",
        description="Mi pasión, aparte de programar y jugar videojuegos, es estar con mi familia.",
        family_title="Mi Familia",
        family_desc="Son mi motor y la razón de querer continuar cada día.",
        games_title="Videojuegos",
        games_desc="Un hobby que me permite desconectar y explorar nuevos mundos.",
        coding_title="Programación",
        coding_desc="No es solo mi trabajo, es mi forma de crear y aportar valor.",
    )
    db.add(item)


async def seed_projects(db):
    print("  🚀 Seeding Projects...")
    await db.execute(delete(Project))
    items = [
        Project(
            title="Tapicería Moderna",
            description="Plataforma de gestión para taller de tapicería. Seguimiento de pedidos e inventario.",
            tags=["Vite", "Neon", "Django", "Tailwind"],
            icon_name="Layers",
            color="from-amber-500/20 to-orange-600/20"
        ),
        Project(
            title="CoreAppointment",
            description="Sistema modular de gestión de citas y turnos multi-tenant.",
            tags=["FastAPI", "Svelte", "PostgreSQL"],
            icon_name="Calendar",
            color="from-blue-500/20 to-cyan-600/20"
        ),
        Project(
            title="Módulo de Seguridad",
            description="Autenticación robusta con JWT y OAuth2 para aplicaciones FastAPI.",
            tags=["FastAPI", "JWT", "Security"],
            icon_name="Lock",
            color="from-pink-500/20 to-rose-600/20"
        )
    ]
    db.add_all(items)


async def seed_stacks(db):
    print("  💻 Seeding Full Arsenal Técnico (24 tecnologías)...")
    await db.execute(delete(Stack))

    items = [
        # FRONTEND
        Stack(name="HTML5", category="Frontend", icon="Globe", description="Estructura Web", color="text-orange-500", border="group-hover:border-orange-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]"),
        Stack(name="CSS3", category="Frontend", icon="Palette", description="Estilos Modernos", color="text-blue-500", border="group-hover:border-blue-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"),
        Stack(name="Tailwind CSS", category="Frontend", icon="Palette", description="Estilos Utilitarios", color="text-cyan-400", border="group-hover:border-cyan-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]"),
        Stack(name="JavaScript", category="Frontend", icon="FileCode2", description="Interactividad", color="text-yellow-400", border="group-hover:border-yellow-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]"),
        Stack(name="TypeScript", category="Frontend", icon="FileCode2", description="JS Tipado", color="text-blue-400", border="group-hover:border-blue-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]"),
        Stack(name="React", category="Frontend", icon="Atom", description="Interfaces interactivas", color="text-cyan-400", border="group-hover:border-cyan-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]"),
        Stack(name="Astro", category="Frontend", icon="Rocket", description="Webs ultra rápidas", color="text-orange-400", border="group-hover:border-orange-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(251,146,60,0.3)]"),
        Stack(name="Next.js", category="Frontend", icon="LayoutTemplate", description="Framework de producción", color="text-white", border="group-hover:border-white/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]"),

        # BACKEND
        Stack(name="Python", category="Backend", icon="Terminal", description="Lenguaje Versátil", color="text-yellow-300", border="group-hover:border-yellow-300/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(253,224,71,0.3)]"),
        Stack(name="FastAPI", category="Backend", icon="Zap", description="APIs rápidas con Python", color="text-teal-400", border="group-hover:border-teal-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(45,212,191,0.3)]"),
        Stack(name="Django", category="Backend", icon="Layers", description="Framework Web Robusto", color="text-green-600", border="group-hover:border-green-600/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(22,163,74,0.3)]"),
        Stack(name="API REST", category="Backend", icon="Server", description="Arquitectura de APIs", color="text-indigo-400", border="group-hover:border-indigo-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(129,140,248,0.3)]"),
        Stack(name="JWT", category="Backend", icon="Lock", description="Seguridad & Auth", color="text-pink-500", border="group-hover:border-pink-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(236,72,153,0.3)]"),
        Stack(name="MongoDB", category="Backend", icon="Database", description="NoSQL escalable", color="text-green-400", border="group-hover:border-green-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(74,222,128,0.3)]"),
        Stack(name="NEON", category="Backend", icon="Server", description="Postgres Serverless", color="text-blue-400", border="group-hover:border-blue-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(96,165,250,0.3)]"),

        # DEVOPS
        Stack(name="Docker", category="DevOps", icon="Container", description="Contenedorización", color="text-blue-500", border="group-hover:border-blue-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"),
        Stack(name="Git", category="DevOps", icon="GitBranch", description="Control de versiones", color="text-red-500", border="group-hover:border-red-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(239,68,68,0.3)]"),
        Stack(name="GitHub", category="DevOps", icon="Github", description="Colaboración", color="text-white", border="group-hover:border-white/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(255,255,255,0.2)]"),
        Stack(name="Vercel", category="DevOps", icon="Triangle", description="Deploy Frontend", color="text-gray-200", border="group-hover:border-gray-200/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(229,231,235,0.2)]"),
        Stack(name="Render", category="DevOps", icon="Cloud", description="Cloud Hosting", color="text-purple-400", border="group-hover:border-purple-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(192,132,252,0.3)]"),

        # HERRAMIENTAS
        Stack(name="VS Code", category="Herramientas", icon="Code2", description="Editor de Código", color="text-blue-500", border="group-hover:border-blue-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"),
        Stack(name="Postman", category="Herramientas", icon="Send", description="Testing de APIs", color="text-orange-500", border="group-hover:border-orange-500/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]"),
        Stack(name="IA & LLMs", category="Herramientas", icon="BrainCircuit", description="Inteligencia Artificial", color="text-rose-400", border="group-hover:border-rose-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(251,113,133,0.3)]"),
        Stack(name="Optimización", category="Herramientas", icon="Gauge", description="Performance Web", color="text-yellow-400", border="group-hover:border-yellow-400/50", glow="group-hover:shadow-[0_0_30px_-5px_rgba(250,204,21,0.3)]"),
    ]
    db.add_all(items)


async def seed_footers(db):
    print("  🦶 Seeding Footer...")
    await db.execute(delete(Footer))
    item = Footer(
        name="Hernan Arango Cortes",
        description="Programador Full Stack enfocado en rendimiento. Creando el futuro web desde Asturias.",
        location="Avilés, Asturias, España",
        email="hernan.harco@gmail.com",
        quick_links=[
            {"text": "Inicio", "href": "#inicio"},
            {"text": "Sobre Mí", "href": "#sobre-mi"},
            {"text": "Stack", "href": "#stack"}
        ]
    )
    db.add(item)


async def main():
    async with AsyncSessionLocal() as db:
        try:
            print("\n🚀 Iniciando sincronización de base de datos (Seed) en Neon/PostgreSQL...")

            await seed_site_settings(db)
            await seed_heroes(db)
            await seed_abouts(db)
            await seed_passions(db)
            await seed_projects(db)
            await seed_stacks(db)
            await seed_footers(db)

            await db.commit()
            print("\n✅ ¡Seed completado con éxito! Todo el arsenal está listo.\n")
        except Exception as e:
            await db.rollback()
            print(f"\n❌ Error crítico durante el Seed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())