from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Importamos los modelos aquí para que se registren en el objeto Base
# Asegúrate de que la ruta coincida con tus archivos reales
try:
    from app.models.example import Example
    from app.models.hero import Hero
    from app.models.about import About
    from app.models.passions import Passion
    from app.models.projects import Project
    from app.models.stack import Stack
    from app.models.footer import Footer
    from app.models.showroom import Showroom
    from app.models.site_settings import SiteSettings
except ImportError:
    pass
