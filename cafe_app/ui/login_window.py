import tkinter as tk
from tkinter import ttk
from cafe_app.auth import login
from cafe_app.utils import show_error
from cafe_app.ui.admin_window import AdminWindow
from cafe_app.ui.kasir_window import KasirWindow
from cafe_app.ui.waiter_window import WaiterWindow
from cafe_app.ui.pembeli_window import PembeliWindow
from cafe_app.ui.owner_window import OwnerWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Username").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.frame, text="Password").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(self.frame, text="Login", command=self.do_login).grid(row=2, column=0, columnspan=2, pady=10)

    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login(username, password)
        if not user:
            show_error("Username atau password salah")
            return

        # user = (id, username, role)
        user = {
            "id": user[0],
            "username": user[1],
            "role": user[2]
        }

        role = user["role"]

        if role == "admin":
            AdminWindow(self.root, user)
        elif role == "kasir":
            KasirWindow(self.root, user)
        elif role == "waiter":
            WaiterWindow(self.root, user)
        elif role == "pembeli":
            PembeliWindow(self.root, user)
        elif role == "owner":
            OwnerWindow(self.root, user)
        else:
            show_error("Role tidak dikenal")

        self.frame.destroy()

