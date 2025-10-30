"""
Test script to check database and agent setup
"""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import HumanMessage
from sqlalchemy import select

from app.agents.lush_agent import run_agent
from app.database import AsyncSessionLocal
from app.models import Package, Theme


async def main():
    print("=" * 60)
    print("Lush Moments Agent Test")
    print("=" * 60)

    # Check database
    print("\n1. Checking database...")
    db = AsyncSessionLocal()

    try:
        result = await db.execute(select(Package))
        packages = result.scalars().all()
        print(f"   ✓ Found {len(packages)} packages in database")
        for pkg in packages:
            print(f"     - {pkg.title}: ${pkg.price}")

        result = await db.execute(select(Theme))
        themes = result.scalars().all()
        print(f"   ✓ Found {len(themes)} themes in database")

        # Check API key
        print("\n2. Checking Google API Key...")
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            print(f"   ✓ API Key found: {api_key[:20]}...")
        else:
            print("   ✗ API Key not found!")
            return

        # Test agent
        print("\n3. Testing agent...")
        test_message = "What packages do you offer?"
        print(f"   Query: '{test_message}'")

        response = await run_agent(message=test_message, db_session=db, history=[])

        print(f"\n   Agent Response:")
        print(f"   {response.content}")

        print("\n" + "=" * 60)
        print("✓ Agent test completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
