from fastapi import APIRouter
from app.api.v1.endpoints import (
    example,
    hero,
    about,
    passions,
    projects,
    stack,
    footer,
    site_settings,
)

api_router = APIRouter()

api_router.include_router(example.router, prefix="/api/v1/example", tags=["example"])
api_router.include_router(hero.router, prefix="/api/v1/heroes", tags=["heroes"])
api_router.include_router(about.router, prefix="/api/v1/abouts", tags=["abouts"])
api_router.include_router(passions.router, prefix="/api/v1/passions", tags=["passions"])
api_router.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
api_router.include_router(stack.router, prefix="/api/v1/stacks", tags=["stacks"])
api_router.include_router(footer.router, prefix="/api/v1/footers", tags=["footers"])
api_router.include_router(
    site_settings.router, prefix="/api/v1/site-settings", tags=["site-settings"]
)
