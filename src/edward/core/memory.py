from typing import Dict, List, Optional

import aiosqlite

DB_PATH = "edward_memory.db"
_CONN: Optional[aiosqlite.Connection] = None


async def init_db(db_path: Optional[str] = None) -> None:
    """Initialize the SQLite database with the messages table."""
    global DB_PATH, _CONN
    if db_path is not None:
        DB_PATH = db_path

    if _CONN is None:
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

    sql = "SELECT role, content FROM messages"
    params = []

    if query:
        sql += " WHERE content LIKE ?"
        params.append(f"%{query}%")

    sql += " ORDER BY timestamp DESC, id DESC LIMIT ?"
    params.append(limit)

    cursor = await _CONN.execute(sql, tuple(params))
    rows = await cursor.fetchall()

    # Reverse to get chronological order for context
    messages = [{"role": row[0], "content": row[1]} for row in rows]
    messages.reverse()
    return messages


async def close_db() -> None:
    """Close the database connection."""
    global _CONN
    if _CONN is not None:
        await _CONN.close()
        _CONN = None
