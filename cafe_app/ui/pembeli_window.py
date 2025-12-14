import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from cafe_app.logika.menu_model import MenuModel


class PembeliWindow:
    def __init__(self, root, user):
        self.window = tk.Toplevel(root)
        self.window.title("Pemesanan Menu")
        self.window.state("zoomed")

        self.menu_model = MenuModel()
        self.cart = []
        self.images = []

        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        header = ttk.Label(
            container,
            text="Pemesanan Menu",
            font=("Poppins", 18, "bold")
        )
        header.pack(pady=10)

        control = ttk.Frame(container)
        control.pack(fill="x", pady=10)

        ttk.Label(control, text="Cari").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(control, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.load_menu())

        ttk.Label(control, text="Kategori").pack(side="left", padx=10)
        self.kategori_var = tk.StringVar(value="Semua")
        kategori_box = ttk.Combobox(
            control,
            textvariable=self.kategori_var,
            values=["Semua", "Makanan", "Minuman"],
            width=15,
            state="readonly"
        )
        kategori_box.pack(side="left")
        kategori_box.bind("<<ComboboxSelected>>", lambda e: self.load_menu())

        menu_area = ttk.Frame(container)
        menu_area.pack(fill="both", expand=True)

        canvas = tk.Canvas(menu_area)
        scrollbar = ttk.Scrollbar(menu_area, orient="vertical", command=canvas.yview)
        self.menu_frame = ttk.Frame(canvas)

        self.menu_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.menu_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        order_box = ttk.LabelFrame(container, text="Keranjang")
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

        self.total_label = ttk.Label(
            container,
            text="Total : Rp0",
            font=("Poppins", 14, "bold")
        )
        self.total_label.pack(pady=10)

        ttk.Button(
            container,
            text="Selesaikan Pesanan",
            width=30,
            command=self.pilih_pembayaran
        ).pack(pady=10)

        self.load_menu()

    def load_menu(self):
        for w in self.menu_frame.winfo_children():
            w.destroy()

        self.images.clear()

        keyword = self.search_var.get()
        kategori = self.kategori_var.get()
        if kategori == "Semua":
            kategori = None

        menus = self.menu_model.search_menu(keyword, kategori)

        for m in menus:
            card = ttk.Frame(self.menu_frame, padding=10, relief="ridge")
            card.pack(fill="x", pady=6)

            img_label = ttk.Label(card)
            img_label.pack(side="left", padx=10)

            if m[5] and os.path.exists(m[5]):
                img = Image.open(m[5])
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)
                img_label.config(image=photo)
                self.images.append(photo)
            else:
                img_label.config(text="No Image", width=12)

            info = ttk.Frame(card)
            info.pack(side="left", fill="x", expand=True)

            ttk.Label(info, text=m[1], font=("Poppins", 12, "bold")).pack(anchor="w")
            ttk.Label(info, text=f"Kategori: {m[2]}").pack(anchor="w")
            ttk.Label(info, text=f"Harga: Rp{m[3]:,}").pack(anchor="w")

            action = ttk.Frame(card)
            action.pack(side="right")

            qty = tk.IntVar(value=1)
            ttk.Entry(action, textvariable=qty, width=5).pack(pady=2)
            ttk.Button(
                action,
                text="Tambah",
                command=lambda x=m, q=qty: self.add_to_cart(x, q.get())
            ).pack(pady=2)

    def add_to_cart(self, menu, jumlah):
        if jumlah <= 0:
            return

        for item in self.cart:
            if item["id"] == menu[0]:
                item["jumlah"] += jumlah
                self.refresh_cart()
                return

        self.cart.append({
            "id": menu[0],
            "nama": menu[1],
            "harga": menu[3],
            "jumlah": jumlah
        })
        self.refresh_cart()

    def refresh_cart(self):
        self.order_table.delete(*self.order_table.get_children())
        total = 0
        for item in self.cart:
            subtotal = item["harga"] * item["jumlah"]
            total += subtotal
            self.order_table.insert(
                "",
                "end",
                values=(item["nama"], item["jumlah"], subtotal)
            )
        self.total_label.config(text=f"Total : Rp{total:,}")

    def pilih_pembayaran(self):
        if not self.cart:
            return

        popup = tk.Toplevel(self.window)
        popup.title("Pembayaran")
        popup.geometry("350x300")

        total = sum(i["harga"] * i["jumlah"] for i in self.cart)

        ttk.Label(
            popup,
            text=f"Total : Rp{total:,}",
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
        messagebox.showinfo(
            "Pembayaran",
            f"Metode: {metode}\nPembayaran berhasil"
        )
        self.cart.clear()
        self.refresh_cart()
