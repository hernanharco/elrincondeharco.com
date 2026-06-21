import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.config import settings
from app.models.base import Base


class TestDatabase:
    """Test database operations and connections."""
    
    async def test_database_connection(self):
        """Test that we can connect to the database."""
        engine = create_async_engine(settings.database_url)
        
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        
        await engine.dispose()
    
    async def test_database_tables_creation(self):
        """Test that all tables can be created."""
        test_engine = create_async_engine(settings.database_url)
        
        async with test_engine.begin() as conn:
            # Drop all tables first
            await conn.run_sync(Base.metadata.drop_all)
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        # Verify tables exist
        async with test_engine.begin() as conn:
            result = await conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            )
            tables = [row[0] for row in result.fetchall()]
            
            # Check that our main tables exist
            expected_tables = ["heroes", "projects", "stacks", "site_settings"]
            for table in expected_tables:
                assert any(table in t for t in tables)
        
        await test_engine.dispose()
    
    async def test_database_transaction_rollback(self):
        """Test database transaction rollback."""
        test_engine = create_async_engine(settings.database_url)
        TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
        
        async with TestSessionLocal() as session:
            # Start a transaction
            await session.begin()
            
            # Add a hero
            from app.models.hero import Hero
            hero = Hero(
                title="Test Hero",
                subtitle="Test Subtitle",
                description="Test Description",
                contact_button_text="Contact",
                cv_button_text="Download CV",
                image_url="https://example.com/hero.jpg",
                cv_url="https://example.com/cv.pdf",
            )
            session.add(hero)
            await session.flush()
            hero_id = hero.id
            
            # Rollback the transaction
            await session.rollback()
        
        # Verify the hero was not committed
        async with TestSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(select(Hero).where(Hero.id == hero_id))
            hero = result.scalar_one_or_none()
            assert hero is None
        
        await test_engine.dispose()
    
    async def test_database_connection_pooling(self):
        """Test database connection pooling."""
        # Create multiple concurrent connections
        async def test_connection():
            engine = create_async_engine(settings.database_url, pool_size=5)
            async with engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                return result.scalar()
            await engine.dispose()
        
        # Run multiple connections concurrently
        tasks = [test_connection() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All should succeed
        assert all(result == 1 for result in results)
    
    async def test_database_error_handling(self):
        """Test database error handling."""
        engine = create_async_engine(settings.database_url)
        
        async with engine.begin() as conn:
            # Try to execute invalid SQL
            with pytest.raises(Exception):  # This should raise a database error
                await conn.execute(text("SELECT * FROM nonexistent_table"))
        
        await engine.dispose()
    
    async def test_seed_data_functionality(self):
        """Test that seed data can be inserted correctly."""
        test_engine = create_async_engine(settings.database_url)
        TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
        
        # Clean up first
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        # Test seed functionality
        from app.db.seed import seed_site_settings, seed_heroes, seed_projects, seed_stacks
        
        async with TestSessionLocal() as session:
            # Seed all data
            await seed_site_settings(session)
            await seed_heroes(session)
            await seed_projects(session)
            await seed_stacks(session)
            
            await session.commit()
        
        # Verify data was seeded
        async with TestSessionLocal() as session:
            from sqlalchemy import select
            from app.models.hero import Hero
            from app.models.projects import Project
            from app.models.stack import Stack
            from app.models.site_settings import SiteSettings
            
            # Check site settings
            result = await session.execute(select(SiteSettings))
            settings = result.scalar_one_or_none()
            assert settings is not None
            assert settings.brand_name == "elRincondelHarco.com"
            
            # Check heroes
            result = await session.execute(select(Hero))
            heroes = result.scalars().all()
            assert len(heroes) > 0
            
            # Check projects
            result = await session.execute(select(Project))
            projects = result.scalars().all()
            assert len(projects) > 0
            
            # Check stacks
            result = await session.execute(select(Stack))
            stacks = result.scalars().all()
            assert len(stacks) > 0
        
        await test_engine.dispose()
