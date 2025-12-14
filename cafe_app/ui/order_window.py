import tkinter as tk
from tkinter import ttk
from cafe_app.logika.menu_model import MenuModel
from cafe_app.logika.order_model import OrderModel
import qrcode
from PIL import Image, ImageTk


class OrderWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Pemesanan Menu")
        self.window.state("zoomed")

        self.menu_model = MenuModel()
        self.order = OrderModel()

        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        # ===== TOP BAR =====
        top = ttk.Frame(container)
        top.pack(fill="x")

        ttk.Label(top, text="Pemesanan Menu", font=("Poppins", 18, "bold")).pack(side="left")

        # SEARCH
        self.search_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.search_var, width=30).pack(side="right", padx=5)
        ttk.Button(top, text="Cari", command=self.load_menu).pack(side="right")

        # FILTER
        self.filter_var = tk.StringVar(value="Semua")
        ttk.Combobox(
            top,
            values=["Semua", "Makanan", "Minuman"],
            textvariable=self.filter_var,
            width=12
        ).pack(side="right", padx=5)

        # ===== MENU LIST =====
        self.menu_table = ttk.Treeview(
            container,
            columns=("nama", "kategori", "harga"),
            show="headings",
            height=12
        )
        self.menu_table.heading("nama", text="Menu")
        self.menu_table.heading("kategori", text="Kategori")
        self.menu_table.heading("harga", text="Harga")
        self.menu_table.pack(fill="both", expand=True, pady=10)

        # ===== INPUT =====
        input_box = ttk.Frame(container)
        input_box.pack(fill="x")

        self.jumlah_var = tk.IntVar(value=1)
        ttk.Entry(input_box, textvariable=self.jumlah_var, width=5).pack(side="left")
        ttk.Button(input_box, text="Tambah", command=self.tambah).pack(side="left", padx=5)

        # ===== ORDER LIST =====
        self.order_table = ttk.Treeview(
            container,
            columns=("nama", "jumlah", "subtotal"),
            show="headings",
            height=6
        )
        self.order_table.heading("nama", text="Menu")
        self.order_table.heading("jumlah", text="Jumlah")
        self.order_table.heading("subtotal", text="Subtotal")
        self.order_table.pack(fill="x", pady=10)

        # ===== BOTTOM =====
        bottom = ttk.Frame(container)
        bottom.pack(fill="x")

        self.total_label = ttk.Label(bottom, text="Total: Rp0", font=("Poppins", 14, "bold"))
        self.total_label.pack(side="left")

        ttk.Button(
            bottom,
            text="Selesaikan Pesanan",
            command=self.bayar
        ).pack(side="right")

        self.load_menu()

    def load_menu(self):
        self.menu_table.delete(*self.menu_table.get_children())
        keyword = self.search_var.get().lower()
        kategori = self.filter_var.get()

        for m in self.menu_model.get_all_menu():
            if keyword and keyword not in m[1].lower():
                continue
            if kategori != "Semua" and m[2] != kategori:
                continue

            self.menu_table.insert("", "end", values=(m[1], m[2], m[3]))

    def tambah(self):
        pilih = self.menu_table.focus()
        if not pilih:
            return
        nama, kategori, harga = self.menu_table.item(pilih)["values"]
        jumlah = self.jumlah_var.get()

        self.order.add_item(nama, harga, jumlah)
        self.refresh_order()

    def refresh_order(self):
        self.order_table.delete(*self.order_table.get_children())
        for i in self.order.items:
            self.order_table.insert("", "end",
                values=(i["nama"], i["jumlah"], i["subtotal"])
            )
        self.total_label.config(text=f"Total: Rp{self.order.get_total():,}")

    # ===== PEMBAYARAN =====
    def bayar(self):
        pay = tk.Toplevel(self.window)
        pay.title("Pembayaran")
        pay.geometry("400x450")

        total = self.order.get_total()

        metode = tk.StringVar(value="QRIS")
        ttk.Radiobutton(pay, text="QRIS", variable=metode, value="QRIS").pack()
        ttk.Radiobutton(pay, text="Tunai", variable=metode, value="Tunai").pack()

        frame = ttk.Frame(pay)
        frame.pack(expand=True)

        def tampilkan():
            for w in frame.winfo_children():
                w.destroy()

            if metode.get() == "QRIS":
                img = qrcode.make(f"PAY-{total}")
                img = img.resize((220, 220))
                img = ImageTk.PhotoImage(img)
                lbl = ttk.Label(frame, image=img)
                lbl.image = img
                lbl.pack()
            ttk.Label(frame, text=f"Total: Rp{total:,}",
                      font=("Poppins", 14, "bold")).pack(pady=10)

        ttk.Button(pay, text="Tampilkan", command=tampilkan).pack(pady=5)

        ttk.Button(
            pay,
            text="Selesai",
            command=lambda: (pay.destroy(), self.window.destroy())
        ).pack(pady=10)
