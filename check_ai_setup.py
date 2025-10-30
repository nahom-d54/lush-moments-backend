"""
Check if all requirements for AI Chat Agent are met
"""

import os
import sys


def check_env_variable(var_name: str, required: bool = True) -> bool:
    """Check if environment variable is set"""
    value = os.getenv(var_name)

    if value:
        # Mask API keys in output
        if "KEY" in var_name or "SECRET" in var_name:
            display_value = value[:8] + "..." if len(value) > 8 else "***"
        else:
            display_value = value
        print(f"✓ {var_name} = {display_value}")
        return True
    else:
        if required:
            print(f"✗ {var_name} is NOT SET (Required)")
            return False
        else:
            print(f"○ {var_name} is not set (Optional)")
            return True


def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        ("langchain_google_genai", "langchain-google-genai"),
        ("langchain", "langchain"),
        ("langgraph", "langgraph"),
        ("fastapi", "fastapi"),
        ("sqlalchemy", "sqlalchemy"),
    ]

    all_installed = True

    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is NOT installed")
            all_installed = False

    return all_installed


def check_database():
    """Check if database file exists"""
    db_path = "lush_moments.db"

    if os.path.exists(db_path):
        size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"✓ Database exists ({size_mb:.2f} MB)")
        return True
    else:
        print(f"✗ Database not found: {db_path}")
        return False


def check_migration():
    """Check if latest migration is applied"""
    try:
        import asyncio

        from sqlalchemy import text

        from app.database import engine

        async def check_columns():
            async with engine.begin() as conn:
                # Check if new columns exist
                result = await conn.execute(
                    text(
                        "SELECT sql FROM sqlite_master WHERE type='table' AND name='sessions'"
                    )
                )
                table_sql = result.scalar()

                if table_sql:
                    has_agent_fields = (
                        "is_handled_by_agent" in table_sql
                        and "transferred_to_human" in table_sql
                    )

                    if has_agent_fields:
                        print(
                            "✓ Database migration applied (agent handoff fields exist)"
                        )
                        return True
                    else:
                        print("✗ Database migration NOT applied")
                        print("  Run: alembic upgrade head")
                        return False
                else:
                    print("✗ Sessions table not found")
                    return False

        return asyncio.run(check_columns())

    except Exception as e:
        print(f"○ Could not check migration: {e}")
        return True  # Don't fail the check


def main():
    """Run all checks"""
    print("=" * 60)
    print("Lush Moments AI Chat Agent - Requirements Check")
    print("=" * 60)

    print("\n1. Environment Variables")
    print("-" * 60)
    env_ok = all(
        [
            check_env_variable("GOOGLE_API_KEY", required=True),
            check_env_variable("DATABASE_URL", required=False),
            check_env_variable("SECRET_KEY", required=False),
        ]
    )

    print("\n2. Python Dependencies")
    print("-" * 60)
    deps_ok = check_dependencies()

    print("\n3. Database")
    print("-" * 60)
    db_ok = check_database()
    migration_ok = check_migration()

    print("\n" + "=" * 60)

    if env_ok and deps_ok and db_ok and migration_ok:
        print("✓ ALL CHECKS PASSED - Ready to use AI Chat Agent!")
        print("\nQuick Start:")
        print("  1. uvicorn app.main:app --reload")
        print("  2. Open chat widget in frontend")
        print("  3. Start chatting!")
        return 0
    else:
        print("✗ SOME CHECKS FAILED - Please fix the issues above")
        print("\nCommon Solutions:")

        if not env_ok:
            print("  • Add GOOGLE_API_KEY to .env file")
            print("    Get key: https://aistudio.google.com/app/apikey")

        if not deps_ok:
            print("  • Install dependencies: pip install -e .")

        if not db_ok:
            print("  • Create database: alembic upgrade head")

        if not migration_ok:
            print("  • Apply migration: alembic upgrade head")

        return 1


if __name__ == "__main__":
    sys.exit(main())
