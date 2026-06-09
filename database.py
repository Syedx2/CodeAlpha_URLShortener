"""
Database layer for the URL Shortener.
Dual-mode: uses PostgreSQL when POSTGRES_URL is set (Vercel production),
otherwise falls back to SQLite for local development.
"""

import os
import sqlite3
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

POSTGRES_URL = os.environ.get("POSTGRES_URL") or os.environ.get("DATABASE_URL") or os.environ.get("STORAGE_URL")
USE_POSTGRES = bool(POSTGRES_URL)

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras

# SQLite path (local dev only)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "url_shortener.db")


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------

def _get_pg_connection():
    """Create a PostgreSQL connection."""
    conn = psycopg2.connect(POSTGRES_URL, sslmode="require")
    conn.autocommit = False
    return conn


def _get_sqlite_connection():
    """Create a SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def init_db():
    """Create the urls table if it doesn't exist."""
    if USE_POSTGRES:
        conn = _get_pg_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                short_code VARCHAR(10) UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_short_code ON urls (short_code)
        """)
        conn.commit()
        conn.close()
    else:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_short_code ON urls (short_code)
        """)
        conn.commit()
        conn.close()


# ---------------------------------------------------------------------------
# CRUD Operations
# ---------------------------------------------------------------------------

def save_url(short_code: str, original_url: str) -> bool:
    """
    Save a short code -> original URL mapping.
    Returns True on success, False if the short_code already exists.
    """
    if USE_POSTGRES:
        conn = _get_pg_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO urls (short_code, original_url) VALUES (%s, %s)",
                (short_code, original_url),
            )
            conn.commit()
            return True
        except psycopg2.IntegrityError:
            conn.rollback()
            return False
        finally:
            conn.close()
    else:
        conn = _get_sqlite_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                (short_code, original_url),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()


def get_url(short_code: str) -> str | None:
    """Look up the original URL for a given short code."""
    if USE_POSTGRES:
        conn = _get_pg_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT original_url FROM urls WHERE short_code = %s", (short_code,)
        )
        row = cursor.fetchone()
        conn.close()
        return row["original_url"] if row else None
    else:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT original_url FROM urls WHERE short_code = ?", (short_code,)
        )
        row = cursor.fetchone()
        conn.close()
        return row["original_url"] if row else None


def increment_clicks(short_code: str):
    """Increment the click counter for a short code."""
    if USE_POSTGRES:
        conn = _get_pg_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE short_code = %s",
            (short_code,),
        )
        conn.commit()
        conn.close()
    else:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?",
            (short_code,),
        )
        conn.commit()
        conn.close()


def get_stats(short_code: str) -> dict | None:
    """Return stats for a short code: original URL, click count, creation date."""
    if USE_POSTGRES:
        conn = _get_pg_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT short_code, original_url, click_count, created_at FROM urls WHERE short_code = %s",
            (short_code,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "short_code": row["short_code"],
                "original_url": row["original_url"],
                "click_count": row["click_count"],
                "created_at": str(row["created_at"]),
            }
        return None
    else:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT short_code, original_url, click_count, created_at FROM urls WHERE short_code = ?",
            (short_code,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "short_code": row["short_code"],
                "original_url": row["original_url"],
                "click_count": row["click_count"],
                "created_at": row["created_at"],
            }
        return None


def get_recent_urls(limit: int = 10) -> list[dict]:
    """Return the most recently created short URLs."""
    if USE_POSTGRES:
        conn = _get_pg_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT short_code, original_url, click_count, created_at FROM urls ORDER BY created_at DESC LIMIT %s",
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "short_code": row["short_code"],
                "original_url": row["original_url"],
                "click_count": row["click_count"],
                "created_at": str(row["created_at"]),
            }
            for row in rows
        ]
    else:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT short_code, original_url, click_count, created_at FROM urls ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "short_code": row["short_code"],
                "original_url": row["original_url"],
                "click_count": row["click_count"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]
