from cafe_app.database import get_db

def get_user_by_username(username: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password, role FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    return user

def create_user(username: str, password: str, role: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role)
    )
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()
    conn.close()
    return users

def delete_user(user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def update_user_role(user_id: int, new_role: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role=? WHERE id=?", (new_role, user_id))
    conn.commit()
    conn.close()
