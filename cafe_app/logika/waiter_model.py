import sqlite3
from cafe_app.database import get_connection

class WaiterModel:
    def get_pending_orders(self):
        conn = get_connection()
        cur = conn.cursor()
        # Fetch orders that are 'pending' (Kitchen/Waiter flow)

        cur.execute("""
            SELECT t.id, tb.nomor, t.status
            FROM transaksi t
            JOIN tables tb ON t.meja_id = tb.id
            WHERE t.status = 'pending'
            ORDER BY t.id ASC
        """)
        rows = cur.fetchall()
        conn.close()
        return rows

    def complete_order(self, trans_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            # Update status to completed
            cur.execute("UPDATE transaksi SET status = 'completed' WHERE id = ?", (trans_id,))
            
            # NOTE: We DO NOT clear the table here anymore. 
            # Waiter must manually clear it in "Status Meja" tab.
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error completing order: {e}")
            return False
        finally:
            conn.close()

    def get_active_tables(self):
        conn = get_connection()
        cur = conn.cursor()
        # Get tables that are occupied ('terisi')
        cur.execute("SELECT id, nomor, status FROM tables WHERE status = 'terisi'")
        rows = cur.fetchall()
        conn.close()
        return rows

    def clear_table(self, table_id):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE tables SET status = 'kosong' WHERE id = ?", (table_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing table: {e}")
            return False
        finally:
            conn.close()
