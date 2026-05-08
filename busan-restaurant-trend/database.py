import sqlite3
from datetime import datetime

DB_PATH = "restaurants.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, address TEXT, district TEXT,
            category TEXT, naver_link TEXT, collected_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT, address TEXT,
            google_rating REAL, google_review_count INTEGER, recorded_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_restaurant(name, address, district, category, naver_link):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM restaurants WHERE name=? AND address=?", (name, address))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO restaurants (name, address, district, category, naver_link, collected_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, address, district, category, naver_link, datetime.now().isoformat()))
        conn.commit()
    conn.close()

def save_review_snapshot(name, address, rating, review_count):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (restaurant_name, address, google_rating, google_review_count, recorded_at)
        VALUES (?, ?, ?, ?, ?)
    """, (name, address, rating, review_count, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_review_history(name, address):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT google_review_count, recorded_at FROM reviews
        WHERE restaurant_name=? AND address=? ORDER BY recorded_at ASC
    """, (name, address))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_restaurants():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, address, district, category FROM restaurants")
    rows = cursor.fetchall()
    conn.close()
    return rows
