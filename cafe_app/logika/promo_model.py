import sqlite3
from cafe_app.database import DB_PATH

class PromoModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def all(self):
        self.cur.execute("SELECT * FROM promo ORDER BY id DESC")
        return self.cur.fetchall()

    def get(self, promo_id):
        self.cur.execute("SELECT * FROM promo WHERE id=?", (promo_id,))
        return self.cur.fetchone()

    def get_by_code(self, code):
        self.cur.execute("SELECT * FROM promo WHERE code=?", (code,))
        return self.cur.fetchone()

    def create(self, code, jenis, value, target="transaksi", aktif=1):
        self.cur.execute(
            "INSERT INTO promo (code, jenis, value, target, aktif) VALUES (?, ?, ?, ?, ?)",
            (code, jenis, value, target, aktif)
        )
        self.conn.commit()
        return self.cur.lastrowid

    def update(self, promo_id, code, jenis, value, target, aktif):
        self.cur.execute(
            "UPDATE promo SET code=?, jenis=?, value=?, target=?, aktif=? WHERE id=?",
            (code, jenis, value, target, aktif, promo_id)
        )
        self.conn.commit()
        return True

    def delete(self, promo_id):
        self.cur.execute("DELETE FROM promo WHERE id=?", (promo_id,))
        self.conn.commit()
        return True

    def apply_promo(self, code, subtotal):
        promo = self.get_by_code(code)
        if not promo or promo["aktif"] == 0:
            return subtotal, 0

        if promo["jenis"] == "persen":
            diskon = subtotal * (promo["value"] / 100)
        else:
            diskon = promo["value"]

        if diskon > subtotal:
            diskon = subtotal

        total = subtotal - diskon
        return total, diskon
