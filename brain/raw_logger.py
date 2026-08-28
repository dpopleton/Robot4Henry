import os
import sqlite3
import uuid
from datetime import datetime
from config.settings import DB_PATH


class RawLogger:
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()
        self.current_session_id = None

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS raw_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                started_at TIMESTAMP NOT NULL,
                ended_at TIMESTAMP,
                processed INTEGER DEFAULT 0,
                compressed_log TEXT
            )
        """)
        self.conn.commit()

    def start_session(self) -> str:
        self.current_session_id = str(uuid.uuid4())
        self.conn.execute("""
            INSERT INTO sessions (session_id, started_at)
            VALUES (?, ?)
        """, (self.current_session_id, datetime.now().isoformat()))
        self.conn.commit()
        return self.current_session_id

    def log(self, role: str, content: str):
        """Log every message verbatim during conversation."""
        if not self.current_session_id:
            self.start_session()

        self.conn.execute("""
            INSERT INTO raw_conversations
                (session_id, role, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (self.current_session_id, role, content,
              datetime.now().isoformat()))
        self.conn.commit()

    def end_session(self):
        """Mark session as ended, ready for rest process."""
        if not self.current_session_id:
            return
        self.conn.execute("""
            UPDATE sessions SET ended_at = ?
            WHERE session_id = ?
        """, (datetime.now().isoformat(), self.current_session_id))
        self.conn.commit()
        self.current_session_id = None

    def get_unprocessed_sessions(self) -> list:
        """Called by rest process to find sessions needing processing."""
        rows = self.conn.execute("""
            SELECT session_id FROM sessions
            WHERE processed = 0
            AND ended_at IS NOT NULL
        """).fetchall()
        return [row[0] for row in rows]

    def get_session_messages(self, session_id: str) -> list:
        rows = self.conn.execute("""
            SELECT role, content, timestamp
            FROM raw_conversations
            WHERE session_id = ?
            ORDER BY timestamp ASC
        """, (session_id,)).fetchall()
        return [
            {"role": r[0], "content": r[1], "timestamp": r[2]}
            for r in rows
        ]

    def mark_processed(self, session_id: str, compressed_log: str):
        """
        Called by rest process after long term memory is built.
        Stores compressed version for debugging, removes raw messages.
        """
        self.conn.execute("""
            UPDATE sessions
            SET processed = 1, compressed_log = ?
            WHERE session_id = ?
        """, (compressed_log, session_id))
        self.conn.execute("""
            DELETE FROM raw_conversations WHERE session_id = ?
        """, (session_id,))
        self.conn.commit()