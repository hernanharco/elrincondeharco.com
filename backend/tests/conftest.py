import os
import pytest
import asyncio
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.models.base import Base
from app.db.session import get_db


def _build_test_database_url() -> str:
    """Build the test database URL.

    Priority:
    1. TEST_DATABASE_URL env var (explicit, clean URL)
    2. Derived from settings.database_url with /{db} → /test_{db}
       and the ``options=`` query parameter stripped (D1).
    """
    env_url = os.environ.get("TEST_DATABASE_URL")
    if env_url:
        return env_url

    # Fallback: derive from production URL, strip options= (search_path)
    raw = settings.database_url
    parsed = urlparse(raw)

    # Replace database name: /dbname → /test_dbname
    path = parsed.path
    db_name = path.lstrip("/")
    new_path = f"/test_{db_name}"

    # Strip 'options' from query string (keeps sslmode etc.)
    qs = dict(parse_qsl(parsed.query))
    qs.pop("options", None)
    clean_query = urlencode(qs)

    return urlunparse(parsed._replace(path=new_path, query=clean_query))


# Test database URL — clean, no options= search_path override
TEST_DATABASE_URL = _build_test_database_url()

# Admin URL for CREATE DATABASE (connects to default 'postgres' DB)
_admin_parsed = urlparse(TEST_DATABASE_URL)
ADMIN_DATABASE_URL = urlunparse(_admin_parsed._replace(path="/postgres"))

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
    """Create test database tables and drop them after tests.

    Uses an admin connection to CREATE DATABASE IF NOT EXISTS (REQ-TESTDB),
    then guards Base.metadata.schema = None so create_all targets the
    default 'public' schema in the isolated test DB (D2).
    """
    test_db_name = _admin_parsed.path.lstrip("/")

    # 1. Ensure the test database exists via admin connection
    admin_engine = create_async_engine(ADMIN_DATABASE_URL, echo=False)
    try:
        async with admin_engine.connect() as conn:
            result = await conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'")
            )
            db_exists = result.scalar() is not None
            if not db_exists:
                # Must close transaction before CREATE DATABASE
                await conn.execute(text("COMMIT"))
                await conn.execute(text(f'CREATE DATABASE "{test_db_name}"'))
    finally:
        await admin_engine.dispose()

    # 2. Guard: lifespan sets Base.metadata.schema = <prod_schema>,
    #    but lifespan doesn't run in tests. Force None so create_all
    #    targets 'public' in the isolated test DB (D2).
    original_schema = Base.metadata.schema
    original_table_schemas = {}
    for table in Base.metadata.tables.values():
        original_table_schemas[table.name] = table.schema
        table.schema = None
    Base.metadata.schema = None

    try:
        # Create tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield TestSessionLocal

        # Drop tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    finally:
        # Restore original schema setting
        Base.metadata.schema = original_schema
        for table in Base.metadata.tables.values():
            table.schema = original_table_schemas.get(table.name)


@pytest.fixture
async def db_session(test_db):
    """Create a fresh database session for each test."""
    async with test_db() as session:
        yield session
        # Rollback any uncommitted changes and clean up
        await session.rollback()
        # Clean all tables after each test
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


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
        color="from-test-500/20",
    )

    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)

    return project


@pytest.fixture
async def sample_site_settings(db_session):
    """Create sample site settings for testing."""
    from app.models.site_settings import SiteSettings

    settings = SiteSettings(
        brand_name="Test Brand",
        site_url="https://test.com",
        legal_name="Test Legal",
        slogan="Test Slogan",
        copyright_notice="© Test",
        contact_email="test@test.com",
        social_networks={},
        is_active=True,
    )

    db_session.add(settings)
    await db_session.commit()
    await db_session.refresh(settings)

    return settings


@pytest.fixture
async def sample_experience(db_session):
    """Create a sample experience section for testing."""
    from app.models.experience import ExperienceSection

    exp = ExperienceSection(
        tagline="Test Experience",
        title="Test <span>Title</span>",
        description="Test description",
    )

    db_session.add(exp)
    await db_session.commit()
    await db_session.refresh(exp)

    return exp
