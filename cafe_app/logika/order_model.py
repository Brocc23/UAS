from cafe_app.database import get_db
from datetime import datetime

class OrderModel:
    def __init__(self):
        self.items = [] 

    def add_item(self, nama, harga, jumlah, menu_id=None):
        for item in self.items:
            if item["nama"] == nama:
                item["jumlah"] += jumlah
                item["subtotal"] = item["jumlah"] * item["harga"]
                return

        self.items.append({
            "nama": nama,
            "menu_id": menu_id,
            "harga": harga,
            "jumlah": jumlah,
            "subtotal": harga * jumlah
        })

    def remove_item(self, nama):
        self.items = [item for item in self.items if item["nama"] != nama]

    def get_total(self):
        return sum(item["subtotal"] for item in self.items)

    def reset(self):
        self.items = []

    @staticmethod
    def create_order(meja_id, metode_pembayaran="", status="pending"):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transaksi (tanggal, total, metode_pembayaran, meja_id, status) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(), 0, metode_pembayaran, meja_id, status)
        )
        transaksi_id = cur.lastrowid
        conn.commit()
        conn.close()
        return transaksi_id

    @staticmethod
    def add_item_db(transaksi_id, menu_id, jumlah, subtotal, diskon=0):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, subtotal, diskon) VALUES (?, ?, ?, ?, ?)",
            (transaksi_id, menu_id, jumlah, subtotal, diskon)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_order_items(transaksi_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT d.id, m.nama, m.harga, d.jumlah, d.subtotal, d.diskon, m.id as menu_id "
            "FROM detail_transaksi d JOIN menu m ON d.menu_id = m.id "
            "WHERE d.transaksi_id=?",
            (transaksi_id,)
        )
        items = cur.fetchall()
        conn.close()
        return items

    @staticmethod
    def update_total(transaksi_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT SUM(subtotal - diskon) FROM detail_transaksi WHERE transaksi_id=?",
            (transaksi_id,)
        )
        total = cur.fetchone()[0] or 0
        cur.execute(
            "UPDATE transaksi SET total=? WHERE id=?",
            (total, transaksi_id)
        )
        conn.commit()
        conn.close()
        return total

    @staticmethod
    def set_order_status(transaksi_id, status):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE transaksi SET status=? WHERE id=?",
            (status, transaksi_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_pending_orders():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, meja_id, total, status FROM transaksi WHERE status='pending'")
        rows = cur.fetchall()
        conn.close()
        return rows
