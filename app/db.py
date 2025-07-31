import sqlite3
import json
from pathlib import Path

DB_PATH = Path('database/forms.db')
DB_PATH.parent.mkdir(exist_ok=True)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS completed_forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    form_json TEXT NOT NULL
)
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(CREATE_TABLE_SQL)
    return conn

def save_form(template_name: str, timestamp: str, data: dict):
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO completed_forms (template_name, timestamp, form_json) VALUES (?, ?, ?)",
            (template_name, timestamp, json.dumps(data)),
        )
    conn.close()

def list_forms():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, template_name, timestamp FROM completed_forms ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return rows

def get_form(form_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT template_name, timestamp, form_json FROM completed_forms WHERE id=?",
        (form_id,),
    ).fetchone()
    conn.close()
    if row:
        template_name, timestamp, form_json = row
        return {
            "template_name": template_name,
            "timestamp": timestamp,
            "data": json.loads(form_json),
        }
    return None

def update_form(form_id: int, template_name: str, timestamp: str, data: dict):
    """Update an existing form record."""
    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE completed_forms SET template_name=?, timestamp=?, form_json=? WHERE id=?",
            (template_name, timestamp, json.dumps(data), form_id),
        )
    conn.close()
