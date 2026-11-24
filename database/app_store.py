"""Small persistent key/value store for application state.

Local runs use SQLite. Vercel deployments must provide DATABASE_URL for a
shared PostgreSQL database so users, opportunities, sessions and audit logs
survive serverless cold starts.
"""
import json
import os
import sqlite3
import threading
from pathlib import Path


class AppStore:
    def __init__(self):
        self._lock = threading.RLock()
        self.database_url = os.environ.get("DATABASE_URL", "").strip()
        self._postgres = self.database_url.startswith(("postgres://", "postgresql://"))
        if self.database_url and not self._postgres:
            raise RuntimeError("DATABASE_URL must use the postgres:// or postgresql:// scheme.")
        if os.environ.get("VERCEL") and not self.database_url:
            raise RuntimeError("Vercel deployment requires DATABASE_URL for persistent PostgreSQL storage.")
        if self._postgres:
            try:
                import psycopg
            except ImportError as exc:
                raise RuntimeError("Install psycopg[binary] to use DATABASE_URL.") from exc
            self._psycopg = psycopg
            with self._connect() as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )
        else:
            default_path = Path(__file__).resolve().parent / "minhan_app.sqlite3"
            self.path = Path(os.environ.get("APP_DB_PATH", str(default_path))).expanduser()
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )

    def _connect(self):
        if self._postgres:
            return self._psycopg.connect(self.database_url)
        conn = sqlite3.connect(str(self.path), timeout=30)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")
        return conn

    def get(self, key, default=None):
        with self._lock, self._connect() as conn:
            placeholder = "%s" if self._postgres else "?"
            row = conn.execute(f"SELECT value FROM app_state WHERE key = {placeholder}", (key,)).fetchone()
        if row is None:
            return default
        try:
            return json.loads(row[0])
        except (TypeError, json.JSONDecodeError):
            return default

    def set(self, key, value):
        encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        with self._lock, self._connect() as conn:
            if self._postgres:
                conn.execute(
                    "INSERT INTO app_state(key, value) VALUES (%s, %s) "
                    "ON CONFLICT(key) DO UPDATE SET value = EXCLUDED.value",
                    (key, encoded),
                )
            else:
                conn.execute(
                    "INSERT INTO app_state(key, value) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                    (key, encoded),
                )

