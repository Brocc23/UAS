import sqlite3

DB_NAME = "cafe_app.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def get_db():
    conn = connect_db()
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            kategori TEXT,
            harga INTEGER,
            stok INTEGER,
            foto TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            total INTEGER,
            metode_pembayaran TEXT,
            meja_id INTEGER,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaksi_id INTEGER,
            menu_id INTEGER,
            jumlah INTEGER,
            subtotal INTEGER,
            diskon INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomor INTEGER,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
