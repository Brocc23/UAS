import tkinter as tk
from tkinter import ttk
from cafe_app.logika.menu_model import MenuModel
import qrcode
from PIL import Image, ImageTk
import tempfile
import os


class PembeliWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        # ❗ PENTING: pakai Toplevel, BUKAN root langsung
        self.window = tk.Toplevel(root)
        self.window.title("Pemesanan - Pembeli")
        self.window.state("zoomed")

        self.menu_model = MenuModel()
        self.items = []

        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Pemesanan Menu",
            font=("Poppins", 18, "bold")
        ).pack(pady=10)

        # ===== MENU LIST =====
        self.menu_table = ttk.Treeview(
            container,
            columns=("Nama", "Kategori", "Harga"),
            show="headings",
            height=10
        )
        self.menu_table.heading("Nama", text="Nama")
        self.menu_table.heading("Kategori", text="Kategori")
        self.menu_table.heading("Harga", text="Harga")
        self.menu_table.pack(fill="x")

        self.load_menu()

        # ===== INPUT JUMLAH =====
        input_frame = ttk.Frame(container)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Jumlah").pack(side="left")
        self.jumlah_var = tk.IntVar(value=1)
        ttk.Entry(input_frame, textvariable=self.jumlah_var, width=6).pack(side="left", padx=5)

        ttk.Button(
            input_frame,
            text="Tambah",
            command=self.tambah_item
        ).pack(side="left", padx=5)

        # ===== PESANAN =====
        self.order_table = ttk.Treeview(
            container,
            columns=("Nama", "Jumlah", "Subtotal"),
            show="headings",
            height=6
        )
        self.order_table.heading("Nama", text="Menu")
        self.order_table.heading("Jumlah", text="Jumlah")
        self.order_table.heading("Subtotal", text="Subtotal")
        self.order_table.pack(fill="x", pady=10)

        self.total_label = ttk.Label(
            container,
            text="Total: Rp0",
            font=("Poppins", 14, "bold")
        )
        self.total_label.pack(pady=5)

        ttk.Button(
            container,
            text="Selesaikan Pesanan",
            command=self.pilih_pembayaran,
            width=30
        ).pack(pady=10)

    # ===== LOGIKA =====
    def load_menu(self):
        for i in self.menu_table.get_children():
            self.menu_table.delete(i)

        for m in self.menu_model.get_all_menu():
            self.menu_table.insert("", "end", values=(m[1], m[2], m[3]))

    def tambah_item(self):
        pilih = self.menu_table.focus()
        if not pilih:
            return

        nama, kategori, harga = self.menu_table.item(pilih)["values"]
        jumlah = self.jumlah_var.get()
        subtotal = harga * jumlah

        self.items.append(subtotal)
        self.order_table.insert("", "end", values=(nama, jumlah, subtotal))
        self.update_total()

    def update_total(self):
        total = sum(self.items)
        self.total_label.config(text=f"Total: Rp{total:,}")

    # ===== PEMBAYARAN =====
    def pilih_pembayaran(self):
        win = tk.Toplevel(self.window)
        win.title("Pembayaran")
        win.geometry("400x400")

        ttk.Label(win, text="Pilih Metode Pembayaran", font=("Poppins", 14, "bold")).pack(pady=15)

        ttk.Button(
            win,
            text="QRIS",
            width=20,
            command=lambda: self.show_qr(win)
        ).pack(pady=10)

        ttk.Button(
            win,
            text="Tunai",
            width=20,
            command=lambda: self.show_tunai(win)
        ).pack(pady=10)

    def show_qr(self, parent):
        total = sum(self.items)
        data = f"QRIS-PEMBAYARAN-RP-{total}"

        img = qrcode.make(data)
        path = os.path.join(tempfile.gettempdir(), "qris.png")
        img.save(path)

        qr = ImageTk.PhotoImage(Image.open(path).resize((250, 250)))

        win = tk.Toplevel(parent)
        win.title("QRIS")
        ttk.Label(win, image=qr).pack()
        ttk.Label(win, text=f"Total: Rp{total:,}", font=("Poppins", 12, "bold")).pack(pady=10)

        win.image = qr  # keep reference

    def show_tunai(self, parent):
        total = sum(self.items)
        win = tk.Toplevel(parent)
        win.title("Pembayaran Tunai")
        ttk.Label(win, text=f"Total Bayar: Rp{total:,}", font=("Poppins", 14, "bold")).pack(pady=30)
