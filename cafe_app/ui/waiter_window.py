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
        ).pack(side="right", pady=10, padx=(0, 10))

        from cafe_app.ui.logout_utils import global_logout
        tk.Button(header_card, text="Log Out", command=lambda: global_logout(self.window, self.root), bg=COLORS["danger"], fg="white", relief="flat", padx=10).pack(side="right", pady=10)

        # ===== Content Card =====
        content_card = create_card(container)
        content_card.pack(fill="both", expand=True)

        # ===== Tabs =====
        self.notebook = ttk.Notebook(content_card)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Tab 1: Pesanan ---
        self.tab_orders = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.tab_orders, text=" Daftar Pesanan ")
        
        self.setup_order_tab()

        # --- Tab 2: Meja ---
        self.tab_tables = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.notebook.add(self.tab_tables, text=" Status Meja ")
        
        self.setup_table_tab()

        # Load initial data
        self.load_pending_orders()
        self.load_active_tables()

    def setup_order_tab(self):
        # Treeview (Existing Logic)
        tree_frame = tk.Frame(self.tab_orders, bg="white")
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview( # Rename if needed, keeping as self.tree for compat
            tree_frame, columns=("id", "meja", "status"), show="headings", 
            yscrollcommand=scrollbar.set, style="Treeview"
        )
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("id", text="ID"); self.tree.column("id", width=80, anchor="center")
        self.tree.heading("meja", text="MEJA"); self.tree.column("meja", width=80, anchor="center")
        self.tree.heading("status", text="STATUS"); self.tree.column("status", width=150, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Buttons
        btn_frame = tk.Frame(self.tab_orders, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=10)
        
        create_button(btn_frame, "REFRESH DATA", self.refresh_all, "warning").pack(side="left", fill="x", expand=True, padx=5)
        create_button(btn_frame, "TANDAI SUDAH DIANTAR", self.set_delivered, "success").pack(side="left", fill="x", expand=True, padx=5)

    def setup_table_tab(self):
        # Table List
        tree_frame = tk.Frame(self.tab_tables, bg="white")
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        self.table_tree = ttk.Treeview(
            tree_frame, columns=("id", "nomor", "status"), show="headings", style="Treeview"
        )
        self.table_tree.heading("id", text="ID"); self.table_tree.column("id", width=50, anchor="center")
        self.table_tree.heading("nomor", text="NOMOR MEJA"); self.table_tree.column("nomor", width=100, anchor="center")
        self.table_tree.heading("status", text="STATUS"); self.table_tree.column("status", width=100, anchor="center")
        self.table_tree.pack(fill="both", expand=True)
        
        # Buttons
        btn_frame = tk.Frame(self.tab_tables, bg=COLORS["bg"])
        btn_frame.pack(fill="x", pady=10)
        
        create_button(btn_frame, "REFRESH DATA", self.refresh_all, "warning").pack(side="left", fill="x", expand=True, padx=5)
        create_button(btn_frame, "KOSONGKAN MEJA (SELESAI)", self.clear_table, "danger").pack(side="left", fill="x", expand=True, padx=5)

    def refresh_all(self):
        self.load_pending_orders()
        self.load_active_tables()

    def load_active_tables(self):
        from cafe_app.logika.waiter_model import WaiterModel
        for i in self.table_tree.get_children(): self.table_tree.delete(i)
        
        tables = WaiterModel().get_active_tables()
        for t in tables:
            self.table_tree.insert("", "end", values=t)

    def clear_table(self):
        selected = self.table_tree.focus()
        if not selected:
            show_error("Pilih meja terlebih dahulu!")
            return
        
        val = self.table_tree.item(selected, "values")
        t_id = val[0]
        
        from cafe_app.logika.waiter_model import WaiterModel
        if WaiterModel().clear_table(t_id):
            show_info(f"Meja {val[1]} berhasil dikosongkan!")
            self.refresh_all()
        else:
            show_error("Gagal update status meja")

    def load_pending_orders(self):
        from cafe_app.logika.waiter_model import WaiterModel
        
        for i in self.tree.get_children():
            self.tree.delete(i)

        orders = WaiterModel().get_pending_orders()
        # orders: [(id, nomor_meja, status), ...]
        
        for order in orders:
            self.tree.insert(
                "",
                "end",
                values=(order[0], f"Meja {order[1]}", order[2])
            )

    def set_delivered(self):
        selected = self.tree.focus()
        if not selected:
            show_error("Pilih pesanan terlebih dahulu!")
            return
            
        values = self.tree.item(selected, "values")
        order_id = values[0]
        
        from cafe_app.logika.waiter_model import WaiterModel
        if WaiterModel().complete_order(order_id):
            show_info(f"Pesanan {order_id} berhasil diantar!")
            self.load_pending_orders()
        else:
            show_error("Gagal update status")
