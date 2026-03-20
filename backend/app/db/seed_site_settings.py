import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.site_settings import SiteSettings
from app.core.config import settings
from app.db.session import async_session


async def seed_site_settings():
    """Seed SiteSettings con datos iniciales"""
    print("🌐 Seeding SiteSettings...")
    
    async with async_session() as db:
        try:
            # Limpiar configuraciones existentes
            await db.execute(delete(SiteSettings))
            await db.commit()
            print("✅ SiteSettings limpiados")
            
            # Crear configuración inicial
            site_settings = SiteSettings(
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
                },
                is_active=True
            )
            
            db.add(site_settings)
            await db.commit()
            await db.refresh(site_settings)
            
            print(f"✅ SiteSettings creado: {site_settings.brand_name}")
            print(f"   📧 Email: {site_settings.contact_email}")
            print(f"   🔗 GitHub: {site_settings.social_networks.get('github')}")
            
        except Exception as e:
            print(f"❌ Error creando SiteSettings: {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_site_settings())
