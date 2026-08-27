import sqlite3

class Database:
    def __init__(self):
        self.path = "./database.db"
        self.table = "checks"

    def add_to_db(self, url, status, http_code, response_time_ms, checked_at):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO checks
            (url, status, http_code, response_time_ms, checked_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (url, status, http_code, response_time_ms, checked_at)
        )
        conn.commit()
        conn.close()

    def read_from_db(self):
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM checks")

            return [dict(row) for row in cursor.fetchall()]