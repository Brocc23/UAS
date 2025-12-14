import tkinter as tk
from tkinter import ttk
from cafe_app.auth import login
from cafe_app.utils import show_error, show_info
from cafe_app.logika.user_model import UserModel
from cafe_app.ui.admin_window import AdminWindow
from cafe_app.ui.kasir_window import KasirWindow
from cafe_app.ui.waiter_window import WaiterWindow
from cafe_app.ui.pembeli_window import PembeliWindow
from cafe_app.ui.owner_window import OwnerWindow


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.mode = "login"

        self.root.title("Login - Café App")
        self.root.geometry("380x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Title.TLabel", font=("Poppins", 16, "bold"))
        style.configure("Form.TFrame", background="#f5f6fa")
        style.configure("TButton", padding=6)

        self.frame = ttk.Frame(root, style="Form.TFrame")
        self.frame.pack(expand=True)

        self.title_label = ttk.Label(
            self.frame,
            text="Café App Login",
            style="Title.TLabel"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        ttk.Label(self.frame, text="Username").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(self.frame, width=28)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.frame, text="Password").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*", width=28)
        self.password_entry.grid(row=2, column=1, pady=5)

        self.action_button = ttk.Button(
            self.frame,
            text="Login",
            command=self.submit_action,
            width=20
        )
        self.action_button.grid(row=3, column=0, columnspan=2, pady=(15, 5))

        self.switch_button = ttk.Button(
            self.frame,
            text="Daftar sebagai Pembeli",
            command=self.switch_mode,
            width=20
        )
        self.switch_button.grid(row=4, column=0, columnspan=2)

    def switch_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.title_label.config(text="Register Pembeli")
            self.action_button.config(text="Register")
            self.switch_button.config(text="Kembali ke Login")
        else:
            self.mode = "login"
            self.title_label.config(text="Café App Login")
            self.action_button.config(text="Login")
            self.switch_button.config(text="Daftar sebagai Pembeli")

    def submit_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            show_error("Username dan password wajib diisi")
            return

        if self.mode == "login":
            self.do_login(username, password)
        else:
            self.do_register(username, password)

    def do_login(self, username, password):
        user = login(username, password)
        if not user:
            show_error("Username atau password salah")
            return

        user_data = {
            "id": user[0],
            "username": user[1],
            "role": user[2]
        }

        self.open_role_window(user_data)

    def do_register(self, username, password):
        success = UserModel().register(username, password, "pembeli")
        if not success:
            show_error("Username sudah digunakan")
            return

        show_info("Registrasi berhasil")
        user = login(username, password)

        user_data = {
            "id": user[0],
            "username": user[1],
            "role": user[2]
        }

        self.open_role_window(user_data)

    def open_role_window(self, user):
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
            return

        self.frame.destroy()
