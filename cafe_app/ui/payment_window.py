import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from cafe_app.logika import payment_model


class PaymentWindow:
    def __init__(self, master, total, meja_id=None):
        self.master = master
        self.master.title("Pembayaran")
        self.master.geometry("450x400")

        self.total = total
        self.meja_id = meja_id
        self.payment = PaymentModel()

        frame = ttk.Frame(master, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"Total Tagihan: Rp{total:,}", font=("Poppins", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Pilih Metode Pembayaran:", font=("Poppins", 12)).pack(pady=5)

        self.metode_var = tk.StringVar()
        metode_box = ttk.Combobox(frame, textvariable=self.metode_var, state="readonly",
                                  values=["Cash", "E-Wallet", "QRIS"])
        metode_box.pack(pady=5)
        metode_box.bind("<<ComboboxSelected>>", self.show_detail)

        self.detail_frame = ttk.Frame(frame)
        self.detail_frame.pack(pady=10)

        self.pay_btn = ttk.Button(frame, text="Bayar Sekarang", command=self.process_payment)
        self.pay_btn.pack(pady=12)

        self.qr_image = None

    def clear_detail(self):
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

    def show_detail(self, _):
        self.clear_detail()
        metode = self.metode_var.get()

        if metode == "Cash":
            ttk.Label(self.detail_frame, text="Bayar di kasir.", font=("Poppins", 12)).pack()

        elif metode == "E-Wallet":
            ttk.Label(self.detail_frame, text="Masukkan nomor E-Wallet:", font=("Poppins", 12)).pack(pady=3)
            self.nomor_ewallet = tk.StringVar()
            ttk.Entry(self.detail_frame, textvariable=self.nomor_ewallet).pack()

        elif metode == "QRIS":
            try:
                self.qr_image = PhotoImage(file="assets/images/qris.png")
                ttk.Label(self.detail_frame, image=self.qr_image).pack()
            except:
                ttk.Label(self.detail_frame, text="[QRIS IMAGE NOT FOUND]").pack()

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
