# Quick Start Guide

Get the Lush Moments Backend up and running in minutes!

## Prerequisites

- Python 3.12 or higher
- Redis (optional, for caching)
- PostgreSQL (optional, SQLite used by default)

## Installation

### 1. Install uv (Python package manager)

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd lush-moments-backend

# Install dependencies
uv sync

# Copy environment variables
cp .env.example .env
# Edit .env and update SECRET_KEY and other settings
```

### 3. Initialize Database

```bash
# Option A: Using CLI (Recommended)
uv run python cli.py init-db
uv run python cli.py seed-db

# Option B: Using seeder directly
uv run python -m app.seeders.seed
```

### 4. Create Admin User

```bash
# Interactive mode
uv run python cli.py create-admin

# Or with options
uv run python cli.py create-admin \
  --email "admin@lushmoments.com" \
  --name "Admin User" \
  --password "SecurePassword123"
```

### 5. Start the Server

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

### 6. Access API Documentation

Open your browser and visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Test the API

### 1. Login as Admin

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@lushmoments.com",
    "password": "Admin@123"
  }'
```

**Note:** If you seeded the database, use the credentials from the seeder:
- Email: `admin@lushmoments.com`
- Password: `Admin@123`

You'll receive a response with an access token:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Test Public Endpoints

Get packages:
```bash
curl "http://127.0.0.1:8000/packages"
```

Get themes:
```bash
curl "http://127.0.0.1:8000/themes"
```

Get packages in Spanish:
```bash
curl "http://127.0.0.1:8000/packages?lang=es"
```

### 3. Test Admin Endpoints

Replace `YOUR_TOKEN` with the token from step 1:

```bash
curl -X GET "http://127.0.0.1:8000/admin/packages" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Create a new package:
```bash
curl -X POST "http://127.0.0.1:8000/admin/packages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Package",
    "description": "A custom event package",
    "price": 1500.0,
    "included_items": "Venue, Catering, DJ"
  }'
```

## Optional: Setup Redis (for caching)

### Using Docker:

```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

### On Windows:

1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Install and start Redis service

### On macOS:

```bash
brew install redis
brew services start redis
```

### On Linux:

```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

## Development Workflow

### View All Users

```bash
uv run python cli.py list-users
```

### Create Additional Admins

```bash
uv run python cli.py create-admin
```

### Change User Password

```bash
uv run python cli.py change-password --email "user@example.com"
```

### Reset Database

```bash
# This will clear all data and reseed
uv run python cli.py seed-db --clear
```

## Common Issues

### Port 8000 Already in Use

```bash
# Use a different port
uv run uvicorn app.main:app --reload --port 8001
```

### Database Locked (SQLite)

Stop any running instances of the application and try again.

### Redis Connection Failed

The app will work without Redis, but caching will be disabled. Start Redis to enable caching:
```bash
docker run -d -p 6379:6379 redis:alpine
```

### Import Errors

Make sure dependencies are installed:
```bash
uv sync
```

## Next Steps

1. **Customize Environment**: Edit `.env` file with your settings
2. **Add Sample Data**: Customize `app/seeders/seed.py` with your data
3. **Deploy**: See [README.md](README.md) for deployment instructions
4. **API Integration**: Use the API documentation at `/docs` to integrate with frontend
5. **WebSocket Chat**: Test real-time chat at `/ws/chat/{session_id}`

## Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Use strong admin passwords
- [ ] Switch to PostgreSQL database
- [ ] Enable Redis for caching
- [ ] Configure proper email service
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS for your frontend domain
- [ ] Set up backup strategy
- [ ] Configure logging and monitoring
- [ ] Review and update security settings

## Support

For detailed documentation:
- [README.md](README.md) - Full project documentation
- [CLI.md](CLI.md) - CLI command reference
- API Docs - http://127.0.0.1:8000/docs (when running)

For issues and questions:
- Check existing issues on GitHub
- Create a new issue with detailed description
- Include error messages and system information

---

**Happy coding! 🎉**