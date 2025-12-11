import sqlite3
from cafe_app.database import get_db

class ReportModel:

    def get_report(self, period):
        conn = get_db()
        cur = conn.cursor()

        if period == "Harian":
            query = """
                SELECT tanggal, total, metode, meja_id, status
                FROM transaksi
                WHERE tanggal = date('now')
            """

        elif period == "Mingguan":
            query = """
                SELECT tanggal, total, metode, meja_id, status
                FROM transaksi
                WHERE tanggal >= date('now', '-7 days')
            """

        elif period == "Bulanan":
            query = """
                SELECT tanggal, total, metode, meja_id, status
                FROM transaksi
                WHERE strftime('%Y-%m', tanggal) = strftime('%Y-%m', 'now')
            """

        else:
            return []

        cur.execute(query)
        data = cur.fetchall()
        conn.close()

        return data
