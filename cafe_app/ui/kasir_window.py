import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import os
from cafe_app.utils import show_error

QRIS_PATH = r"cafe_app\assets\images\qris_dummy.png"

class KasirWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.window = tk.Toplevel(root)
        self.window.title("Kasir - Café App")
        self.window.geometry("700x980")
        self.window.resizable(False, False)

        self.metode = tk.StringVar(value="QRIS")
        self.total_var = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        main = ttk.Frame(self.window, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Kasir Manual",
            font=("Poppins", 16, "bold")
        ).pack(pady=10)

        ttk.Label(main, text="Total Harga").pack(anchor="w")
        ttk.Entry(main, textvariable=self.total_var).pack(fill="x", pady=5)

        ttk.Label(main, text="Metode Pembayaran").pack(anchor="w", pady=(15, 5))

        ttk.Radiobutton(
            main, text="QRIS", variable=self.metode, value="QRIS"
        ).pack(anchor="w")

        ttk.Radiobutton(
            main, text="Tunai", variable=self.metode, value="TUNAI"
        ).pack(anchor="w")

        ttk.Button(
            main,
            text="Proses Pembayaran",
            command=self.proses_pembayaran
        ).pack(pady=20)

        self.result_frame = ttk.Frame(main)
        self.result_frame.pack()

    def proses_pembayaran(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

        total = self.total_var.get()
        if not total.isdigit():
            show_error("Total harus berupa angka")
            return

        total = int(total)

        if self.metode.get() == "QRIS":
            self.show_qris(total)
        else:
            self.show_tunai(total)

    def show_qris(self, total):
        ttk.Label(
            self.result_frame,
            text="Scan QRIS",
            font=("Poppins", 12, "bold")
        ).pack(pady=5)

        if not os.path.exists(QRIS_PATH):
            show_error("File QRIS tidak ditemukan")
            return

        img = Image.open(QRIS_PATH)
        img = img.resize((220, 220))

        self.qr_photo = ImageTk.PhotoImage(img)

        ttk.Label(
            self.result_frame,
            image=self.qr_photo
        ).pack(pady=10)

        ttk.Label(
            self.result_frame,
            text=f"Rp {total:,}",
            font=("Poppins", 11)
        ).pack()

    def show_tunai(self, total):
        ttk.Label(
            self.result_frame,
            text="Pembayaran Tunai",
            font=("Poppins", 12, "bold")
        ).pack(pady=10)

        ttk.Label(
            self.result_frame,
            text=f"Rp {total:,}",
            font=("Poppins", 11)
        ).pack()
