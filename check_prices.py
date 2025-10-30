import asyncio

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Package


async def main():
    db = AsyncSessionLocal()
    try:
        result = await db.execute(select(Package).order_by(Package.price))
        pkgs = result.scalars().all()
        print("Packages in DB:")
        for p in pkgs:
            print(f"  {p.title}: ${p.price} (type: {type(p.price).__name__})")
    finally:
        await db.close()


asyncio.run(main())
