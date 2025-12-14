from cafe_app.database import get_db

class MenuModel:

    def get_all_menu(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, nama, kategori, harga, stok, foto FROM menu")
        data = cur.fetchall()
        conn.close()
        return data

    def get_menu_by_id(self, menu_id: int):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nama, kategori, harga, stok, foto FROM menu WHERE id=?",
            (menu_id,)
        )
        data = cur.fetchone()
        conn.close()
        return data

    def add_menu(self, nama: str, kategori: str, harga: int, stok: int, foto: str):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO menu (nama, kategori, harga, stok, foto) VALUES (?, ?, ?, ?, ?)",
            (nama, kategori, harga, stok, foto)
        )
        conn.commit()
        conn.close()

    def update_menu(self, menu_id: int, nama: str, kategori: str, harga: int, stok: int, foto: str):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE menu SET nama=?, kategori=?, harga=?, stok=?, foto=? WHERE id=?",
            (nama, kategori, harga, stok, foto, menu_id)
        )
        conn.commit()
        conn.close()

    def delete_menu(self, menu_id: int):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM menu WHERE id=?", (menu_id,))
        conn.commit()
        conn.close()

    def reduce_stock(self, menu_id: int, jumlah: int):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE menu SET stok = stok - ? WHERE id=? AND stok >= ?",
            (jumlah, menu_id, jumlah)
        )
        success = cur.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def restore_stock(self, menu_id: int, jumlah: int):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE menu SET stok = stok + ? WHERE id=?",
            (jumlah, menu_id)
        )
        conn.commit()
        conn.close()

    def search_menu(self, keyword="", kategori=None):
        conn = get_db()
        cur = conn.cursor()

        query = "SELECT id, nama, kategori, harga, stok, foto FROM menu WHERE nama LIKE ?"
        params = [f"%{keyword}%"]

        if kategori:
            query += " AND kategori=?"
            params.append(kategori)

        cur.execute(query, params)
        data = cur.fetchall()
        conn.close()
        return data
