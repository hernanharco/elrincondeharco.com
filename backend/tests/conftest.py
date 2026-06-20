import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.config import settings
from app.models.base import Base
from app.db.session import get_db

# Test database URL
TEST_DATABASE_URL = settings.database_url.replace("/neondb", "/test_neondb")

# Test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
)

# Test session
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db():
    """Create test database tables and drop them after tests."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield TestSessionLocal
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(test_db):
    """Create a fresh database session for each test."""
    async with test_db() as session:
        yield session


@pytest.fixture
async def client(db_session):
    """Create a test client with database dependency override."""
    # Override the get_db dependency
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
async def sample_hero(db_session):
    """Create a sample hero for testing."""
    from app.models.hero import Hero
    
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
    
    db_session.add(hero)
    await db_session.commit()
    await db_session.refresh(hero)
    
    return hero


@pytest.fixture
async def sample_project(db_session):
    """Create a sample project for testing."""
    from app.models.projects import Project
    
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
    
    return project
