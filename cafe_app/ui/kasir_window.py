import tkinter as tk
from tkinter import ttk
from cafe_app.database import get_menu_items
from cafe_app.utils import show_info, show_error

class KasirWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Kasir - Café App")
        self.window.geometry("900x500")
        self.window.resizable(False, False)

        self.selected_items = []

        self.build_ui()

    def build_ui(self):
        frame_left = tk.Frame(self.window)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        lbl = tk.Label(frame_left, text="Menu Items", font=("Arial", 14))
        lbl.pack()

        # ==== Tambahkan kolom NAMA ====
        self.menu_list = ttk.Treeview(
            frame_left,
            columns=("Nama", "Harga", "Stok"),
            show="headings",
            height=20
        )
        self.menu_list.heading("Nama", text="Nama")
        self.menu_list.heading("Harga", text="Harga")
        self.menu_list.heading("Stok", text="Stok")

        self.menu_list.column("Nama", width=150)
        self.menu_list.column("Harga", width=80)
        self.menu_list.column("Stok", width=60)

        self.menu_list.pack()
        self.load_menu()

        frame_mid = tk.Frame(self.window)
        frame_mid.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        tk.Button(frame_mid, text="Tambah >>", command=self.add_item).pack(pady=5)
        tk.Button(frame_mid, text="<< Hapus", command=self.remove_item).pack(pady=5)

        frame_right = tk.Frame(self.window)
        frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        lbl2 = tk.Label(frame_right, text="Keranjang", font=("Arial", 14))
        lbl2.pack()

        # ==== Tambahkan kolom NAMA juga di cart ====
        self.cart = ttk.Treeview(
            frame_right,
            columns=("Nama", "Jumlah", "Subtotal"),
            show="headings",
            height=15
        )
        self.cart.heading("Nama", text="Nama")
        self.cart.heading("Jumlah", text="Jumlah")
        self.cart.heading("Subtotal", text="Subtotal")

        self.cart.column("Nama", width=150)
        self.cart.column("Jumlah", width=70)
        self.cart.column("Subtotal", width=100)

        self.cart.pack(fill=tk.BOTH, expand=True)

        tk.Button(frame_right, text="Checkout", command=self.checkout).pack(pady=10)

    def load_menu(self):
        data = get_menu_items()  
        # format item: (id, nama, kategori, harga, stok, foto)

        for item in data:
            item_id = item[0]
            nama = item[1]
            harga = item[3]
            stok = item[4]

            self.menu_list.insert("", tk.END, iid=item_id, values=(nama, harga, stok))

    def add_item(self):
        selected = self.menu_list.focus()
        if not selected:
            show_error("Pilih item terlebih dahulu!")
            return
        
        nama, harga, stok = self.menu_list.item(selected, "values")
        harga = int(harga)

        # Masukkan ke keranjang
        self.cart.insert("", tk.END, iid=selected, values=(nama, 1, harga))

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
