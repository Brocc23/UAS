import tkinter as tk
from tkinter import ttk
from cafe_app.logika.menu_model import MenuModel
from cafe_app.ui.order_window import OrderWindow


class PembeliWindow:
    def __init__(self, master, user):
        self.root = master
        self.user = user

        # ===== WINDOW =====
        self.window = tk.Toplevel(master)
        self.window.title("Halaman Pembeli")
        self.window.geometry("650x480")
        self.window.resizable(False, False)

        self.menu_model = MenuModel()

        # ===== CONTAINER =====
        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        # ===== TITLE =====
        ttk.Label(
            container,
            text="Daftar Menu",
            font=("Poppins", 18, "bold")
        ).pack(pady=(0, 5))

        ttk.Label(
            container,
            text="Silakan pilih menu untuk dipesan",
            font=("Poppins", 11),
            foreground="gray"
        ).pack(pady=(0, 10))

        ttk.Separator(container).pack(fill="x", pady=10)

        # ===== TABLE =====
        table_frame = ttk.Frame(container)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Nama", "Kategori", "Harga", "Stok"),
            show="headings",
            height=12
        )

        self.tree.heading("Nama", text="Nama Menu")
        self.tree.heading("Kategori", text="Kategori")
        self.tree.heading("Harga", text="Harga")
        self.tree.heading("Stok", text="Stok")

        self.tree.column("Nama", width=200)
        self.tree.column("Kategori", width=130, anchor="center")
        self.tree.column("Harga", width=90, anchor="center")
        self.tree.column("Stok", width=70, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ===== BUTTON =====
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=15)

        ttk.Button(
            btn_frame,
            text="Pesan",
            command=self.buka_order
        ).pack(side="left", expand=True, fill="x", padx=5)

        ttk.Button(
            btn_frame,
            text="Refresh",
            command=self.load_menu
        ).pack(side="left", expand=True, fill="x", padx=5)

        ttk.Button(
            btn_frame,
            text="Logout",
            command=self.window.destroy
        ).pack(side="left", expand=True, fill="x", padx=5)

        self.load_menu()

    def load_menu(self):
        self.tree.delete(*self.tree.get_children())
        data = self.menu_model.get_all_menu()

        for m in data:
            self.tree.insert("", "end", values=(m[1], m[2], m[3], m[4]))

    def buka_order(self):
        OrderWindow(self.window)
