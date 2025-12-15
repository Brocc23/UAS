import sys
import os
import random
import datetime
import sqlite3

# Add parent directory to path to import cafe_app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from cafe_app.database import get_connection

def generate_fake_data():
    conn = get_connection()
    cur = conn.cursor()

    # Get Menu Items
    cur.execute("SELECT id, harga FROM menu")
    menu_items = cur.fetchall() # [(id, harga), ...]
    
    if not menu_items:
        print("Menu is empty! Please populate menu first.")
        return

    # Date range: 3 months ago to yesterday
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=90)
    
    print(f"Generating data from {start_date} to {end_date}...")

    transactions = []
    details = []
    
    current_date = start_date
    while current_date < end_date:
        # Random number of transactions per day (e.g., 5 to 20)
        daily_transactions = random.randint(5, 20)
        
        for _ in range(daily_transactions):
            # Time logic (mostly lunch and dinner)
            hour = random.choice(list(range(11, 14)) + list(range(17, 21)))
            minute = random.randint(0, 59)
            trans_date = datetime.datetime.combine(current_date, datetime.time(hour, minute))
            trans_date_str = trans_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Random items
            num_items = random.randint(1, 4)
            selected_items = random.choices(menu_items, k=num_items)
            
            total_trans = 0
            temp_details = []
            
            for m_id, harga in selected_items:
                qty = random.randint(1, 2)
                subtotal = harga * qty
                total_trans += subtotal
                temp_details.append((m_id, qty, subtotal))
            
            # Insert Transaction
            cur.execute("""
                INSERT INTO transaksi (tanggal, total, metode_pembayaran, meja_id, status)
                VALUES (?, ?, ?, ?, ?)
            """, (trans_date_str, total_trans, random.choice(['cash', 'qris']), random.randint(1, 10), 'completed'))
            
            trans_id = cur.lastrowid
            
            # Insert Details
            for m_id, qty, sub in temp_details:
                details.append((trans_id, m_id, qty, sub))

        current_date += datetime.timedelta(days=1)

    # Bulk insert details
    cur.executemany("""
        INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, subtotal, diskon)
        VALUES (?, ?, ?, ?, 0)
    """, details)

    conn.commit()
    conn.close()
    print("Fake data generation complete!")

if __name__ == "__main__":
    generate_fake_data()
