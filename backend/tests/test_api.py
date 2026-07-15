import pytest
from httpx import AsyncClient


class TestAPI:
    """Test API endpoints."""
    
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    async def test_get_hero(self, client: AsyncClient, sample_hero):
        """Test getting hero information via API."""
        response = await client.get("/api/v1/heroes/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "title" in data[0]
        assert "subtitle" in data[0]

    async def test_get_projects(self, client: AsyncClient, sample_project):
        """Test getting projects list."""
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check project structure
        project = data[0]
        assert "title" in project
        assert "description" in project
        assert "tags" in project
        assert "icon_name" in project
        assert "color" in project
    
    async def test_get_stacks(self, client: AsyncClient):
        """Test getting stacks list."""
        # First create a stack
        from app.models.stack import Stack
        from app.db.session import get_db
        
        # We'll create a stack through the API or directly in the database
        # For now, let's test the endpoint structure
        response = await client.get("/api/v1/stacks/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # If there are stacks, check structure
        if data:
            stack = data[0]
            assert "name" in stack
            assert "category" in stack
            assert "icon" in stack
            assert "description" in stack
    
    async def test_get_site_settings(self, client: AsyncClient, sample_site_settings):
        """Test getting site settings."""
        response = await client.get("/api/v1/site-settings/")
        assert response.status_code == 200
        data = response.json()
        # The endpoint returns a list, get the first item
        if isinstance(data, list):
            data = data[0]
        assert "brand_name" in data
        assert "site_url" in data
        assert "legal_name" in data
        assert "slogan" in data
    
    async def test_cors_headers(self, client: AsyncClient, sample_project):
        """Test CORS headers are present on responses with Origin header."""
        response = await client.get(
            "/api/v1/projects/",
            headers={"Origin": "http://localhost:4321"}
        )
        assert response.status_code == 200
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
    
    async def test_404_error(self, client: AsyncClient):
        """Test 404 error handling."""
        response = await client.get("/api/v1/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    async def test_api_response_format(self, client: AsyncClient, sample_project):
        """Test API responses are in correct JSON format."""
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        data = response.json()
        assert isinstance(data, list)
        
        # Test individual project structure
        if data:
            project = data[0]
            required_fields = ["id", "title", "description", "tags", "icon_name", "color"]
            for field in required_fields:
                assert field in project
    
    async def test_project_tags_structure(self, client: AsyncClient, sample_project):
        """Test project tags are properly structured."""
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        
        if data:
            project = data[0]
            assert isinstance(project["tags"], list)
            assert all(isinstance(tag, str) for tag in project["tags"])
    
    async def test_stack_categories(self, client: AsyncClient):
        """Test stacks are properly categorized."""
        response = await client.get("/api/v1/stacks/")
        assert response.status_code == 200
        data = response.json()
        
        if data:
            # Check that stacks have valid categories
            valid_categories = ["Frontend", "Backend", "Database", "DevOps", "Tools"]
            for stack in data:
                assert stack["category"] in valid_categories
