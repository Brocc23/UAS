import tkinter as tk
from tkinter import ttk
from cafe_app.auth import login
from cafe_app.ui import admin_window
from cafe_app.ui import kasir_window
from cafe_app.ui import waiter_window
from cafe_app.ui import pembeli_window
from cafe_app.ui import owner_window
from cafe_app.utils import show_error

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

        role = user[2]

        if role == "admin":
            AdminWindow(self.root)
        elif role == "kasir":
            KasirWindow(self.root)
        elif role == "waiter":
            WaiterWindow(self.root)
        elif role == "pembeli":
            PembeliWindow(self.root)
        elif role == "owner":
            OwnerWindow(self.root)
        else:
            show_error("Role tidak dikenal")

        self.frame.destroy()
