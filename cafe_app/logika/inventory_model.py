import sqlite3
from cafe_app.database import DB_NAME

class InventoryModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def all(self):
        self.cur.execute("SELECT * FROM inventory ORDER BY id DESC")
        return self.cur.fetchall()

    def get(self, inventory_id):
        self.cur.execute("SELECT * FROM inventory WHERE id=?", (inventory_id,))
        return self.cur.fetchone()

    def create(self, nama_bahan, stok, satuan):
        self.cur.execute(
            "INSERT INTO inventory (nama_bahan, stok, satuan) VALUES (?, ?, ?)",
            (nama_bahan, stok, satuan)
        )
        self.conn.commit()
        return self.cur.lastrowid

    def update(self, inventory_id, nama_bahan, stok, satuan):
        self.cur.execute(
            "UPDATE inventory SET nama_bahan=?, stok=?, satuan=? WHERE id=?",
            (nama_bahan, stok, satuan, inventory_id)
        )
        self.conn.commit()
        return True

    def delete(self, inventory_id):
        self.cur.execute("DELETE FROM inventory WHERE id=?", (inventory_id,))
        self.conn.commit()
        return True

    def reduce_stock(self, inventory_id, jumlah):
        data = self.get(inventory_id)
        if not data:
            return False
        sisa = data["stok"] - jumlah
        if sisa < 0:
            return False
        self.cur.execute("UPDATE inventory SET stok=? WHERE id=?", (sisa, inventory_id))
        self.conn.commit()
        return True

    def check_out_of_stock(self):
        self.cur.execute("SELECT * FROM inventory WHERE stok <= 0")
        return self.cur.fetchall()

    def search(self, keyword):
        self.cur.execute("SELECT * FROM inventory WHERE nama_bahan LIKE ?", (f"%{keyword}%",))
        return self.cur.fetchall()
