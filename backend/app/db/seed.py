import asyncio
import json
from sqlalchemy import delete
from app.db.session import AsyncSessionLocal
# IMPORTANTE: Importa tus modelos aquí
from app.models.models import Hero, About, Passion, Project, Stack, SiteSettings

async def seed_site_settings(db):
    """Borra e inserta la configuración de marca y sitio"""
    await db.execute(delete(SiteSettings))
    item = SiteSettings(
        brand_name="elRincondelHarco.com",
        site_url="https://elrincondelharco.com",
        legal_name="Hernan Arango Cortes",
        slogan="Programador Full Stack enfocado en velocidad y rendimiento.",
        copyright_notice="Todos los derechos reservados.",
        contact_email="hernan.harco@gmail.com",
        social_networks={
            "github": "https://github.com/hernanharco",
            "linkedin": "https://www.linkedin.com/in/hernan-harco/",
            "twitter": None
        }
    )
    db.add(item)

async def seed_heroes(db):
    await db.execute(delete(Hero))
    item = Hero(
        title="Desarrollador Full Stack",
        subtitle="Hernan Arango Cortes",
        description="Transformando 14+ años de experiencia en liderazgo...",
        contact_button_text="Contactar",
        cv_button_text="Descargar CV",
        image_url="https://res.cloudinary.com/..."
    )
    db.add(item)

async def seed_abouts(db):
    await db.execute(delete(About))
    item = About(
        years_experience="14+ Años",
        location="Avilés, Asturias, España",
        team_name="Equipo de Oro",
        leadership_title="Liderazgo",
        leadership_desc="Formación de equipos de alto rendimiento.",
        experience_title="Experiencia",
        experience_desc="Más de una década entregando soluciones."
    )
    db.add(item)

async def seed_passions(db):
    await db.execute(delete(Passion))
    item = Passion(
        title="Más allá del Código",
        description="Mi pasión es estar con mi familia.",
        family_title="Mi Familia",
        family_desc="Son mi motor.",
        games_title="Videojuegos",
        games_desc="Desconexión total.",
        coding_title="Programación",
        coding_desc="Mi forma de crear."
    )
    db.add(item)

async def seed_projects(db):
    await db.execute(delete(Project))
    items = [
        Project(
            title="Tapicería Moderna",
            description="Plataforma de gestión para taller.",
            tags=["Vite", "Neon", "Django"],
            icon_name="Layers",
            color="from-amber-500/20 to-orange-600/20"
        ),
        # ... otros proyectos
    ]
    db.add_all(items)

async def seed_stacks(db):
    await db.execute(delete(Stack))
    items = [
        Stack(
            name="HTML5", 
            category="Frontend", 
            icon="Globe", 
            description="Estructura Web", 
            color="text-orange-500", 
            border="group-hover:border-orange-500/50", 
            glow="group-hover:shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]"
        ),
        # ... el resto de tus stacks
    ]
    db.add_all(items)

async def main():
    async with AsyncSessionLocal() as db:
        try:
            print("⏳ Iniciando seed...")
            await seed_site_settings(db) # El nuevo para tu marca
            await seed_heroes(db)
            await seed_abouts(db)
            await seed_passions(db)
            await seed_projects(db)
            await seed_stacks(db)
            
            await db.commit()
            print("✅ Seed completado con éxito")
        except Exception as e:
            await db.rollback()
            print(f"❌ Error en el seed: {e}")

if __name__ == "__main__":
    asyncio.run(main())