import sqlite3, os
from cafe_app.database import DB_PATH

print("DB PATH =", DB_PATH)
print("EXISTS =", os.path.exists(DB_PATH))
