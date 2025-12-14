import tkinter as tk
from tkinter import ttk
from cafe_app.utils import show_info, show_error


class WaiterWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        username = None
        try:
            username = user.get("username")
        except Exception:
            try:
                username = user[1]
            except Exception:
                username = "Unknown"

        self.window = tk.Toplevel(root)
        self.window.title("Waiter Panel")
        self.window.geometry("650x480")
        self.window.resizable(False, False)

        # ===== Container utama =====
        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        # ===== Header =====
        ttk.Label(
            container,
            text="Waiter Panel",
            font=("Poppins", 18, "bold")
        ).pack(pady=(0, 5))

        ttk.Label(
            container,
            text=f"Login sebagai: {username}",
            font=("Poppins", 11),
            foreground="gray"
        ).pack(pady=(0, 10))

        ttk.Separator(container).pack(fill="x", pady=10)

        # ===== Table Pesanan =====
        table_frame = ttk.Frame(container)
        table_frame.pack(fill="both", expand=True)

        ttk.Label(
            table_frame,
            text="Daftar Pesanan Menunggu",
            font=("Poppins", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "meja", "status"),
            show="headings",
            height=12
        )

        self.tree.heading("id", text="ID Pesanan")
        self.tree.heading("meja", text="Meja")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=120, anchor="center")
        self.tree.column("meja", width=100, anchor="center")
        self.tree.column("status", width=200, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ===== Tombol aksi =====
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=15)

        ttk.Button(
            btn_frame,
            text="Tandai Sudah Diantar",
            command=self.set_delivered
        ).pack(fill="x")

        self.load_pending_orders()

    def load_pending_orders(self):
        orders = [
            {"id": 101, "meja": 3, "status": "Menunggu Diantar"},
            {"id": 102, "meja": 5, "status": "Menunggu Diantar"},
        ]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for order in orders:
            self.tree.insert(
                "",
                "end",
                values=(order["id"], order["meja"], order["status"])
            )

    def set_delivered(self):
        selected = self.tree.focus()
        if not selected:
            show_error("Pilih pesanan terlebih dahulu!")
            return

        values = self.tree.item(selected, "values")
        order_id = values[0]

        show_info(f"Pesanan {order_id} sudah diantar!")
        self.tree.delete(selected)
