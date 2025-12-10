import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cafe_app.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kategori TEXT NOT NULL,
            harga INTEGER NOT NULL,
            stok INTEGER NOT NULL,
            foto TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomor INTEGER UNIQUE NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            total INTEGER NOT NULL,
            metode_pembayaran TEXT NOT NULL,
            meja_id INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaksi_id INTEGER NOT NULL,
            menu_id INTEGER NOT NULL,
            jumlah INTEGER NOT NULL,
            subtotal INTEGER NOT NULL,
            diskon INTEGER DEFAULT 0
        )
    """)

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        default_users = [
            ("admin", "admin123", "admin"),
            ("kasir", "kasir123", "kasir"),
            ("waiter", "waiter123", "waiter"),
            ("pembeli", "pembeli123", "pembeli"),
            ("owner", "owner123", "owner")
        ]
        cur.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            default_users
        )

    cur.execute("SELECT COUNT(*) FROM menu")
    if cur.fetchone()[0] == 0:
        sample_menu = [
            ("Es Teh", "Minuman", 5000, 50, None),
            ("Ayam Geprek", "Makanan", 15000, 30, None),
            ("Kopi Hitam", "Minuman", 7000, 40, None),
        ]
        cur.executemany(
            "INSERT INTO menu (nama, kategori, harga, stok, foto) VALUES (?, ?, ?, ?, ?)",
            sample_menu
        )

    cur.execute("SELECT COUNT(*) FROM tables")
    if cur.fetchone()[0] == 0:
        meja_list = [(1, "kosong"), (2, "kosong"), (3, "kosong")]
        cur.executemany(
            "INSERT INTO tables (nomor, status) VALUES (?, ?)",
            meja_list
        )

    conn.commit()
    conn.close()

def get_menu_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nama, kategori, harga, stok, foto FROM menu")
    data = cur.fetchall()
    conn.close()
    return data

def get_db():
    return get_connection()
