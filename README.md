# Lush Moments Backend

A modern, feature-rich FastAPI backend for event management and planning services.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with role-based access control
- 📦 **Package Management** - CRUD operations for event packages
- 🎨 **Theme Gallery** - Manage event themes with image galleries
- 💬 **Real-time Chat** - WebSocket-based chat system for customer support
- 🌍 **Multi-language Support** - Dynamic content translation system
- ⚡ **Redis Caching** - High-performance caching for frequently accessed data
- 📧 **Background Tasks** - Asynchronous email notifications
- 📁 **Media Upload** - File upload and management system
- 📊 **Admin Dashboard** - Comprehensive admin endpoints for content management
- 🗄️ **Async Database** - SQLAlchemy 2.0 with async support (SQLite/PostgreSQL)

## Tech Stack

- **Framework**: FastAPI 0.119+
- **Database**: SQLAlchemy 2.0 (async), aiosqlite/asyncpg
- **Caching**: Redis
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with PBKDF2
- **Package Manager**: uv
- **Migrations**: Alembic

## Project Structure

```
lush-moments-backend/
├── app/
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API endpoints
│   │   ├── admin/       # Admin-only endpoints
│   │   ├── auth.py
│   │   ├── packages.py
│   │   ├── themes.py
│   │   ├── testimonials.py
│   │   ├── bookings.py
│   │   ├── sessions.py
│   │   ├── chat.py
│   │   └── media.py
│   ├── seeders/         # Database seeders
│   ├── utils/           # Utilities
│   │   ├── auth.py      # JWT & password utilities
│   │   ├── cache.py     # Redis caching
│   │   ├── email.py     # Email notifications
│   │   └── translations.py  # Multi-language support
│   ├── database.py      # Database configuration
│   └── main.py          # FastAPI application
├── uploads/             # Media files storage
├── cli.py               # Management CLI
├── CLI.md               # CLI documentation
├── pyproject.toml       # Project dependencies
└── .env                 # Environment variables
```

## Installation

### Prerequisites

- Python 3.12+
- Redis (for caching)
- PostgreSQL (for production) or SQLite (for development)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd lush-moments-backend
```

2. **Install uv** (if not already installed)
```bash
# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Install dependencies**
```bash
uv sync
```

4. **Configure environment variables**
```bash
# Copy .env template and update values
cp .env.example .env
```

Edit `.env` file:
```properties
# Database
DATABASE_URL=sqlite+aiosqlite:///lush_moments.db
# For PostgreSQL: postgresql+asyncpg://user:password@localhost/dbname

# Redis
REDIS_URL=redis://localhost:6379

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Admin credentials
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

5. **Start Redis** (if not running)
```bash
# On Windows with Docker
docker run -d -p 6379:6379 redis:alpine

# Or install and start Redis locally
redis-server
```

6. **Initialize and seed the database**
```bash
# Initialize database tables
uv run python cli.py init-db

# Seed with sample data
uv run python cli.py seed-db

# Create a super admin
uv run python cli.py create-admin
```

7. **Run the application**
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## CLI Management Tool

The project includes a comprehensive command-line interface for managing the application. See [CLI.md](CLI.md) for full documentation.

**Quick commands:**

```bash
# Create admin user
uv run python cli.py create-admin --email "admin@example.com" --name "Admin"

# List all admins
uv run python cli.py list-admins

# Seed database
uv run python cli.py seed-db

# Change user password
uv run python cli.py change-password --email "user@example.com"

# Get help
uv run python cli.py --help
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

## API Endpoints

### Public Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /packages?lang=en` - List packages (with translation support)
- `GET /themes?lang=en` - List themes (with translation support)
- `GET /testimonials` - List testimonials
- `POST /bookings` - Create event booking
- `POST /sessions` - Create chat session
- `WS /ws/chat/{session_id}` - WebSocket chat connection
- `GET /chat/history/{session_id}` - Get chat history
- `GET /media/files/{filename}` - Get uploaded file

### Admin Endpoints (Requires Authentication)

All admin endpoints require a valid JWT token with admin role.

**Packages**
- `GET /admin/packages` - List all packages
- `POST /admin/packages` - Create package
- `GET /admin/packages/{id}` - Get package details
- `PUT /admin/packages/{id}` - Update package
- `DELETE /admin/packages/{id}` - Delete package

**Themes**
- `GET /admin/themes` - List all themes
- `POST /admin/themes` - Create theme
- `GET /admin/themes/{id}` - Get theme details
- `PUT /admin/themes/{id}` - Update theme
- `DELETE /admin/themes/{id}` - Delete theme

**Testimonials**
- `GET /admin/testimonials` - List all testimonials
- `POST /admin/testimonials` - Create testimonial
- `GET /admin/testimonials/{id}` - Get testimonial details
- `PUT /admin/testimonials/{id}` - Update testimonial
- `DELETE /admin/testimonials/{id}` - Delete testimonial

**Bookings**
- `GET /admin/bookings` - List all bookings
- `POST /admin/bookings` - Create booking
- `GET /admin/bookings/{id}` - Get booking details
- `PUT /admin/bookings/{id}` - Update booking
- `DELETE /admin/bookings/{id}` - Delete booking

**Sessions**
- `GET /admin/sessions` - List all chat sessions
- `POST /admin/sessions` - Create session
- `GET /admin/sessions/{id}` - Get session details
- `PUT /admin/sessions/{id}` - Update session
- `DELETE /admin/sessions/{id}` - Delete session

**Translations**
- `GET /admin/translations` - List all translations
- `POST /admin/translations` - Create translation
- `GET /admin/translations/{id}` - Get translation details
- `PUT /admin/translations/{id}` - Update translation
- `DELETE /admin/translations/{id}` - Delete translation

**Media**
- `POST /media/upload` - Upload single file
- `POST /media/upload-multiple` - Upload multiple files
- `DELETE /media/files/{filename}` - Delete file

## Authentication

To access admin endpoints:

1. **Login to get JWT token**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

2. **Use token in Authorization header**
```bash
curl -X GET "http://127.0.0.1:8000/admin/packages" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## WebSocket Chat

Connect to WebSocket endpoint for real-time chat:

```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/YOUR_SESSION_ID');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.send(JSON.stringify({
  message: 'Hello from client!'
}));
```

## Multi-language Support

Add translations via admin endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/admin/translations" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "Package",
    "object_id": 1,
    "language_code": "es",
    "field_name": "name",
    "translated_text": "Paquete Básico"
  }'
```

Access translated content:
```bash
curl "http://127.0.0.1:8000/packages?lang=es"
```

## Caching

The application uses Redis for caching:

- Package lists are cached for 10 minutes
- Cache is automatically invalidated when data is modified via admin endpoints
- Manual cache clearing available through Redis commands

## Background Tasks

Background tasks are used for:

- Sending booking confirmation emails
- Sending admin notifications
- Processing chat responses (extensible for AI integration)

## Database Migrations

Using Alembic for database migrations:

```bash
# Generate migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback
uv run alembic downgrade -1
```

## Development

### Running Tests
```bash
uv run pytest
```

### Code Formatting
```bash
uv run black app/
uv run isort app/
```

### Type Checking
```bash
uv run mypy app/
```

## Production Deployment

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependencies
COPY pyproject.toml .
RUN uv sync

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: lush_moments
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db/lush_moments
      REDIS_URL: redis://redis:6379
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

### Environment Variables for Production

Update `.env` for production:
- Use strong `SECRET_KEY`
- Configure production database URL
- Set up proper email service credentials
- Configure domain and CORS settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License

## Support

For support and questions, contact: support@lushmoments.com

---

Built with ❤️ using FastAPI