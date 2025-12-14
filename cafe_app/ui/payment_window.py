import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from cafe_app.logika.payment_model import PaymentModel


class PaymentWindow:
    def __init__(self, master, total, meja_id=None):
        self.master = master
        self.master.title("Pembayaran")
        self.master.geometry("450x420")
        self.master.resizable(False, False)

        self.total = total
        self.meja_id = meja_id
        self.payment = PaymentModel()

        container = ttk.Frame(master, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Pembayaran",
            font=("Poppins", 18, "bold")
        ).pack(pady=(0, 5))

        ttk.Label(
            container,
            text=f"Total Tagihan: Rp{total:,}",
            font=("Poppins", 14)
        ).pack(pady=(0, 15))

        ttk.Separator(container).pack(fill="x", pady=10)

        ttk.Label(
            container,
            text="Metode Pembayaran",
            font=("Poppins", 12, "bold")
        ).pack(anchor="w", pady=(5, 3))

        self.metode_var = tk.StringVar()
        metode_box = ttk.Combobox(
            container,
            textvariable=self.metode_var,
            state="readonly",
            values=["Cash", "E-Wallet", "QRIS"],
            width=30
        )
        metode_box.pack(pady=5)
        metode_box.bind("<<ComboboxSelected>>", self.show_detail)

        self.detail_frame = ttk.Frame(container, padding=10, relief="groove")
        self.detail_frame.pack(fill="x", pady=15)

        ttk.Label(
            self.detail_frame,
            text="Silakan pilih metode pembayaran",
            font=("Poppins", 11),
            foreground="gray"
        ).pack()

        self.pay_btn = ttk.Button(
            container,
            text="Bayar Sekarang",
            command=self.process_payment
        )
        self.pay_btn.pack(fill="x", pady=10)

        self.qr_image = None

    def clear_detail(self):
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

    def show_detail(self, _):
        self.clear_detail()
        metode = self.metode_var.get()

        if metode == "Cash":
            ttk.Label(
                self.detail_frame,
                text="Bayar langsung di kasir.",
                font=("Poppins", 12)
            ).pack(pady=5)

        elif metode == "E-Wallet":
            ttk.Label(
                self.detail_frame,
                text="Nomor E-Wallet",
                font=("Poppins", 11)
            ).pack(anchor="w", pady=(0, 3))

            self.nomor_ewallet = tk.StringVar()
            ttk.Entry(
                self.detail_frame,
                textvariable=self.nomor_ewallet,
                width=30
            ).pack()

        elif metode == "QRIS":
            try:
                self.qr_image = PhotoImage(file="assets/images/qris.png")
                ttk.Label(self.detail_frame, image=self.qr_image).pack(pady=5)
            except:
                ttk.Label(
                    self.detail_frame,
                    text="[QRIS IMAGE NOT FOUND]",
                    foreground="red"
                ).pack()

    def process_payment(self):
        metode = self.metode_var.get()
        if metode == "":
            return

        if metode == "E-Wallet":
            nomor = self.nomor_ewallet.get()
            if nomor == "":
                return

        self.payment.save_payment(self.total, metode, self.meja_id)
        self.master.destroy()