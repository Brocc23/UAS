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
        self.root.title("Login - Café App")
        self.root.geometry("380x260")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")

        # ===== STYLE (UI ONLY) =====
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Title.TLabel", font=("Poppins", 16, "bold"))
        style.configure("Form.TFrame", background="#f5f6fa")
        style.configure("TButton", padding=6)

        self.frame = ttk.Frame(root, style="Form.TFrame")
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Café App Login", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        ttk.Label(self.frame, text="Username").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(self.frame, width=28)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame, text="Password").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*", width=28)
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Button(
            self.frame,
            text="Login",
            command=self.do_login,
            width=20
        ).grid(row=3, column=0, columnspan=2, pady=15)

    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login(username, password)
        if not user:
            show_error("Username atau password salah")
            return

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