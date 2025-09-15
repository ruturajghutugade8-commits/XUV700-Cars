import sqlite3  # Import necessary libraries
from werkzeug.security import generate_password_hash  # Import necessary libraries
import os  # Import necessary libraries

DB_PATH = os.path.join(os.path.dirname(__file__), "bookings.db")

def get_conn():  # Function: get_conn
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():  # Function: init_db
    # create tables if not exists and insert default admin if none
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        car_model TEXT,
        start_date TEXT,
        end_date TEXT,
        price TEXT,
        notes TEXT,
        payment_method TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()

    # Insert default admin if doesn't exist
    cur.execute("SELECT COUNT(*) as cnt FROM admins")
    row = cur.fetchone()
    if row and row["cnt"] == 0:
        # default admin credentials (from your JS)
        default_username = "rmsruturaj"
        default_password = "nad@3118"
        hashed = generate_password_hash(default_password)
        cur.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (default_username, hashed))
        conn.commit()
    conn.close()

def add_booking(booking):  # Function: add_booking
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (name, email, phone, car_model, start_date, end_date, price, notes, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        booking.get("name"),
        booking.get("email"),
        booking.get("phone"),
        booking.get("car_model"),
        booking.get("start_date"),
        booking.get("end_date"),
        booking.get("price"),
        booking.get("notes"),
        booking.get("payment_method")
    ))
    conn.commit()
    id = cur.lastrowid
    conn.close()
    return id

def get_bookings():  # Function: get_bookings
    conn = get_conn()
    rows = conn.execute("SELECT * FROM bookings ORDER BY created_at DESC").fetchall()
    conn.close()
    return rows

def get_booking(booking_id):  # Function: get_booking
    conn = get_conn()
    row = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
    conn.close()
    return row

def delete_booking(booking_id):  # Function: delete_booking
    conn = get_conn()
    conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

def clear_bookings():  # Function: clear_bookings
    conn = get_conn()
    conn.execute("DELETE FROM bookings")
    conn.commit()
    conn.close()

def get_admin_by_username(username):  # Function: get_admin_by_username
    conn = get_conn()
    row = conn.execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()
    conn.close()
    return row