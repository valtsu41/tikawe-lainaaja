from collections.abc import Sequence
import sqlite3

DB_PATH = "database.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    with open("schema.sql",) as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# Execute a command and return the last row id
def execute(sql: str, params: dict | Sequence = ()) -> int | None:
    conn = get_conn()
    res = conn.execute(sql, params)
    conn.commit()
    rowid = res.lastrowid
    conn.close()
    return rowid


def query(sql: str, params: dict | Sequence = ()) -> list:
    conn = get_conn()
    res = conn.execute(sql, params).fetchall()
    conn.close()
    return res