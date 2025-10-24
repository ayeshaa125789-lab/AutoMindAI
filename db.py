import sqlite3
import os

DB_FILE = "automind.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msg_id TEXT,
                sender TEXT,
                subject TEXT,
                date TEXT,
                summary TEXT,
                category TEXT,
                sentiment TEXT,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
