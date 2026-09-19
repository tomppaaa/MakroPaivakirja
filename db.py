import sqlite3
from flask import g


def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def ensure_meals_schema():
    con = get_connection()
    columns = con.execute("PRAGMA table_info(meals)").fetchall()
    existing = {row[1] for row in columns}
    if "diet_tags" not in existing:
        con.execute("ALTER TABLE meals ADD COLUMN diet_tags TEXT DEFAULT ''")
        con.commit()
    con.close()


def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()


def last_insert_id():
    return g.last_insert_id


def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result