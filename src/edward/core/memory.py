import json
import os
import re
from typing import Dict, List, Optional

import aiosqlite

from edward.core.config import settings

DB_PATH = settings.db_path
_CONN: Optional[aiosqlite.Connection] = None


def _build_fts_query(query: str) -> str:
    """Sanitize and build an FTS5 MATCH query string."""
    words = re.findall(r"\w+", query)
    if not words:
        return '""'
    return " OR ".join(words)


async def init_db(db_path: Optional[str] = None) -> None:
    """Initialize the SQLite database with the messages table."""
    global DB_PATH, _CONN
    if db_path is not None:
        DB_PATH = db_path

    if _CONN is None:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        _CONN = await aiosqlite.connect(DB_PATH)

    await _CONN.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT,
            content TEXT
        )
        """
    )

    # FTS5 Virtual Table for true RAG
    await _CONN.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
            content,
            content='messages',
            content_rowid='id'
        )
        """
    )

    # Triggers to keep FTS table in sync
    await _CONN.execute(
        """
        CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
            INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
        END;
        """
    )

    # Safely rebuild the index for any pre-existing records before FTS5 was added
    await _CONN.execute("INSERT INTO messages_fts(messages_fts) VALUES('rebuild')")

    await _CONN.commit()


async def store_message(role: str, content: str) -> None:
    """Store a message in the database."""
    if _CONN is None:
        await init_db()

    await _CONN.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content),
    )
    await _CONN.commit()


async def get_context(
    query: Optional[str] = None, limit: int = 10
) -> List[Dict[str, str]]:
    """Retrieve the most recent messages."""
    if _CONN is None:
        await init_db()

    if query:
        fts_query = _build_fts_query(query)
        if fts_query == '""':
            return []

        sql = """
            SELECT m.role, m.content 
            FROM messages m
            JOIN messages_fts fts ON m.id = fts.rowid
            WHERE messages_fts MATCH ?
            ORDER BY fts.rank
            LIMIT ?
        """
        params = [fts_query, limit]
    else:
        sql = "SELECT role, content FROM messages ORDER BY timestamp DESC, id DESC LIMIT ?"
        params = [limit]

    cursor = await _CONN.execute(sql, tuple(params))
    rows = await cursor.fetchall()

    messages = [{"role": row[0], "content": row[1]} for row in rows]

    # Reverse only if getting sequential recent history
    if not query:
        messages.reverse()

    return messages


async def export_history(filepath: str = "edward_export.json") -> None:
    """Export the conversation history to a JSON file."""
    if _CONN is None:
        await init_db()

    all_history = await get_context(limit=10000)
    with open(filepath, "w") as f:
        json.dump(all_history, f, indent=2)


async def close_db() -> None:
    """Close the database connection."""
    global _CONN
    if _CONN is not None:
        await _CONN.close()
        _CONN = None
