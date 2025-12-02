import tkinter as tk
from tkinter import ttk
from cafe_app.database import get_menu_items
from cafe_app.utils import show_info, show_error, ask_yes_no

class KasirWindow:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Kasir - Café App")
        self.window.geometry("800x500")
        self.window.resizable(False, False)

        self.selected_items = []

        self.build_ui()

    def build_ui(self):
        frame_left = tk.Frame(self.window)
        frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        lbl = tk.Label(frame_left, text="Menu Items", font=("Arial", 14))
        lbl.pack()

        self.menu_list = ttk.Treeview(frame_left, columns=("Harga", "Stok"), show="headings", height=20)
        self.menu_list.heading("Harga", text="Harga")
        self.menu_list.heading("Stok", text="Stok")
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

        self.cart = ttk.Treeview(frame_right, columns=("Jumlah", "Subtotal"), show="headings", height=15)
        self.cart.heading("Jumlah", text="Jumlah")
        self.cart.heading("Subtotal", text="Subtotal")
        self.cart.pack(fill=tk.BOTH, expand=True)

        tk.Button(frame_right, text="Checkout", command=self.checkout).pack(pady=10)

    def load_menu(self):
        data = get_menu_items()
        for item in data:
            self.menu_list.insert("", tk.END, iid=item[0], values=(item[3], item[4]))

    def add_item(self):
        selected = self.menu_list.focus()
        if not selected:
            show_error("Pilih item terlebih dahulu!")
            return
        harga = int(self.menu_list.item(selected, "values")[0])
        self.cart.insert("", tk.END, iid=selected, values=(1, harga))

    def remove_item(self):
        selected = self.cart.focus()
        if not selected:
            return
        self.cart.delete(selected)

    def checkout(self):
        total = 0
        for iid in self.cart.get_children():
            subtotal = int(self.cart.item(iid, "values")[1])
            total += subtotal
        show_info(f"Total pembayaran: {total}")