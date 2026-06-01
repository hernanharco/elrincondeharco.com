from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    company,
    example,
    hero,
    about,
    passions,
    projects,
    stack,
    footer,
    site_settings,
    showroom,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(hero.router, prefix="/heroes", tags=["heroes"])
api_router.include_router(about.router, prefix="/abouts", tags=["abouts"])
api_router.include_router(passions.router, prefix="/passions", tags=["passions"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(stack.router, prefix="/stacks", tags=["stacks"])
api_router.include_router(footer.router, prefix="/footers", tags=["footers"])
api_router.include_router(showroom.router, prefix="/showrooms", tags=["showrooms"])
api_router.include_router(
    site_settings.router, prefix="/site-settings", tags=["site-settings"]
)
