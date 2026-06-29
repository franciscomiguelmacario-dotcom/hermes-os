from pathlib import Path
import sqlite3


class Database:

    def __init__(self, db_path="data/hermes.db"):
        self.db_path = db_path

    def initialize(self):
        Path("data").mkdir(exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT
        )
        """)

        conn.commit()
        conn.close()
