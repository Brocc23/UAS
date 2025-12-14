import sqlite3
from cafe_app.database import get_db


class UserModel:

    def get_user_by_username(self, username: str):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password, role FROM users WHERE username=?",
            (username,)
        )
        user = cur.fetchone()
        conn.close()
        return user

    def register(self, username: str, password: str, role: str):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_all_users(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, role FROM users")
        users = cur.fetchall()
        conn.close()
        return users

    def delete_user(self, user_id: int):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

    def update_user(self, user_id: int, new_username: str, new_role: str):
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET username=?, role=? WHERE id=?",
            (new_username, new_role, user_id)
        )
        conn.commit()
        conn.close()
