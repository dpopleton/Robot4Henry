import os
import sqlite3
import threading
from datetime import datetime
from config.settings import DB_PATH


class KeyFactsStore:
    def __init__(self, db_path: str = DB_PATH):
        self._lock = threading.RLock()
        with self._lock:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS key_facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def set(self, key: str, value: str):
        with self._lock:
            self.conn.execute("""
                INSERT OR REPLACE INTO key_facts (key, value, updated_at)
                VALUES (?, ?, ?)
            """, (key, value, datetime.now().isoformat()))
            self.conn.commit()

    def get(self, key: str) -> str | None:
        with self._lock:
            row = self.conn.execute(
                "SELECT value FROM key_facts WHERE key = ?", (key,)
            ).fetchone()
            return row[0] if row else None

    def delete(self, key: str):
        with self._lock:
            self.conn.execute(
                "DELETE FROM key_facts WHERE key = ?", (key,)
            )
            self.conn.commit()

    def get_all(self) -> dict:
        with self._lock:
            rows = self.conn.execute(
                "SELECT key, value FROM key_facts ORDER BY updated_at DESC"
            ).fetchall()
            return {row[0]: row[1] for row in rows}

    def format_for_prompt(self) -> str:
        facts = self.get_all()
        if not facts:
            return ""
        lines = [f"  - {k}: {v}" for k, v in facts.items()]
        return "KEY FACTS ABOUT THE USER:\n" + "\n".join(lines)

    def clear(self):
        with self._lock:
            self.conn.execute("DELETE FROM key_facts")
            self.conn.commit()

    def close(self):
        with self._lock:
            if self.conn:
                self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
