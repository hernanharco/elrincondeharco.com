from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Importamos los modelos aquí para que se registren en el objeto Base
# Asegúrate de que la ruta coincida con tus archivos reales
try:
    from app.models.example import Example  # noqa: F401
    from app.models.hero import Hero  # noqa: F401
    from app.models.about import About  # noqa: F401
    from app.models.passions import Passion  # noqa: F401
    from app.models.projects import Project  # noqa: F401
    from app.models.stack import Stack  # noqa: F401
    from app.models.footer import Footer  # noqa: F401
    from app.models.showroom import Showroom  # noqa: F401
    from app.models.site_settings import SiteSettings  # noqa: F401
    from app.models.sector import Sector  # noqa: F401
    from app.models.testimonial import Testimonial  # noqa: F401
    from app.models.experience import ExperienceSection  # noqa: F401
except ImportError:
    pass
