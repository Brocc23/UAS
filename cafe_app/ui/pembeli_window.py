import tkinter as tk
from tkinter import ttk, messagebox
from cafe_app.logika.menu_model import MenuModel
from cafe_app.logika.order_model import OrderModel


class PembeliWindow:
    def __init__(self, root, user):
        self.window = tk.Toplevel(root)
        self.window.title("Pemesanan Menu")
        self.window.state("zoomed")

        self.menu_model = MenuModel()
        self.order = OrderModel()

        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        # ===== HEADER =====
        header = ttk.Label(
            container,
            text="Pemesanan Menu",
            font=("Poppins", 18, "bold")
        )
        header.pack(pady=10)

        # ===== MENU TABLE =====
        table_frame = ttk.Frame(container)
        table_frame.pack(fill="both", expand=True)

        self.menu_table = ttk.Treeview(
            table_frame,
            columns=("nama", "kategori", "harga"),
            show="headings"
        )
        self.menu_table.heading("nama", text="Nama")
        self.menu_table.heading("kategori", text="Kategori")
        self.menu_table.heading("harga", text="Harga")

        self.menu_table.column("nama", width=300)
        self.menu_table.column("kategori", width=150, anchor="center")
        self.menu_table.column("harga", width=120, anchor="center")

        self.menu_table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.menu_table.yview
        )
        self.menu_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ===== INPUT =====
        input_frame = ttk.Frame(container)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Jumlah").pack(side="left", padx=5)
        self.jumlah_var = tk.IntVar(value=1)
        ttk.Entry(input_frame, textvariable=self.jumlah_var, width=8).pack(side="left")

        ttk.Button(
            input_frame,
            text="Tambah Pesanan",
            command=self.tambah_item
        ).pack(side="left", padx=10)

        # ===== ORDER LIST =====
        order_box = ttk.LabelFrame(container, text="Pesanan")
        order_box.pack(fill="x", pady=10)

        self.order_table = ttk.Treeview(
            order_box,
            columns=("nama", "jumlah", "subtotal"),
            show="headings",
            height=5
        )
        self.order_table.heading("nama", text="Menu")
        self.order_table.heading("jumlah", text="Jumlah")
        self.order_table.heading("subtotal", text="Subtotal")

        self.order_table.pack(fill="x")

        # ===== TOTAL =====
        self.total_label = ttk.Label(
            container,
            text="Total : Rp0",
            font=("Poppins", 14, "bold")
        )
        self.total_label.pack(pady=10)

        # ===== ACTION =====
        ttk.Button(
            container,
            text="Selesaikan Pesanan",
            width=30,
            command=self.pilih_pembayaran
        ).pack(pady=10)

        self.load_menu()

    # =========================
    def load_menu(self):
        self.menu_table.delete(*self.menu_table.get_children())
        for m in self.menu_model.get_all_menu():
            self.menu_table.insert("", "end", values=(m[1], m[2], m[3]))

    def tambah_item(self):
        pilih = self.menu_table.focus()
        if not pilih:
            return

        nama, kategori, harga = self.menu_table.item(pilih)["values"]
        jumlah = self.jumlah_var.get()
        if jumlah <= 0:
            return

        self.order.add_item(nama, harga, jumlah)
        self.refresh_order()

    def refresh_order(self):
        self.order_table.delete(*self.order_table.get_children())
        for item in self.order.items:
            self.order_table.insert(
                "", "end",
                values=(item["nama"], item["jumlah"], item["subtotal"])
            )
        self.total_label.config(
            text=f"Total : Rp{self.order.get_total():,}"
        )

    # =========================
    def pilih_pembayaran(self):
        if not self.order.items:
            return

        popup = tk.Toplevel(self.window)
        popup.title("Metode Pembayaran")
        popup.geometry("350x200")
        popup.resizable(False, False)

        ttk.Label(
            popup,
            text="Pilih Metode Pembayaran",
            font=("Poppins", 14, "bold")
        ).pack(pady=15)

        ttk.Button(
            popup,
            text="QRIS",
            width=20,
            command=lambda: self.selesai(popup, "QRIS")
        ).pack(pady=5)

        ttk.Button(
            popup,
            text="Tunai",
            width=20,
            command=lambda: self.selesai(popup, "Tunai")
        ).pack(pady=5)

    def selesai(self, popup, metode):
        popup.destroy()
        total = self.order.get_total()

        messagebox.showinfo(
            "Pembayaran",
            f"Cara pembayaran : {metode}\n"
            f"Total : Rp{total:,}\n\n"
            f"Silahkan pergi ke kasir"
        )

        self.window.destroy()
