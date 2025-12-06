import sqlite3
import os
from cafe_app.database import init_db


print("Memastikan database dan tabel telah dibuat...")
init_db()
print("Struktur database siap.")


conn = init_db()
cur = conn.cursor()

users = [
    ("admin", "admin123", "admin"),
    ("kasir", "kasir123", "kasir"),
    ("waiter", "waiter123", "waiter"),
    ("owner", "owner123", "owner"), 
    ("pembeli", "pembeli123", "pembeli")
]

print("\nMemasukkan data pengguna contoh...")
for username, password, role in users:
    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role)
        )
        print(f"  - User '{username}' berhasil ditambahkan.")
    except sqlite3.IntegrityError:
        print(f"  - User '{username}' sudah ada (diabaikan).")
        pass


DUMMY_URL = "https://example.com/images/"

menu_items = [
    ("Espresso", "Minuman Kopi", 15000, 20, DUMMY_URL + "espresso.png"),
    ("Cappuccino", "Minuman Kopi", 20000, 15, DUMMY_URL + "cappuccino.png"),
    ("Croissant", "Makanan Ringan", 12000, 10, DUMMY_URL + "croissant.png"),
    ("Nasi Goreng", "Makanan Berat", 35000, 18, DUMMY_URL + "nasigoreng.png"),
    ("Air Mineral", "Minuman Non-Kopi", 5000, 50, DUMMY_URL + "airmineral.png")
]

print("\nMemasukkan data menu contoh (dengan URL)...")
for nama, kategori, harga, stok, foto in menu_items:
    try:
        cur.execute(
            "INSERT INTO menu (nama, kategori, harga, stok, foto) VALUES (?, ?, ?, ?, ?)", (nama, kategori, harga, stok, foto)
        )
        print(f"  - Menu '{nama}' berhasil ditambahkan (URL: {foto}).")
    except sqlite3.IntegrityError:
        print(f"  - Menu '{nama}' sudah ada (diabaikan).")
        pass

tables = [
    (1, "available"),
    (2, "available"),
    (3, "occupied"),
    (4, "available"),
    (5, "available")
]

print("\nMemasukkan data meja contoh...")
for nomor, status in tables:
    try:
        cur.execute(
            "INSERT INTO tables (nomor, status) VALUES (?, ?)",
            (nomor, status)
        )
        print(f"  - Meja No. {nomor} berhasil ditambahkan.")
    except sqlite3.IntegrityError:
        print(f"  - Meja No. {nomor} sudah ada (diabaikan).")
        pass
        
conn.commit()
conn.close()

print("\n=======================================================")
print("✅ Database berhasil dibuat dan diisi user + menu contoh.")
print("Kolom FOTO diisi dengan URL dummy.")
print("=======================================================")
print("Membuat database...")
init_db()
print("Selesai!")