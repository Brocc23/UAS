import sqlite3
from cafe_app.database import get_db

class ReportModel:

    def get_report(self, period):
        conn = get_db()
        cur = conn.cursor()

        if period == "Harian":
            query = """
                SELECT 
                    t.tanggal,
                    SUM(dt.subtotal) AS total_pendapatan,
                    t.metode_pembayaran,
                    t.meja_id,
                    t.status
                FROM transaksi t
                JOIN detail_transaksi dt ON t.id = dt.transaksi_id
                WHERE DATE(t.tanggal) = DATE('now')
                GROUP BY t.id
            """

        elif period == "Mingguan":
            query = """
                SELECT 
                    t.tanggal,
                    SUM(dt.subtotal) AS total_pendapatan,
                    t.metode_pembayaran,
                    t.meja_id,
                    t.status
                FROM transaksi t
                JOIN detail_transaksi dt ON t.id = dt.transaksi_id
                WHERE DATE(t.tanggal) >= DATE('now', '-7 days')
                GROUP BY t.id
            """

        elif period == "Bulanan":
            query = """
                SELECT 
                    t.tanggal,
                    SUM(dt.subtotal) AS total_pendapatan,
                    t.metode_pembayaran,
                    t.meja_id,
                    t.status
                FROM transaksi t
                JOIN detail_transaksi dt ON t.id = dt.transaksi_id
                WHERE strftime('%Y-%m', t.tanggal) = strftime('%Y-%m', 'now')
                GROUP BY t.id
            """

        else:
            conn.close()
            return []

        cur.execute(query)
        data = cur.fetchall()
        conn.close()

        return data
