import tkinter as tk
from tkinter import ttk
from cafe_app.utils import show_info, show_error
from cafe_app.ui.style_utils import COLORS, FONTS, setup_global_styles, create_card, create_button

class WaiterWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        username = "Unknown"
        if isinstance(user, dict): username = user.get("username", "Unknown")
        elif isinstance(user, list) or isinstance(user, tuple): username = user[1]

        self.window = tk.Toplevel(root)
        self.window.title(f"Waiter Panel - {username}")
        self.window.state("zoomed")
        self.window.configure(bg=COLORS["bg"])
        
        setup_global_styles()

        # ===== Container utama (Center) =====
        container = tk.Frame(self.window, bg=COLORS["bg"])
        container.pack(fill="both", expand=True, padx=40, pady=40)

        # ===== Header in Card =====
        header_card = create_card(container, padding=15)
        header_card.pack(fill="x", pady=(0, 20))

        tk.Label(
            header_card,
            text="WAITER PANEL",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack(side="left")

        tk.Label(
            header_card,
            text=f"Logged in as: {username}",
            font=FONTS["body"],
            bg=COLORS["card"],
            fg=COLORS["text_grey"]
        ).pack(side="right", pady=10)

        # ===== Content Card =====
        content_card = create_card(container)
        content_card.pack(fill="both", expand=True)

        tk.Label(
            content_card,
            text="Daftar Pesanan Menunggu",
            font=FONTS["h2"],
            bg=COLORS["card"],
            fg=COLORS["text_dark"]
        ).pack(anchor="w", pady=(0, 15))

        # ===== Table Pesanan =====
        tree_frame = tk.Frame(content_card, bg="white")
        tree_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "meja", "status"),
            show="headings",
            height=12,
            yscrollcommand=scrollbar.set,
            style="Treeview"
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("id", text="ID PESANAN")
        self.tree.heading("meja", text="NOMOR MEJA")
        self.tree.heading("status", text="STATUS")

        self.tree.column("id", width=120, anchor="center")
        self.tree.column("meja", width=100, anchor="center")
        self.tree.column("status", width=200, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        # ===== Tombol aksi =====
        btn_frame = tk.Frame(content_card, bg=COLORS["card"])
        btn_frame.pack(fill="x", pady=20)

        create_button(
            btn_frame, 
            "TANDAI SUDAH DIANTAR", 
            self.set_delivered, 
            "success"
        ).pack(fill="x")

        self.load_pending_orders()

    def load_pending_orders(self):
        orders = [
            {"id": 101, "meja": 3, "status": "Menunggu Diantar"},
            {"id": 102, "meja": 5, "status": "Menunggu Diantar"},
            {"id": 105, "meja": 2, "status": "Siap Disajikan"},
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

        show_info(f"Pesanan {order_id} berhasil diantar ke meja!")
        self.tree.delete(selected)
