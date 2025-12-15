import sqlite3
from cafe_app.database import get_connection

class VoucherModel:
    def __init__(self):
        pass

    def add_voucher(self, kode, tipe, nilai, kuota):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO vouchers (kode, tipe, nilai, kuota) VALUES (?, ?, ?, ?)",
                (kode, tipe, nilai, kuota)
            )
            conn.commit()
            return True, "Voucher berhasil ditambahkan"
        except sqlite3.IntegrityError:
            return False, "Kode voucher sudah ada"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def get_all_vouchers(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, kode, tipe, nilai, kuota FROM vouchers")
        data = cur.fetchall()
        conn.close()
        return data

    def delete_voucher(self, voucher_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM vouchers WHERE id = ?", (voucher_id,))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            conn.close()

    def validate_voucher(self, kode):
        # Return (is_valid, message, discount_val, discount_type)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, tipe, nilai, kuota FROM vouchers WHERE kode = ?", (kode,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return False, "Kode voucher tidak ditemukan", 0, None
        
        v_id, tipe, nilai, kuota = row
        if kuota == 0:
            return False, "Kuota voucher habis", 0, None
            
        return True, "Voucher valid", nilai, tipe

    def use_voucher(self, kode):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE vouchers SET kuota = kuota - 1 WHERE kode = ? AND kuota > 0", (kode,))
            if cur.rowcount > 0:
                conn.commit()
                return True
            else:
                return False
        except:
            return False
        finally:
            conn.close()
