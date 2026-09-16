"""
UC189 - AI Voice-Based Insurance Quoting Assistant
Main FastAPI application entry point.
"""

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add backend directory to sys.path so modules resolve cleanly when executed from anywhere
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import get_settings
from api.voice_api import router as voice_router
from api.quote_api import router as quote_router
from api.customer_api import router as customer_router
from api.recommendation_api import router as recommendation_router
from database.db import engine, Base, get_db, init_db
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info(f"Starting {settings.APP_NAME} ...")
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    yield
    logger.info("Shutting down application.")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered voice assistant for insurance quoting, comparison, and recommendations.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────
app.include_router(voice_router, prefix="/api/voice", tags=["Voice"])
app.include_router(quote_router, prefix="/api/quotes", tags=["Quotes"])
app.include_router(customer_router, prefix="/api/customers", tags=["Customers"])
app.include_router(recommendation_router, prefix="/api/recommendations", tags=["Recommendations"])


# ── Health Check ────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": "1.0.0",
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "health": "/health",
    }


# ── Uploads & Logs directories ──────────────────────────
os.makedirs(os.path.join(BACKEND_DIR, "uploads"), exist_ok=True)
os.makedirs(os.path.join(BACKEND_DIR, "logs"), exist_ok=True)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
    )
