import sqlite3
import json
from datetime import datetime

DB_PATH = "backend/app.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS imports
                 (id TEXT PRIMARY KEY, filename TEXT, status TEXT, 
                  created_at TIMESTAMP, rows_processed INTEGER, rows_errored INTEGER, errors TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS thresholds
                 (id TEXT PRIMARY KEY, kpi_name TEXT, operator TEXT, value REAL)''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
