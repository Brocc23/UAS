import sqlite3
from datetime import datetime
from cafe_app.database import DB_PATH

class PaymentModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def create_transaction(self, meja_id, metode_pembayaran):
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute(
            "INSERT INTO transaksi (tanggal, total, metode_pembayaran, meja_id, status) VALUES (?, ?, ?, ?, ?)",
            (tanggal, 0, metode_pembayaran, meja_id, "pending")
        )
        self.conn.commit()
        return self.cur.lastrowid

    def add_detail(self, transaksi_id, menu_id, jumlah, harga, diskon=0):
        subtotal = (harga * jumlah) - diskon
        self.cur.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, subtotal, diskon) VALUES (?, ?, ?, ?, ?)",
            (transaksi_id, menu_id, jumlah, subtotal, diskon)
        )
        self.conn.commit()
        self.update_total(transaksi_id)

    def update_total(self, transaksi_id):
        self.cur.execute(
            "SELECT SUM(subtotal) as total FROM detail_transaksi WHERE transaksi_id=?",
            (transaksi_id,)
        )
        total = self.cur.fetchone()["total"] or 0
        self.cur.execute(
            "UPDATE transaksi SET total=? WHERE id=?",
            (total, transaksi_id)
        )
        self.conn.commit()

    def set_paid(self, transaksi_id):
        self.cur.execute(
            "UPDATE transaksi SET status='paid' WHERE id=?",
            (transaksi_id,)
        )
        self.conn.commit()

    def get_transaction(self, transaksi_id):
        self.cur.execute(
            "SELECT * FROM transaksi WHERE id=?",
            (transaksi_id,)
        )
        return self.cur.fetchone()

    def get_details(self, transaksi_id):
        self.cur.execute(
            "SELECT * FROM detail_transaksi WHERE transaksi_id=?",
            (transaksi_id,)
        )
        return self.cur.fetchall()

    def list_transactions(self):
        self.cur.execute("SELECT * FROM transaksi ORDER BY id DESC")
        return self.cur.fetchall()
