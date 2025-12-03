import tkinter as tk
from tkinter import ttk
from cafe_app.logika.menu_model import menu_model
from cafe_app.logika.order_model import order_model

class OrderWindow:
    def __init__(self, master, meja_id=None, pembeli_nama=None):
        self.master = master
        self.master.title("Pemesanan Menu")
        self.master.geometry("650x450")

        self.meja_id = meja_id
        self.pembeli_nama = pembeli_nama

        self.order = OrderModel()
        self.menu_model = MenuModel()

        frame = ttk.Frame(master, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Pilih Menu", font=("Poppins", 16, "bold")).pack()

        list_frame = ttk.Frame(frame)
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
        self.menu_list.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.menu_list.yview)
        self.menu_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Jumlah").grid(row=0, column=0, padx=5)
        self.jumlah_var = tk.IntVar(value=1)
        ttk.Entry(input_frame, textvariable=self.jumlah_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Button(input_frame, text="Tambah", width=15, command=self.tambah).grid(row=0, column=2, padx=5)
        ttk.Button(input_frame, text="Hapus Item", width=15, command=self.hapus).grid(row=0, column=3, padx=5)

        self.total_label = ttk.Label(frame, text="Total: Rp0", font=("Poppins", 14))
        self.total_label.pack(pady=10)

        ttk.Button(frame, text="Selesaikan Pesanan", width=30, command=self.selesai).pack(pady=5)

        self.load_menu()
        self.load_order_table()

    def load_menu(self):
        self.menu_list.delete(*self.menu_list.get_children())
        data = self.menu_model.get_all_menu()
        for item in data:
            self.menu_list.insert("", "end", values=item)

    def load_order_table(self):
        if hasattr(self, "order_table"):
            self.order_table.destroy()

        self.order_table = ttk.Treeview(
            self.master,
            columns=("nama", "jumlah", "harga"),
            show="headings",
            height=5
        )
        self.order_table.heading("nama", text="Menu")
        self.order_table.heading("jumlah", text="Jumlah")
        self.order_table.heading("harga", text="Subtotal")
        self.order_table.pack(pady=5)

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
