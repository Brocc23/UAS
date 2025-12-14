import tkinter as tk
from tkinter import ttk
from cafe_app.utils import show_error

class KasirWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.window = tk.Toplevel(root)
        self.window.title("Kasir")
        self.window.geometry("900x900")
        self.window.resizable(False, False)

        self.metode = tk.StringVar(value="QRIS")
        self.total_var = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Kasir", font=("Poppins", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Metode Pembayaran").pack(anchor="w")
        ttk.Radiobutton(frame, text="QRIS", variable=self.metode, value="QRIS").pack(anchor="w")
        ttk.Radiobutton(frame, text="Tunai", variable=self.metode, value="Tunai").pack(anchor="w")

        ttk.Label(frame, text="Total Harga").pack(anchor="w", pady=(10, 0))
        ttk.Entry(frame, textvariable=self.total_var).pack(fill="x")

        ttk.Button(frame, text="Bayar", command=self.bayar).pack(pady=15)

        self.result_frame = ttk.Frame(frame)
        self.result_frame.pack(fill="both", expand=True)

    def bayar(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

        total = self.total_var.get()
        if not total.isdigit():
            show_error("Total harga harus angka")
            return

        total = int(total)

        if self.metode.get() == "QRIS":
            img = tk.PhotoImage(file="cafe_app/assets/images/qris_dummy.png")
            label_img = ttk.Label(self.result_frame, image=img)
            label_img.image = img
            label_img.pack(pady=10)

            ttk.Label(
                self.result_frame,
                text=f"Total: Rp {total:,}",
                font=("Poppins", 14, "bold")
            ).pack()

        else:
            ttk.Label(
                self.result_frame,
                text=f"Total Tunai\nRp {total:,}",
                font=("Poppins", 18, "bold")
            ).pack(pady=40)