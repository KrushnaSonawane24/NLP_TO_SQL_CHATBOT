from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

Provider = Literal["gemini", "groq"]

DEFAULT_PROVIDER: Provider = "gemini"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash-latest"
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_MEMORY_USER_TURNS = 5
DEFAULT_MAX_SQL_STATEMENTS = 4


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    provider: Provider
    api_key: str
    model: str
    database_url: str
    statement_timeout_ms: int
    max_rows: int
    memory_user_turns: int
    max_sql_statements: int


def load_settings() -> Settings:
    """Load settings with default DATABASE_URL fallback"""
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    groq_key = os.getenv("GROQ_API_KEY", "").strip()

    provider: Provider = DEFAULT_PROVIDER
    api_key = ""
    model = DEFAULT_GEMINI_MODEL

    if gemini_key:
        provider = "gemini"
        api_key = gemini_key
        model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL
    elif groq_key:
        provider = "groq"
        api_key = groq_key
        model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL

    return Settings(
        provider=provider,
        api_key=api_key,
        model=model,
        database_url=os.getenv("DATABASE_URL", "").strip(),
        statement_timeout_ms=_get_int("NL2SQL_STATEMENT_TIMEOUT_MS", 8000),
        max_rows=_get_int("NL2SQL_MAX_ROWS", 200),
        memory_user_turns=_get_int("NL2SQL_MEMORY_USER_TURNS", DEFAULT_MEMORY_USER_TURNS),
        max_sql_statements=_get_int("NL2SQL_MAX_SQL_STATEMENTS", DEFAULT_MAX_SQL_STATEMENTS),
    )


def load_settings_custom() -> Settings:
    """Load settings for CUSTOM flow - uses DATABASE_URL_CUSTOMER"""
    settings = load_settings()
    # Override database_url with customer database
    customer_db_url = os.getenv("DATABASE_URL_CUSTOMER", "").strip()
    if customer_db_url:
        return Settings(
            provider=settings.provider,
            api_key=settings.api_key,
            model=settings.model,
            database_url=customer_db_url,
            statement_timeout_ms=settings.statement_timeout_ms,
            max_rows=settings.max_rows,
            memory_user_turns=settings.memory_user_turns,
            max_sql_statements=settings.max_sql_statements,
        )
    return settings


def load_settings_langchain() -> Settings:
    """Load settings for LANGCHAIN flow - uses DATABASE_URL_GIS (PostGIS)"""
    settings = load_settings()
    # Override database_url with GIS database
    gis_db_url = os.getenv("DATABASE_URL_GIS", "").strip()
    if gis_db_url:
        return Settings(
            provider=settings.provider,
            api_key=settings.api_key,
            model=settings.model,
            database_url=gis_db_url,
            statement_timeout_ms=settings.statement_timeout_ms,
            max_rows=settings.max_rows,
            memory_user_turns=settings.memory_user_turns,
            max_sql_statements=settings.max_sql_statements,
        )
    return settings
