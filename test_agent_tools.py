"""
Test script for new AI agent tools
"""

import asyncio

from sqlalchemy import select

from app.agents.lush_agent import run_agent
from app.database import get_db
from app.models import FAQ, PackageEnhancement


async def test_tools():
    """Test the new FAQ and enhancement tools"""
    print("🧪 Testing AI Agent Tools\n")

    # Get database session
    async for db in get_db():
        # Test 1: Check FAQ data exists
        print("1️⃣ Checking FAQ data...")
        faq_result = await db.execute(select(FAQ))
        faqs = faq_result.scalars().all()
        print(f"   ✓ Found {len(faqs)} FAQs in database\n")

        # Test 2: Check Enhancement data exists
        print("2️⃣ Checking Enhancement data...")
        enh_result = await db.execute(select(PackageEnhancement))
        enhancements = enh_result.scalars().all()
        print(f"   ✓ Found {len(enhancements)} enhancements in database\n")

        # Test 3: Test FAQ search tool
        print("3️⃣ Testing FAQ search tool...")
        print("   Question: 'How do I book?'\n")
        response = await run_agent("How do I book?", db)
        print(f"   Agent Response:\n   {response.content}\n")

        # Test 4: Test package enhancements tool
        print("4️⃣ Testing package enhancements tool...")
        print("   Question: 'What extras can I add to my package?'\n")
        response = await run_agent("What extras can I add to my package?", db)
        print(f"   Agent Response:\n   {response.content}\n")

        # Test 5: Test payment FAQ
        print("5️⃣ Testing payment FAQ...")
        print("   Question: 'What payment methods do you accept?'\n")
        response = await run_agent("What payment methods do you accept?", db)
        print(f"   Agent Response:\n   {response.content}\n")

        # Test 6: Test category filter for enhancements
        print("6️⃣ Testing entertainment enhancements...")
        print("   Question: 'Show me entertainment options'\n")
        response = await run_agent("Show me entertainment options", db)
        print(f"   Agent Response:\n   {response.content}\n")

        print("✅ All tests completed!")
        break


if __name__ == "__main__":
    asyncio.run(test_tools())
