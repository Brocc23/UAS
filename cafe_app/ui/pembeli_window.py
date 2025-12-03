import tkinter as tk
from tkinter import ttk
from cafe_app.logika.menu_model import menu_model
from cafe_app.ui.order_window import order_window

class PembeliWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Halaman Pembeli")
        self.master.geometry("600x450")

        self.menu_model = MenuModel()

        frame = ttk.Frame(master, padding=20)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="Menu Pembeli", font=("Poppins", 18, "bold"))
        title.pack(pady=10)

        self.tree = ttk.Treeview(frame, columns=("Kategori", "Harga", "Stok"), show="headings", height=10)
        self.tree.heading("Kategori", text="Kategori")
        self.tree.heading("Harga", text="Harga")
        self.tree.heading("Stok", text="Stok")

        self.tree.column("Kategori", width=120)
        self.tree.column("Harga", width=80)
        self.tree.column("Stok", width=60)

        self.tree.pack(fill="both", expand=True, padx=5, pady=10)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Pesan", command=self.buka_order).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_menu).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Logout", command=self.master.destroy).grid(row=0, column=2, padx=5)

        self.load_menu()

    def load_menu(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for m in self.menu_model.get_all_menu():
            self.tree.insert("", "end", values=(m["kategori"], m["harga"], m["stok"]))

    def buka_order(self):
        OrderWindow(tk.Toplevel(self.master))
