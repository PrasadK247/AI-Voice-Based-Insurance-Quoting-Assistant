"""
UC189 - Application Configuration
Loads settings from environment variables with sensible defaults.
"""

import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ── App ─────────────────────────────────────────────
    APP_NAME: str = "UC189-AI-Insurance-Advisor"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    APP_HOST: str = "0.0.0.0"
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # ── Database ────────────────────────────────────────
    # Defaults to SQLite for immediate local run, easily configured to Postgres via DATABASE_URL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./insurance_advisor.db"
    )

    # ── Azure OpenAI ────────────────────────────────────
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-ada-002"

    # ── Azure Blob Storage ──────────────────────────────
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_STORAGE_CONTAINER: str = "insurance-docs"

    # ── Uniphore ────────────────────────────────────────
    UNIPHORE_API_KEY: str = ""
    UNIPHORE_API_URL: str = "https://api.uniphore.com/v1"
    UNIPHORE_WORKSPACE_ID: str = ""

    # ── Whisper ─────────────────────────────────────────
    WHISPER_MODEL: str = "base"
    WHISPER_LANGUAGE: str = "en"

    # ── ElevenLabs ──────────────────────────────────────
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_VOICE_ID: str = "default"
    ELEVENLABS_MODEL_ID: str = "eleven_monolingual_v1"

    # ── Redis ───────────────────────────────────────────
    REDIS_URL: Optional[str] = None

    # ── Logging ─────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = [".env", "../.env"]
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
