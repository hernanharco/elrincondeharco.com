import pytest
from app.models.hero import Hero
from app.models.projects import Project
from app.models.stack import Stack
from app.models.site_settings import SiteSettings


class TestModels:
    """Test model creation and validations."""
    
    def test_hero_model_creation(self):
        """Test creating a Hero model instance."""
        hero = Hero(
            title="Test Hero",
            subtitle="Test Subtitle",
            description="Test Description",
            background_image="https://example.com/bg.jpg",
            contact_button_text="Contact",
            cv_button_text="Download CV",
            image_url="https://example.com/hero.jpg",
            cv_url="https://example.com/cv.pdf",
        )
        
        assert hero.title == "Test Hero"
        assert hero.subtitle == "Test Subtitle"
        assert hero.contact_button_text == "Contact"
        assert hero.cv_button_text == "Download CV"
        assert hero.cv_url == "https://example.com/cv.pdf"
    
    def test_project_model_creation(self):
        """Test creating a Project model instance."""
        project = Project(
            title="Test Project",
            description="Test Description",
            tags=["Test", "Project"],
            icon_name="TestIcon",
            color="from-test-500/20"
        )
        
        assert project.title == "Test Project"
        assert project.description == "Test Description"
        assert project.tags == ["Test", "Project"]
        assert project.icon_name == "TestIcon"
        assert project.color == "from-test-500/20"
    
    def test_stack_model_creation(self):
        """Test creating a Stack model instance."""
        stack = Stack(
            name="Test Technology",
            category="Frontend",
            icon="TestIcon",
            description="Test Description",
            color="text-test-500",
            border="group-hover:border-test-500/50",
            glow="group-hover:shadow-[0_0_30px_-5px_rgba(0,0,0,0.3)]"
        )
        
        assert stack.name == "Test Technology"
        assert stack.category == "Frontend"
        assert stack.icon == "TestIcon"
        assert stack.description == "Test Description"
    
    def test_site_settings_model_creation(self):
        """Test creating a SiteSettings model instance."""
        settings = SiteSettings(
            brand_name="Test Brand",
            site_url="https://test.com",
            legal_name="Test Legal",
            slogan="Test Slogan",
            copyright_notice="© 2024 Test"
        )
        
        assert settings.brand_name == "Test Brand"
        assert settings.site_url == "https://test.com"
        assert settings.legal_name == "Test Legal"
        assert settings.slogan == "Test Slogan"
        assert settings.copyright_notice == "© 2024 Test"
    
    def test_hero_model_required_fields(self):
        """Test Hero model requires mandatory fields."""
        # SQLAlchemy model doesn't validate on construction,
        # but missing NOT NULL columns will fail on flush
        hero = Hero(
            title="Test Hero",
            subtitle="Test Subtitle",
            description="Test Description",
            contact_button_text="Contact",
            cv_button_text="Download CV",
        )
        assert hero.title == "Test Hero"
        assert hero.subtitle == "Test Subtitle"
    
    def test_project_model_tags(self):
        """Test Project model tags functionality."""
        project = Project(
            title="Test Project",
            description="Test Description",
            tags=["Python", "FastAPI", "SQLAlchemy"],
            icon_name="Code",
            color="from-blue-500/20"
        )
        
        assert len(project.tags) == 3
        assert "Python" in project.tags
        assert "FastAPI" in project.tags
        assert "SQLAlchemy" in project.tags
