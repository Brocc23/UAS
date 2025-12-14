import tkinter as tk
from tkinter import ttk
from cafe_app.logika.menu_model import MenuModel
from cafe_app.logika.order_model import OrderModel

class OrderWindow:
    def __init__(self, master, meja_id=None, pembeli_nama=None):
        self.master = master
        self.master.title("Pemesanan Menu")
        self.master.geometry("720x520")
        self.master.configure(bg="#f5f6fa")

        self.meja_id = meja_id
        self.pembeli_nama = pembeli_nama

        self.order = OrderModel()
        self.menu_model = MenuModel()

        # ===== STYLE (UI ONLY) =====
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=28)
        style.configure("Header.TLabel", font=("Poppins", 16, "bold"))
        style.configure("Section.TLabelframe", padding=10)

        container = ttk.Frame(master, padding=12)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Pemesanan Menu", style="Header.TLabel").pack(pady=(0, 10))

        # ===== MENU LIST =====
        menu_box = ttk.LabelFrame(container, text="Daftar Menu", style="Section.TLabelframe")
        menu_box.pack(fill="both", expand=True)

        list_frame = ttk.Frame(menu_box)
        list_frame.pack(fill="both", expand=True)

        self.menu_list = ttk.Treeview(
            list_frame,
            columns=("nama", "kategori", "harga", "stok"),
            show="headings",
            height=10
        )
        self.menu_list.heading("nama", text="Nama")
        self.menu_list.heading("kategori", text="Kategori")
        self.menu_list.heading("harga", text="Harga")
        self.menu_list.heading("stok", text="Stok")

        self.menu_list.column("nama", width=180, anchor="w")
        self.menu_list.column("kategori", width=120, anchor="center")
        self.menu_list.column("harga", width=100, anchor="center")
        self.menu_list.column("stok", width=80, anchor="center")

        self.menu_list.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.menu_list.yview)
        self.menu_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ===== INPUT =====
        input_box = ttk.LabelFrame(container, text="Tambah Pesanan", style="Section.TLabelframe")
        input_box.pack(fill="x", pady=10)

        ttk.Label(input_box, text="Jumlah").grid(row=0, column=0, padx=5, pady=5)
        self.jumlah_var = tk.IntVar(value=1)
        ttk.Entry(input_box, textvariable=self.jumlah_var, width=10).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(input_box, text="Tambah", width=15, command=self.tambah).grid(row=0, column=2, padx=8)
        ttk.Button(input_box, text="Hapus Item", width=15, command=self.hapus).grid(row=0, column=3, padx=8)

        # ===== ORDER LIST =====
        order_box = ttk.LabelFrame(container, text="Pesanan", style="Section.TLabelframe")
        order_box.pack(fill="x")

        self.order_table = ttk.Treeview(
            order_box,
            columns=("nama", "jumlah", "harga"),
            show="headings",
            height=6
        )
        self.order_table.heading("nama", text="Menu")
        self.order_table.heading("jumlah", text="Jumlah")
        self.order_table.heading("harga", text="Subtotal")

        self.order_table.column("nama", width=200, anchor="w")
        self.order_table.column("jumlah", width=80, anchor="center")
        self.order_table.column("harga", width=120, anchor="center")

        self.order_table.pack(fill="x")

        # ===== TOTAL & ACTION =====
        bottom = ttk.Frame(container)
        bottom.pack(fill="x", pady=10)

        self.total_label = ttk.Label(bottom, text="Total: Rp0", font=("Poppins", 14, "bold"))
        self.total_label.pack(side="left", padx=5)

        ttk.Button(bottom, text="Selesaikan Pesanan", width=25, command=self.selesai).pack(side="right", padx=5)

        self.load_menu()
        self.load_order_table()

    def load_menu(self):
        self.menu_list.delete(*self.menu_list.get_children())
        data = self.menu_model.get_all_menu()
        for item in data:
            self.menu_list.insert("", "end", values=item)

    def load_order_table(self):
        self.order_table.delete(*self.order_table.get_children())
        for item in self.order.items:
            self.order_table.insert("", "end",
                                    values=(item["nama"], item["jumlah"], item["subtotal"]))
        self.total_label.config(text=f"Total: Rp{self.order.get_total():,}")

    def tambah(self):
        pilih = self.menu_list.focus()
        if not pilih:
            return
        data = self.menu_list.item(pilih)["values"]
        nama, kategori, harga, stok = data
        jumlah = self.jumlah_var.get()
        if jumlah <= 0:
            return
        self.order.add_item(nama, harga, jumlah)
        self.load_order_table()

    def hapus(self):
        pilih = self.order_table.focus()
        if not pilih:
            return
        nama = self.order_table.item(pilih)["values"][0]
        self.order.remove_item(nama)
        self.load_order_table()

    def selesai(self):
        self.master.destroy()