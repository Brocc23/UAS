import tkinter as tk
from tkinter import ttk
import uuid
from cafe_app.database import get_menu_items
from cafe_app.utils import show_info, show_error

class KasirWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.window = tk.Toplevel(root)
        self.window.title("Kasir - Café App")
        self.window.geometry("950x520")
        self.window.resizable(False, False)
        self.window.configure(bg="#f5f6fa")

        self.build_ui()

    def build_ui(self):
        # ===== STYLE (UI ONLY) =====
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=28)
        style.configure("Header.TLabel", font=("Poppins", 16, "bold"))
        style.configure("Section.TLabelframe", padding=10)

        main = tk.Frame(self.window, bg="#f5f6fa")
        main.pack(fill="both", expand=True, padx=12, pady=12)

        # ===== LEFT : MENU =====
        frame_left = ttk.LabelFrame(main, text="Daftar Menu", style="Section.TLabelframe")
        frame_left.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(frame_left, text="Menu Items", style="Header.TLabel").pack(pady=5)

        self.menu_list = ttk.Treeview(
            frame_left,
            columns=("Nama", "Harga", "Stok"),
            show="headings",
            height=18
        )
        self.menu_list.heading("Nama", text="Nama")
        self.menu_list.heading("Harga", text="Harga")
        self.menu_list.heading("Stok", text="Stok")

        self.menu_list.column("Nama", width=180, anchor="w")
        self.menu_list.column("Harga", width=90, anchor="center")
        self.menu_list.column("Stok", width=70, anchor="center")

        self.menu_list.pack()
        self.load_menu()

        # ===== MIDDLE : ACTION =====
        frame_mid = ttk.Frame(main)
        frame_mid.pack(side=tk.LEFT, fill=tk.Y, padx=15)

        ttk.Button(frame_mid, text="Tambah ▶", command=self.add_item, width=15).pack(pady=10)
        ttk.Button(frame_mid, text="◀ Hapus", command=self.remove_item, width=15).pack(pady=10)

        # ===== RIGHT : CART =====
        frame_right = ttk.LabelFrame(main, text="Keranjang", style="Section.TLabelframe")
        frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(frame_right, text="Keranjang Belanja", style="Header.TLabel").pack(pady=5)

        self.cart = ttk.Treeview(
            frame_right,
            columns=("Nama", "Jumlah", "Subtotal"),
            show="headings",
            height=14
        )
        self.cart.heading("Nama", text="Nama")
        self.cart.heading("Jumlah", text="Jumlah")
        self.cart.heading("Subtotal", text="Subtotal")

        self.cart.column("Nama", width=200, anchor="w")
        self.cart.column("Jumlah", width=80, anchor="center")
        self.cart.column("Subtotal", width=120, anchor="center")

        self.cart.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame_right, text="Checkout", command=self.checkout).pack(pady=12)

    def load_menu(self):
        data = get_menu_items()
        for item in data:
            menu_id = item[0]
            nama = item[1]
            harga = item[3]
            stok = item[4]
            self.menu_list.insert("", tk.END, iid=str(menu_id), values=(nama, harga, stok))

    def add_item(self):
        selected = self.menu_list.focus()
        if not selected:
            show_error("Pilih item terlebih dahulu!")
            return
        
        nama, harga, stok = self.menu_list.item(selected, "values")
        harga = int(harga)

        iid_cart = str(uuid.uuid4())
        self.cart.insert("", tk.END, iid=iid_cart, values=(nama, 1, harga))

    def remove_item(self):
        selected = self.cart.focus()
        if selected:
            self.cart.delete(selected)

    def checkout(self):
        total = 0
        for iid in self.cart.get_children():
            subtotal = int(self.cart.item(iid, "values")[2])
            total += subtotal
        show_info(f"Total pembayaran: {total}")