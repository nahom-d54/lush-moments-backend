"""
Initialize AI Chat Agent - One-command setup
This script helps set up the AI chat agent quickly
"""

import os
import subprocess
import sys


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_step(step_num, total, text):
    """Print a step indicator"""
    print(f"\n[{step_num}/{total}] {text}")
    print("-" * 70)


def check_command_exists(command):
    """Check if a command exists"""
    try:
        subprocess.run([command, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_command(command, description):
    """Run a command and show output"""
    print(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


def check_env_file():
    """Check and create .env file"""
    if not os.path.exists(".env"):
        print("❌ .env file not found!")

        # Create from template
        env_template = """# Lush Moments Backend Configuration

# Google Gemini AI (REQUIRED for chat agent)
GOOGLE_API_KEY=your-google-gemini-api-key-here

# Application
APP_NAME=Lush Moments
DEBUG=False

# Database
DATABASE_URL=sqlite+aiosqlite:///lush_moments.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Optional: Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Optional: SMTP
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=noreply@lushmoments.com

# Business Contact
ADMIN_EMAIL=admin@lushmoments.com
BUSINESS_PHONE=+1-555-LUSH
"""

        with open(".env", "w") as f:
            f.write(env_template)

        print("✅ Created .env file from template")
        print("⚠️  IMPORTANT: Add your GOOGLE_API_KEY to .env")
        print("   Get it from: https://aistudio.google.com/app/apikey")
        return False
    else:
        # Check if GOOGLE_API_KEY is set
        from dotenv import load_dotenv

        load_dotenv()

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or "your-google" in api_key:
            print("⚠️  GOOGLE_API_KEY not configured in .env")
            print("   Get it from: https://aistudio.google.com/app/apikey")
            return False
        else:
            print("✅ .env file exists and GOOGLE_API_KEY is set")
            return True


def main():
    """Main setup routine"""
    print_header("Lush Moments AI Chat Agent - Automated Setup")

    total_steps = 5

    # Step 1: Check environment
    print_step(1, total_steps, "Checking environment")

    if not os.path.exists("pyproject.toml"):
        print("❌ Not in backend directory! Please run from lush-moments-backend/")
        return 1

    print("✅ In correct directory")

    # Check for Python
    if not check_command_exists("python"):
        print("❌ Python not found! Please install Python 3.12+")
        return 1

    print("✅ Python found")

    # Step 2: Check .env
    print_step(2, total_steps, "Checking .env configuration")

    env_ok = check_env_file()
    if not env_ok:
        print("\n⚠️  Please configure .env file and run this script again")
        return 1

    # Step 3: Install dependencies
    print_step(3, total_steps, "Installing dependencies")

    venv_pip = ".venv/Scripts/pip.exe" if os.name == "nt" else ".venv/bin/pip"

    if not os.path.exists(venv_pip):
        print("⚠️  Virtual environment not found")
        print("   Please create it first:")
        print("   python -m venv .venv")
        print("   .venv\\Scripts\\activate  # Windows")
        print("   source .venv/bin/activate  # Linux/Mac")
        return 1

    if not run_command(
        [venv_pip, "install", "-e", "."], "Installing project dependencies"
    ):
        print("❌ Failed to install dependencies")
        return 1

    print("✅ Dependencies installed")

    # Step 4: Database migration
    print_step(4, total_steps, "Setting up database")

    venv_alembic = (
        ".venv/Scripts/alembic.exe" if os.name == "nt" else ".venv/bin/alembic"
    )

    if not run_command(
        [venv_alembic, "upgrade", "head"], "Applying database migrations"
    ):
        print("❌ Failed to apply migrations")
        return 1

    print("✅ Database migrations applied")

    # Step 5: Verify setup
    print_step(5, total_steps, "Verifying setup")

    if not run_command(["python", "check_ai_setup.py"], "Running setup verification"):
        print("❌ Setup verification failed")
        return 1

    # Success!
    print_header("🎉 Setup Complete!")

    print("\n✅ All checks passed!")
    print("\n📚 Next Steps:")
    print("\n1. Start the backend:")
    print("   uvicorn app.main:app --reload")
    print("\n2. Start the frontend:")
    print("   cd lush-moments-frontend")
    print("   npm run dev")
    print("\n3. Open the chat widget and start testing!")
    print("\n4. Read the docs:")
    print("   - QUICKSTART_AI_CHAT.md (Quick guide)")
    print("   - AI_AGENT_DOCUMENTATION.md (Full docs)")
    print("   - IMPLEMENTATION_SUMMARY.md (What was built)")

    print("\n💡 Test Questions:")
    print('   "What packages do you offer?"')
    print('   "Show me your decoration themes"')
    print('   "What do customers say about you?"')

    print("\n🚀 Happy chatting!")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
