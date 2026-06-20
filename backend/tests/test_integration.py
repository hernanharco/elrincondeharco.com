import pytest
from httpx import AsyncClient
from app.models.hero import Hero
from app.models.projects import Project
from app.models.stack import Stack
from app.models.site_settings import SiteSettings


class TestIntegration:
    """Test integration between different components."""
    
    async def test_full_api_flow(self, client: AsyncClient, db_session):
        """Test complete flow: API -> Database -> Response."""
        # 1. Create data through database
        hero = Hero(
            title="Integration Test Hero",
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
        
        # 2. Fetch through API (list endpoint returns array)
        response = await client.get("/api/v1/heroes/")
        assert response.status_code == 200
        
        # 3. Verify API response matches database
        data = response.json()
        assert len(data) > 0
        assert data[0]["title"] == "Integration Test Hero"
    
    async def test_projects_api_with_database(self, client: AsyncClient, db_session):
        """Test projects API with real database data."""
        # Create multiple projects
        projects = [
            Project(
                title=f"Integration Project {i}",
                description=f"Description {i}",
                tags=["Integration", "Test"],
                icon_name="Code",
                color="from-blue-500/20"
            )
            for i in range(3)
        ]
        
        for project in projects:
            db_session.add(project)
        await db_session.commit()
        
        # Test API response
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 3
        
        # Verify all created projects are returned
        project_titles = [p["title"] for p in data]
        for i in range(3):
            assert f"Integration Project {i}" in project_titles
    
    async def test_stacks_by_category_integration(self, client: AsyncClient, db_session):
        """Test stacks filtering by category through API."""
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
            ),
            Stack(
                name="PostgreSQL",
                category="Database",
                icon="Database",
                description="Database system",
                color="text-green-500",
                border="group-hover:border-green-500/50",
                glow="group-hover:shadow-[0_0_30px_-5px_rgba(34,197,94,0.3)]"
            )
        ]
        
        for stack in stacks:
            db_session.add(stack)
        await db_session.commit()
        
        # Test API returns all stacks
        response = await client.get("/api/v1/stacks/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) >= 3
        
        # Verify categories
        categories = [stack["category"] for stack in data]
        assert "Backend" in categories
        assert "Frontend" in categories
        assert "Database" in categories
    
    async def test_site_settings_integration(self, client: AsyncClient, db_session):
        """Test site settings integration."""
        # Create site settings
        settings = SiteSettings(
            brand_name="Integration Test Brand",
            site_url="https://integration-test.com",
            legal_name="Integration Legal Name",
            slogan="Integration Slogan",
            copyright_notice="© 2024 Integration Test"
        )
        
        db_session.add(settings)
        await db_session.commit()
        
        # Test API response
        response = await client.get("/api/v1/site-settings/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["brand_name"] == "Integration Test Brand"
        assert data["site_url"] == "https://integration-test.com"
        assert data["legal_name"] == "Integration Legal Name"
    
    async def test_error_handling_integration(self, client: AsyncClient):
        """Test error handling across the application."""
        # Test non-existent endpoint
        response = await client.get("/api/v1/nonexistent")
        assert response.status_code == 404
        assert "detail" in response.json()
        
        # Test invalid method
        response = await client.post("/api/v1/heroes/")
        # This should return 405 Method Not Allowed or 422 for validation error
        assert response.status_code in [405, 422]
    
    async def test_cors_integration(self, client: AsyncClient):
        """Test CORS integration with frontend."""
        # Test preflight request
        response = await client.options("/api/v1/projects/")
        assert response.status_code == 200
        
        # Check CORS headers
        headers = response.headers
        assert "access-control-allow-origin" in headers
        assert "access-control-allow-methods" in headers
        assert "access-control-allow-headers" in headers
    
    async def test_database_transaction_with_api(self, client: AsyncClient, db_session):
        """Test database transactions work correctly with API calls."""
        # Create a project in a transaction
        async with db_session.begin():
            project = Project(
                title="Transaction Test Project",
                description="Test Description",
                tags=["Transaction", "Test"],
                icon_name="Code",
                color="from-blue-500/20"
            )
            db_session.add(project)
            # Transaction will be committed automatically
        
        # Verify it's available through API
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        
        data = response.json()
        project_titles = [p["title"] for p in data]
        assert "Transaction Test Project" in project_titles
    
    async def test_full_seed_integration(self, client: AsyncClient, db_session):
        """Test full seed process integration."""
        from app.db.seed import seed_site_settings, seed_heroes, seed_projects, seed_stacks
        
        # Clean database
        await db_session.execute(Hero.__table__.delete())
        await db_session.execute(Project.__table__.delete())
        await db_session.execute(Stack.__table__.delete())
        await db_session.execute(SiteSettings.__table__.delete())
        await db_session.commit()
        
        # Run full seed
        await seed_site_settings(db_session)
        await seed_heroes(db_session)
        await seed_projects(db_session)
        await seed_stacks(db_session)
        await db_session.commit()
        
        # Test all endpoints return data
        hero_response = await client.get("/api/v1/heroes/")
        assert hero_response.status_code == 200
        
        projects_response = await client.get("/api/v1/projects/")
        assert projects_response.status_code == 200
        assert len(projects_response.json()) > 0
        
        stacks_response = await client.get("/api/v1/stacks/")
        assert stacks_response.status_code == 200
        assert len(stacks_response.json()) > 0
        
        settings_response = await client.get("/api/v1/site-settings/")
        assert settings_response.status_code == 200
        assert "brand_name" in settings_response.json()
    
    async def test_concurrent_api_requests(self, client: AsyncClient, sample_project):
        """Test handling concurrent API requests."""
        import asyncio
        
        # Make multiple concurrent requests
        async def make_request():
            return await client.get("/api/v1/projects/")
        
        tasks = [make_request() for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert isinstance(response.json(), list)
