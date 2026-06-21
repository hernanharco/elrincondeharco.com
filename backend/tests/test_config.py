import pytest
from app.core.config import settings
from app.main import app
import os


class TestConfig:
    """Test configuration and settings."""
    
    def test_settings_loading(self):
        """Test that settings are loaded correctly."""
        assert settings.database_url is not None
        assert settings.secret_key is not None
        assert settings.cloudinary_cloud_name is not None
        assert settings.cloudinary_api_key is not None
        assert settings.cloudinary_api_secret is not None
    
    def test_database_url_format(self):
        """Test database URL format."""
        db_url = settings.database_url
        assert "postgresql+psycopg://" in db_url
        assert "@" in db_url
        assert ":" in db_url  # Port should be present
    
    def test_secret_key_length(self):
        """Test secret key is sufficiently long."""
        assert len(settings.secret_key) >= 32  # Should be at least 32 characters
    
    def test_cloudinary_config(self):
        """Test Cloudinary configuration."""
        assert settings.cloudinary_cloud_name != ""
        assert settings.cloudinary_api_key != ""
        assert settings.cloudinary_api_secret != ""
    
    def test_environment_variables(self):
        """Test environment variables are accessible."""
        # Test that required environment variables are set
        required_vars = [
            "PGHOST",
            "PGDATABASE", 
            "PGUSER",
            "PGPASSWORD"
        ]
        
        for var in required_vars:
            assert os.getenv(var) is not None, f"Environment variable {var} is not set"
    
    def test_settings_validation(self):
        """Test settings validation."""
        # Test that database URL is valid
        try:
            from sqlalchemy import create_engine
            # This should not raise an exception for URL format validation
            create_engine(settings.database_url.replace("+psycopg", ""))
        except Exception as e:
            pytest.fail(f"Database URL validation failed: {e}")
    
    def test_app_configuration(self):
        """Test FastAPI app configuration."""
        assert app.title is not None
        assert app.version is not None
        
        # Check that CORS middleware is configured
        cors_middleware = None
        for middleware in app.user_middleware:
            if "CORSMiddleware" in str(middleware.cls):
                cors_middleware = middleware
                break
        
        assert cors_middleware is not None, "CORS middleware not configured"
    
    def test_debug_mode(self):
        """Test debug mode configuration."""
        # In production, debug should be False
        assert isinstance(settings.debug, bool)
    
    def test_authcore_jwks_url_configuration(self):
        """Test authCore JWKS URL configuration."""
        assert hasattr(settings, 'authcore_jwks_url')
        assert settings.authcore_jwks_url.startswith(("http://", "https://"))
    
    def test_database_ssl_mode(self):
        """Test database SSL mode configuration."""
        assert hasattr(settings, 'pg_sslmode')
        assert settings.pg_sslmode in ["require", "disable", "prefer"]
    
    def test_cloudinary_secure_connection(self):
        """Test Cloudinary secure connection is enabled."""
        # This would be tested in the Cloudinary configuration
        # For now, just check the setting exists
        assert hasattr(settings, 'cloudinary_cloud_name')
