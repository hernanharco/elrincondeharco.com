import asyncio
from app.db.seed_site_settings import seed_site_settings


if __name__ == "__main__":
    asyncio.run(seed_site_settings())
