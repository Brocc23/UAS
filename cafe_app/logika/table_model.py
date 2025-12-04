import sqlite3
from cafe_app.database import DB_NAME

class ReportModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def penjualan_harian(self, tanggal):
        self.cur.execute("""
            SELECT * FROM transaksi
            WHERE DATE(tanggal) = DATE(?)
            AND status = 'paid'
            ORDER BY tanggal DESC
        """, (tanggal,))
        return self.cur.fetchall()

    def total_harian(self, tanggal):
        self.cur.execute("""
            SELECT SUM(total) AS total FROM transaksi
            WHERE DATE(tanggal) = DATE(?)
            AND status = 'paid'
        """, (tanggal,))
        row = self.cur.fetchone()
        return row["total"] or 0

    def penjualan_periode(self, tgl_awal, tgl_akhir):
        self.cur.execute("""
            SELECT * FROM transaksi
            WHERE DATE(tanggal) BETWEEN DATE(?) AND DATE(?)
            AND status='paid'
            ORDER BY tanggal DESC
        """, (tgl_awal, tgl_akhir))
        return self.cur.fetchall()

    def total_periode(self, tgl_awal, tgl_akhir):
        self.cur.execute("""
            SELECT SUM(total) AS total FROM transaksi
            WHERE DATE(tanggal) BETWEEN DATE(?) AND DATE(?)
            AND status='paid'
        """, (tgl_awal, tgl_akhir))
        row = self.cur.fetchone()
        return row["total"] or 0

    def menu_terlaris(self, tgl_awal=None, tgl_akhir=None):
        if tgl_awal and tgl_akhir:
            self.cur.execute("""
                SELECT m.nama, SUM(d.jumlah) AS total_jumlah
                FROM detail_transaksi d
                JOIN transaksi t ON d.transaksi_id=t.id
                JOIN menu m ON d.menu_id=m.id
                WHERE DATE(t.tanggal) BETWEEN DATE(?) AND DATE(?)
                AND t.status='paid'
                GROUP BY d.menu_id
                ORDER BY total_jumlah DESC
            """, (tgl_awal, tgl_akhir))
        else:
            self.cur.execute("""
                SELECT m.nama, SUM(d.jumlah) AS total_jumlah
                FROM detail_transaksi d
                JOIN transaksi t ON d.transaksi_id=t.id
                JOIN menu m ON d.menu_id=m.id
                WHERE t.status='paid'
                GROUP BY d.menu_id
                ORDER BY total_jumlah DESC
            """)
        return self.cur.fetchall()

    def metode_pembayaran(self, tgl_awal=None, tgl_akhir=None):
        if tgl_awal and tgl_akhir:
            self.cur.execute("""
                SELECT metode_pembayaran, COUNT(*) AS jumlah, SUM(total) AS nominal
                FROM transaksi
                WHERE status='paid'
                AND DATE(tanggal) BETWEEN DATE(?) AND DATE(?)
                GROUP BY metode_pembayaran
            """, (tgl_awal, tgl_akhir))
        else:
            self.cur.execute("""
                SELECT metode_pembayaran, COUNT(*) AS jumlah, SUM(total) AS nominal
                FROM transaksi
                WHERE status='paid'
                GROUP BY metode_pembayaran
            """)
        return self.cur.fetchall()
