from collections.abc import Sequence
import sqlite3


DB_PATH = "database.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def execute_script(script: str):
    conn = get_conn()
    try:
        conn.executescript(script)
        conn.commit()
    finally:
        conn.close()


def execute(sql: str, params: dict | Sequence = ()) -> int | None:
    """Execute a command and return the last row id."""
    conn = get_conn()
    try:
        res = conn.execute(sql, params)
        conn.commit()
        rowid = res.lastrowid
    finally:
        conn.close()
    return rowid


def query(sql: str, params: dict | Sequence = ()) -> list:
    """Execute a command and fetch all results."""
    conn = get_conn()
    try:
        res = conn.execute(sql, params).fetchall()
    finally:
        conn.close()
    return res