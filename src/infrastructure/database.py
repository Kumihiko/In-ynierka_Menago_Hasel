import sqlite3

class DatabaseManager:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def initialize_schema(self) -> None:
        cursor = self.connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value BLOB NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                encrypted_password BLOB NOT NULL,
                record_iv BLOB NOT NULL
            )
        """)
        
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def save_config(self, key: str, value: bytes) -> None:
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO config (key, value) 
            VALUES (?, ?) 
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        self.connection.commit()

    def get_config(self, key: str) -> bytes | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row['value'] if row else None

    def add_record(self, title: str, encrypted_password: bytes, record_iv: bytes) -> int:
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO vault (title, encrypted_password, record_iv)
            VALUES (?, ?, ?)
        """, (title, encrypted_password, record_iv))
        self.connection.commit()
        return cursor.lastrowid

    def get_all_records(self) -> list[sqlite3.Row]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, title, encrypted_password, record_iv FROM vault")
        return cursor.fetchall()