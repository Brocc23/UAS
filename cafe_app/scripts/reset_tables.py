import sys
import os
import sqlite3

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from cafe_app.database import get_connection

def reset_tables():
    conn = get_connection()
    cur = conn.cursor()
    
    print("Resetting all tables to 'kosong'...")
    cur.execute("UPDATE tables SET status = 'kosong'")
    
    # Optional: Clear pending transactions to start fresh? 
    # User said "mejanya g konek... coba refresh dulu semua data di database buat mejanya"
    # I'll just reset tables.
    
    conn.commit()
    conn.close()
    print("Tables reset successfully.")

if __name__ == "__main__":
    reset_tables()
