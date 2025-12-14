import tkinter as tk
from tkinter import ttk, messagebox
from cafe_app.logika.menu_model import MenuModel


class PembeliWindow:
    def __init__(self, root, user):
        self.user = user
        self.menu_model = MenuModel()
        self.items = []

        # ✅ WAJIB Toplevel (FIX HALAMAN KOSONG)
        self.window = tk.Toplevel(root)
        self.window.title("Pemesanan - Pembeli")
        self.window.state("zoomed")
        self.window.configure(bg="#f5f6fa")

        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        # ===== HEADER =====
        ttk.Label(
            container,
            text="Pemesanan Menu",
            font=("Poppins", 20, "bold")
        ).pack(pady=(0, 10))

        # ===== MENU LIST =====
        menu_box = ttk.LabelFrame(container, text="Daftar Menu")
        menu_box.pack(fill="both", expand=True)

        self.menu_table = ttk.Treeview(
            menu_box,
            columns=("nama", "kategori", "harga"),
            show="headings",
            height=10
        )
        self.menu_table.heading("nama", text="Menu")
        self.menu_table.heading("kategori", text="Kategori")
        self.menu_table.heading("harga", text="Harga")

        self.menu_table.column("nama", width=220)
        self.menu_table.column("kategori", width=140, anchor="center")
        self.menu_table.column("harga", width=120, anchor="center")

        self.menu_table.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(menu_box, orient="vertical", command=self.menu_table.yview)
        self.menu_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ===== INPUT JUMLAH =====
        input_frame = ttk.Frame(container)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Jumlah").pack(side="left", padx=5)
        self.qty = tk.IntVar(value=1)
        ttk.Entry(input_frame, textvariable=self.qty, width=10).pack(side="left")

        ttk.Button(
            input_frame,
            text="Tambah Pesanan",
            command=self.tambah_item
        ).pack(side="left", padx=10)

        # ===== PESANAN =====
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
            text="Total: Rp0",
            font=("Poppins", 14, "bold")
        )
        self.total_label.pack(pady=5)

        # ===== SELESAI =====
        ttk.Button(
            container,
            text="Selesaikan Pesanan",
            width=30,
            command=self.pilih_pembayaran
        ).pack(pady=10)

        self.load_menu()

    # ================= LOGIKA =================

    def load_menu(self):
        self.menu_table.delete(*self.menu_table.get_children())
        for m in self.menu_model.get_all_menu():
            self.menu_table.insert("", "end", values=(m[1], m[2], m[3]))

    def tambah_item(self):
        pilih = self.menu_table.focus()
        if not pilih:
            return

        nama, kategori, harga = self.menu_table.item(pilih)["values"]
        jumlah = self.qty.get()

        subtotal = harga * jumlah
        self.items.append((nama, jumlah, subtotal))

        self.refresh_order()

    def refresh_order(self):
        self.order_table.delete(*self.order_table.get_children())
        total = 0
        for item in self.items:
            self.order_table.insert("", "end", values=item)
            total += item[2]

        self.total_label.config(text=f"Total: Rp{total:,}")

    # ================= PEMBAYARAN =================

    def pilih_pembayaran(self):
        if not self.items:
            messagebox.showerror("Error", "Pesanan masih kosong")
            return

        win = tk.Toplevel(self.window)
        win.title("Metode Pembayaran")
        win.geometry("350x200")

        ttk.Label(
            win,
            text="Pilih Metode Pembayaran",
            font=("Poppins", 14, "bold")
        ).pack(pady=15)

        ttk.Button(
            win,
            text="QRIS",
            width=20,
            command=lambda: self.selesai(win)
        ).pack(pady=5)

        ttk.Button(
            win,
            text="Tunai",
            width=20,
            command=lambda: self.selesai(win)
        ).pack(pady=5)

    def selesai(self, win):
        win.destroy()
        messagebox.showinfo(
            "Pesanan Selesai",
            "Pesanan berhasil dibuat.\n\nSilakan ke kasir untuk pembayaran."
        )
        self.window.destroy()
