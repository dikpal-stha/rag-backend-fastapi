import sqlite3
from typing import List, Dict

DB_PATH = "metadata.db"

# Initialize database and table
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS file_metadata(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            chunk_index INTEGER,
            text_preview TEXT,
            qdrant_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Insert metadata
def insert_metadata(metadata: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for idx, meta in enumerate(metadata):
        c.execute('''
        INSERT INTO file_metadata (filename, chunk_index, text_preview, qdrant_id)
        VALUES (?, ?, ?, ?)
        ''', (meta["filename"], meta["chunk_index"], meta["text_preview"], idx))

    conn.commit()
    conn.close()


