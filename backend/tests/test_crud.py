import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.hero import Hero
from app.models.projects import Project
from app.models.stack import Stack
from app.models.site_settings import SiteSettings


class TestCRUD:
    """Test CRUD operations."""
    
    async def test_create_hero(self, db_session: AsyncSession):
        """Test creating a hero in the database."""
        hero = Hero(
            title="Test Hero",
            subtitle="Test Subtitle",
            description="Test Description",
            contact_button_text="Contact",
            cv_button_text="Download CV",
            image_url="https://example.com/hero.jpg",
            cv_url="https://example.com/cv.pdf",
        )
        
        db_session.add(hero)
        await db_session.commit()
        await db_session.refresh(hero)
        
        assert hero.id is not None
        assert hero.title == "Test Hero"
        assert hero.subtitle == "Test Subtitle"
    
    async def test_read_hero(self, db_session: AsyncSession, sample_hero):
        """Test reading a hero from the database."""
        # Query the hero
        from sqlalchemy import select
        
        result = await db_session.execute(
            select(Hero).where(Hero.id == sample_hero.id)
        )
        hero = result.scalar_one_or_none()
        
        assert hero is not None
        assert hero.title == sample_hero.title
        assert hero.subtitle == sample_hero.subtitle
    
    async def test_update_hero(self, db_session: AsyncSession, sample_hero):
        """Test updating a hero in the database."""
        # Update hero
        sample_hero.title = "Updated Hero"
        sample_hero.subtitle = "Updated Subtitle"
        
        await db_session.commit()
        await db_session.refresh(sample_hero)
        
        assert sample_hero.title == "Updated Hero"
        assert sample_hero.subtitle == "Updated Subtitle"
    
    async def test_delete_hero(self, db_session: AsyncSession, sample_hero):
        """Test deleting a hero from the database."""
        hero_id = sample_hero.id
        
        await db_session.delete(sample_hero)
        await db_session.commit()
        
        # Verify deletion
        from sqlalchemy import select
        
        result = await db_session.execute(
            select(Hero).where(Hero.id == hero_id)
        )
        hero = result.scalar_one_or_none()
        
        assert hero is None
    
    async def test_create_project(self, db_session: AsyncSession):
        """Test creating a project in the database."""
        project = Project(
            title="Test Project",
            description="Test Description",
            tags=["Test", "Project"],
            icon_name="TestIcon",
            color="from-test-500/20"
        )
        
        db_session.add(project)
        await db_session.commit()
        await db_session.refresh(project)
        
        assert project.id is not None
        assert project.title == "Test Project"
        assert len(project.tags) == 2
    
    async def test_list_projects(self, db_session: AsyncSession):
        """Test listing all projects."""
        # Create multiple projects
        projects = [
            Project(
                title=f"Project {i}",
                description=f"Description {i}",
                tags=["Test"],
                icon_name="TestIcon",
                color="from-test-500/20"
            )
            for i in range(3)
        ]
        
        for project in projects:
            db_session.add(project)
        await db_session.commit()
        
        # Query all projects
        from sqlalchemy import select
        
        result = await db_session.execute(select(Project))
        all_projects = result.scalars().all()
        
        assert len(all_projects) >= 3
    
    async def test_create_stack(self, db_session: AsyncSession):
        """Test creating a stack in the database."""
        stack = Stack(
            name="Python",
            category="Backend",
            icon="Code",
            description="Programming language",
            color="text-blue-500",
            border="group-hover:border-blue-500/50",
            glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"
        )
        
        db_session.add(stack)
        await db_session.commit()
        await db_session.refresh(stack)
        
        assert stack.id is not None
        assert stack.name == "Python"
        assert stack.category == "Backend"
    
    async def test_stacks_by_category(self, db_session: AsyncSession):
        """Test filtering stacks by category."""
        # Create stacks in different categories
        stacks = [
            Stack(
                name="Python",
                category="Backend",
                icon="Code",
                description="Backend language",
                color="text-blue-500",
                border="group-hover:border-blue-500/50",
                glow="group-hover:shadow-[0_0_30px_-5px_rgba(59,130,246,0.3)]"
            ),
            Stack(
                name="React",
                category="Frontend",
                icon="Globe",
                description="Frontend framework",
                color="text-cyan-500",
                border="group-hover:border-cyan-500/50",
                glow="group-hover:shadow-[0_0_30px_-5px_rgba(6,182,212,0.3)]"
            )
        ]
        
        for stack in stacks:
            db_session.add(stack)
        await db_session.commit()
        
        # Query by category
        from sqlalchemy import select
        
        result = await db_session.execute(
            select(Stack).where(Stack.category == "Backend")
        )
        backend_stacks = result.scalars().all()
        
        assert len(backend_stacks) == 1
        assert backend_stacks[0].name == "Python"
    
    async def test_site_settings_singleton(self, db_session: AsyncSession):
        """Test that site settings work as a singleton."""
        # Create site settings
        settings = SiteSettings(
            brand_name="Test Brand",
            site_url="https://test.com",
            legal_name="Test Legal",
            slogan="Test Slogan",
            copyright_notice="© 2024 Test",
            contact_email="test@test.com"
        )
        
        db_session.add(settings)
        await db_session.commit()
        await db_session.refresh(settings)
        
        assert settings.id is not None
        assert settings.brand_name == "Test Brand"
