from fastapi import APIRouter
from app.api.v1.endpoints import example, hero, about, passions, projects, stack, footer

api_router = APIRouter()

api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(hero.router, prefix="/heroes", tags=["Hero"])
api_router.include_router(about.router, prefix="/abouts", tags=["About"])
api_router.include_router(passions.router, prefix="/passions", tags=["Passions"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(stack.router, prefix="/stacks", tags=["Stack"])
api_router.include_router(footer.router, prefix="/footers", tags=["Footer"])
