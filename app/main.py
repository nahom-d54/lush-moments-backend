from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routes.admin.bookings import router as admin_bookings_router
from app.routes.admin.contact import router as admin_contact_router
from app.routes.admin.contact_info import router as admin_contact_info_router
from app.routes.admin.dashboard import router as admin_dashboard_router
from app.routes.admin.enhancements import router as admin_enhancements_router
from app.routes.admin.faqs import router as admin_faqs_router
from app.routes.admin.gallery import router as admin_gallery_router
from app.routes.admin.packages import router as admin_packages_router
from app.routes.admin.sessions import router as admin_sessions_router
from app.routes.admin.testimonials import router as admin_testimonials_router
from app.routes.admin.themes import router as admin_themes_router
from app.routes.admin.translations import router as admin_translations_router
from app.routes.auth import router as auth_router
from app.routes.bookings import router as bookings_router
from app.routes.chat import router as chat_router
from app.routes.contact import router as contact_router
from app.routes.contact_info import router as contact_info_router
from app.routes.enhancements import router as enhancements_router
from app.routes.faqs import router as faqs_router
from app.routes.gallery import router as gallery_router
from app.routes.packages import router as packages_router
from app.routes.sessions import router as sessions_router
from app.routes.testimonials import router as testimonials_router
from app.routes.themes import router as themes_router
from app.utils.cache import close_redis, get_redis
from app.utils.image_processing import ensure_upload_directories


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create upload directories
    ensure_upload_directories()
    print("✓ Upload directories initialized")
    # Initialize Redis connection
    try:
        await get_redis()
        print("✓ Redis connection established")
    except Exception as e:
        print(f"⚠ Redis connection failed: {e}")

    yield

    # Cleanup
    await close_redis()
    print("✓ Closed Redis connection")


app = FastAPI(
    title="Lush Moments Backend",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT == "development" else None,
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS Configuration - Allow frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Public routes
app.include_router(packages_router)
app.include_router(auth_router)
app.include_router(themes_router)
app.include_router(testimonials_router)
app.include_router(bookings_router)
app.include_router(sessions_router)
app.include_router(chat_router)
app.include_router(contact_router)
app.include_router(contact_info_router)
app.include_router(gallery_router)
app.include_router(faqs_router)
app.include_router(faqs_router)
app.include_router(enhancements_router)

# Admin routes
app.include_router(admin_dashboard_router)
app.include_router(admin_packages_router)
app.include_router(admin_themes_router)
app.include_router(admin_testimonials_router)
app.include_router(admin_bookings_router)
app.include_router(admin_sessions_router)
app.include_router(admin_translations_router)
app.include_router(admin_contact_router)
app.include_router(admin_gallery_router)
app.include_router(admin_contact_info_router)
app.include_router(admin_faqs_router)
app.include_router(admin_enhancements_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Lush Moments Backend"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Check database
    db_status = "ok"
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check Redis
    redis_status = "ok"
    try:
        redis = await get_redis()
        await redis.ping()
    except Exception as e:
        redis_status = f"error: {str(e)}"

    return {
        "status": "healthy"
        if db_status == "ok" and redis_status == "ok"
        else "degraded",
        "database": db_status,
        "redis": redis_status,
        "version": "0.1.0",
    }
