from cafe_app.database import get_db
from datetime import datetime

class OrderModel:
    def create_order(meja_id, user_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transaksi (tanggal, total, metode_pembayaran, meja_id, status) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(), 0, "", meja_id, "pending")
        )
        transaksi_id = cur.lastrowid
        conn.commit()
        conn.close()
        return transaksi_id

    def add_item(transaksi_id, menu_id, jumlah, subtotal, diskon=0):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, subtotal, diskon) VALUES (?, ?, ?, ?, ?)",
            (transaksi_id, menu_id, jumlah, subtotal, diskon)
        )
        conn.commit()
        conn.close()

    def update_item(detail_id, jumlah, subtotal):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE detail_transaksi SET jumlah=?, subtotal=? WHERE id=?",
            (jumlah, subtotal, detail_id)
        )
        conn.commit()
        conn.close()

    def remove_item(detail_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM detail_transaksi WHERE id=?", (detail_id,))
        conn.commit()
        conn.close()

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

    def set_order_status(transaksi_id, status):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE transaksi SET status=? WHERE id=?",
            (status, transaksi_id)
        )
        conn.commit()
        conn.close()

    def get_pending_orders():
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, meja_id, total, status FROM transaksi WHERE status='pending'"
        )
        rows = cur.fetchall()
        conn.close()
        return rows
