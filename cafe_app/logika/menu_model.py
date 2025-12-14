import sqlite3
import os
from cafe_app.database import get_connection


class MenuModel:
    def add_menu(self, nama, kategori, harga, stok, foto):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO menu (nama, kategori, harga, stok, foto)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nama, kategori, int(harga), int(stok), foto)
        )
        conn.commit()
        conn.close()

    def update_menu(self, menu_id, nama, kategori, harga, stok, foto):
        conn = get_connection()
        cur = conn.cursor()

        if foto:
            cur.execute(
                """
                UPDATE menu
                SET nama=?, kategori=?, harga=?, stok=?, foto=?
                WHERE id=?
                """,
                (nama, kategori, int(harga), int(stok), foto, menu_id)
            )
        else:
            cur.execute(
                """
                UPDATE menu
                SET nama=?, kategori=?, harga=?, stok=?
                WHERE id=?
                """,
                (nama, kategori, int(harga), int(stok), menu_id)
            )

        conn.commit()
        conn.close()

    def delete_menu(self, menu_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM menu WHERE id=?", (menu_id,))
        conn.commit()
        conn.close()

    def get_all_menu(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, nama, kategori, harga, stok, foto
            FROM menu
            ORDER BY nama ASC
            """
        )
        rows = cur.fetchall()
        conn.close()
        return rows

    def search_menu(self, keyword="", kategori=None):
        conn = get_connection()
        cur = conn.cursor()

        query = """
            SELECT id, nama, kategori, harga, stok, foto
            FROM menu
            WHERE nama LIKE ?
        """
        params = [f"%{keyword}%"]

        if kategori:
            query += " AND kategori=?"
            params.append(kategori)

        query += " ORDER BY nama ASC"

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        return rows