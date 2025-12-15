import sys
import os
import sqlite3

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from cafe_app.database import get_connection
from cafe_app.logika.waiter_model import WaiterModel

def test_waiter():
    conn = get_connection()
    cur = conn.cursor()
    
    print("--- DEBUG WAITER ---")
    # 1. Manually set Table 1 to 'terisi'
    print("Setting Table 1 to 'terisi'...")
    cur.execute("UPDATE tables SET status='terisi' WHERE id=1")
    conn.commit()
    
    # 2. Fetch using WaiterModel
    print("Fetching active tables via WaiterModel...")
    wm = WaiterModel()
    tables = wm.get_active_tables()
    print(f"Result: {tables}")
    
    if len(tables) > 0 and tables[0][1] == 1:
        print("SUCCESS: WaiterModel can see occupied tables.")
    else:
        print("FAILURE: WaiterModel returned empty list or wrong data.")
        
    conn.close()

if __name__ == "__main__":
    test_waiter()
