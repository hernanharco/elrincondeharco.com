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
            "/api/v1/projects/", headers={"Origin": "http://localhost:4321"}
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
            required_fields = [
                "id",
                "title",
                "description",
                "tags",
                "icon_name",
                "color",
            ]
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
            valid_categories = ["Frontend", "Backend", "DevOps", "Herramientas"]
            for stack in data:
                assert stack["category"] in valid_categories


class TestExperienceAPI:
    """Tests for the Experience Section API."""

    async def test_create_experience(self, client: AsyncClient, admin_override):
        """Test creating an experience section."""
        response = await client.post(
            "/api/v1/experience/",
            data={
                "tagline": "Experiencia",
                "title": "Test <span>Title</span>",
                "description": "Test description",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["tagline"] == "Experiencia"
        assert "title" in data
        assert "description" in data

    async def test_get_latest_experience(self, client: AsyncClient, db_session):
        """Test getting latest experience section."""
        from app.models.experience import ExperienceSection

        exp = ExperienceSection(tagline="Test", title="Title", description="Desc")
        db_session.add(exp)
        await db_session.commit()

        response = await client.get("/api/v1/experience/latest/")
        assert response.status_code == 200
        data = response.json()
        assert data["tagline"] == "Test"

    async def test_update_experience(
        self, client: AsyncClient, db_session, admin_override
    ):
        """Test updating an experience section."""
        from app.models.experience import ExperienceSection

        exp = ExperienceSection(
            tagline="Old", title="Old Title", description="Old Desc"
        )
        db_session.add(exp)
        await db_session.commit()

        response = await client.put(
            f"/api/v1/experience/{exp.id}",
            data={
                "tagline": "Updated",
                "title": "Updated Title",
                "description": "Updated Desc",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["tagline"] == "Updated"
        assert data["title"] == "Updated Title"

    async def test_experience_404(self, client: AsyncClient):
        """Test 404 when no experience exists."""
        response = await client.get("/api/v1/experience/latest/")
        assert response.status_code == 404


class TestPublicTestimonialsAPI:
    """Tests for the public testimonials endpoint."""

    async def test_public_submission(self, client: AsyncClient):
        """Test submitting a testimonial via public endpoint."""
        response = await client.post(
            "/api/v1/testimonials/public",
            json={
                "name": "Test User",
                "role": "Tester",
                "company": "Test Co",
                "content": "Great service!",
                "rating": 5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "gracias" in data["message"].lower()

    async def test_public_submission_creates_inactive(
        self, client: AsyncClient, db_session
    ):
        """Test public submissions are created with is_active=False."""
        response = await client.post(
            "/api/v1/testimonials/public",
            json={"name": "Test", "content": "Test content", "rating": 4},
        )
        assert response.status_code == 200

        # Verify directly in DB
        from app.models.testimonial import Testimonial
        from sqlalchemy import select

        result = await db_session.execute(select(Testimonial))
        testimonial = result.scalars().first()
        assert testimonial is not None
        assert testimonial.is_active is False
        assert testimonial.name == "Test"

    async def test_public_submission_minimal_fields(self, client: AsyncClient):
        """Test submitting with only required fields (name, content, rating)."""
        response = await client.post(
            "/api/v1/testimonials/public",
            json={"name": "Minimal", "content": "Minimal content", "rating": 3},
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

    async def test_active_testimonials_visible(self, client: AsyncClient, db_session):
        """Test only active testimonials appear on public endpoint."""
        from app.models.testimonial import Testimonial

        db_session.add_all(
            [
                Testimonial(
                    name="Active",
                    content="Active",
                    rating=5,
                    is_active=True,
                    sort_order=1,
                ),
                Testimonial(
                    name="Inactive",
                    content="Inactive",
                    rating=4,
                    is_active=False,
                    sort_order=2,
                ),
            ]
        )
        await db_session.commit()

        response = await client.get("/api/v1/testimonials/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Active"


class TestCTASiteSettingsAPI:
    """Tests for CTA fields in SiteSettings."""

    async def test_cta_fields_in_response(self, client: AsyncClient, db_session):
        """Test CTA fields are present in site settings response."""
        from app.models.site_settings import SiteSettings

        ss = SiteSettings(
            brand_name="Test",
            site_url="https://test.com",
            legal_name="Test Legal",
            copyright_notice="© Test",
            contact_email="test@test.com",
            cta_title="Test <span>CTA</span>",
            cta_description="Test description",
            cta_features=["Feature 1", "Feature 2"],
            cta_primary_text="Contact Us",
            cta_secondary_text="LinkedIn",
        )
        db_session.add(ss)
        await db_session.commit()

        response = await client.get("/api/v1/site-settings/latest/")
        assert response.status_code == 200
        data = response.json()
        assert data["cta_title"] == "Test <span>CTA</span>"
        assert data["cta_description"] == "Test description"
        assert "Feature 1" in data["cta_features"]
        assert len(data["cta_features"]) == 2
        assert data["cta_primary_text"] == "Contact Us"
        assert data["cta_secondary_text"] == "LinkedIn"

    async def test_cta_fields_optional(self, client: AsyncClient, sample_site_settings):
        """Test CTA fields are optional and default to null."""
        response = await client.get("/api/v1/site-settings/latest/")
        assert response.status_code == 200
        data = response.json()
        # sample_site_settings has no CTA fields -> should be null
        assert "cta_title" in data
        assert "cta_features" in data

    async def test_update_cta_fields(self, client: AsyncClient, db_session):
        """Test updating CTA fields via PUT."""
        from app.models.site_settings import SiteSettings

        ss = SiteSettings(
            brand_name="Test",
            site_url="https://test.com",
            legal_name="Test",
            copyright_notice="©",
            contact_email="t@t.com",
        )
        db_session.add(ss)
        await db_session.commit()

        response = await client.put(
            f"/api/v1/site-settings/{ss.id}",
            data={
                "cta_title": "New CTA Title",
                "cta_description": "New description",
                "cta_features": '["A","B","C"]',
                "cta_primary_text": "Email Us",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["cta_title"] == "New CTA Title"
        assert data["cta_primary_text"] == "Email Us"
        assert len(data["cta_features"]) == 3


class TestProjectsImageUrlsAPI:
    """Tests for projects image_urls field."""

    async def test_project_image_urls_field(self, client: AsyncClient, db_session):
        """Test project has image_urls array in response."""
        from app.models.projects import Project

        project = Project(
            title="Test",
            description="Test",
            tags=["a"],
            icon_name="Icon",
            color="red",
            image_urls=["https://img1.com", "https://img2.com"],
        )
        db_session.add(project)
        await db_session.commit()

        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        p = data[0]
        assert "image_urls" in p
        assert isinstance(p["image_urls"], list)
        assert len(p["image_urls"]) == 2

    async def test_project_image_urls_empty_default(
        self, client: AsyncClient, sample_project
    ):
        """Test project defaults to empty image_urls array."""
        response = await client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        p = data[0]
        assert isinstance(p["image_urls"], list)
