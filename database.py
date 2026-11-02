import sqlite3

DB_NAME = "expenses.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL
            )
            """
        )


def add_expense(description, amount):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO expenses (description, amount) VALUES (?, ?)",
            (description, amount),
        )
        return {"id": cursor.lastrowid, "description": description, "amount": amount}


def list_expenses():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, description, amount FROM expenses").fetchall()
        return [dict(row) for row in rows]