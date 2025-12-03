import tkinter as tk
from tkinter import ttk
from cafe_app.ui.report_window import report_window
from cafe_app.ui.admin_window import admin_window
from cafe_app.ui.kasir_window import kasir_window

class OwnerWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Owner Panel")
        self.master.geometry("500x350")

        frame = ttk.Frame(master, padding=20)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="Owner Dashboard", font=("Poppins", 20, "bold"))
        title.pack(pady=10)

        ttk.Button(frame, text="Kelola Menu & Data", width=30,
                   command=self.buka_admin).pack(pady=8)

        ttk.Button(frame, text="Lihat Laporan Transaksi", width=30,
                   command=self.buka_laporan).pack(pady=8)

        ttk.Button(frame, text="Simulasi Kasir", width=30,
                   command=self.buka_kasir).pack(pady=8)

        ttk.Button(frame, text="Logout", width=30,
                   command=self.master.destroy).pack(pady=8)

    def buka_admin(self):
        AdminWindow(tk.Toplevel(self.master))

    def buka_laporan(self):
        ReportWindow(tk.Toplevel(self.master))

    def buka_kasir(self):
        KasirWindow(tk.Toplevel(self.master))
