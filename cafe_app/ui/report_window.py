import tkinter as tk
from tkinter import ttk, messagebox
from cafe_app.logika.report_model import ReportModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ReportWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Laporan Penjualan")
        self.master.geometry("950x620")
        self.master.resizable(False, False)
        
        self.report_model = ReportModel()

        # ===== Container utama =====
        container = ttk.Frame(self.master, padding=15)
        container.pack(fill="both", expand=True)

        # ===== Judul =====
        ttk.Label(
            container,
            text="Laporan Penjualan",
            font=("Poppins", 18, "bold")
        ).pack(pady=(0, 10))

        # ===== Filter Card =====
        filter_card = ttk.Frame(container, padding=10, relief="groove")
        filter_card.pack(fill="x", pady=5)

        ttk.Label(filter_card, text="Periode").grid(row=0, column=0, padx=5, sticky="w")
        self.filter_period = tk.StringVar()
        self.combo_period = ttk.Combobox(
            filter_card,
            textvariable=self.filter_period,
            values=["Harian", "Mingguan", "Bulanan"],
            state="readonly",
            width=15
        )
        self.combo_period.grid(row=0, column=1, padx=5)

        ttk.Label(filter_card, text="Metode").grid(row=0, column=2, padx=5, sticky="w")
        self.filter_pay = tk.StringVar()
        self.combo_payment = ttk.Combobox(
            filter_card,
            textvariable=self.filter_pay,
            values=["Semua", "Cash", "QRIS", "E-Wallet"],
            state="readonly",
            width=15
        )
        self.combo_payment.current(0)
        self.combo_payment.grid(row=0, column=3, padx=5)

        ttk.Button(
            filter_card,
            text="Tampilkan",
            command=self.show_report
        ).grid(row=0, column=4, padx=10)

        ttk.Button(
            filter_card,
            text="Tampilkan Grafik",
            command=self.show_chart
        ).grid(row=0, column=5, padx=5)

        # ===== Table Card =====
        table_card = ttk.Frame(container, padding=10)
        table_card.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(
            table_card,
            columns=("tanggal", "total", "metode", "meja", "status"),
            show="headings",
            height=12
        )

        self.tree.heading("tanggal", text="Tanggal")
        self.tree.heading("total", text="Total")
        self.tree.heading("metode", text="Pembayaran")
        self.tree.heading("meja", text="Meja")
        self.tree.heading("status", text="Status")

        self.tree.column("tanggal", width=120)
        self.tree.column("total", width=120, anchor="center")
        self.tree.column("metode", width=120, anchor="center")
        self.tree.column("meja", width=80, anchor="center")
        self.tree.column("status", width=100, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ===== Total =====
        self.label_total = ttk.Label(
            container,
            text="Total Pendapatan: Rp 0",
            font=("Poppins", 12, "bold")
        )
        self.label_total.pack(pady=5)

        ttk.Separator(container).pack(fill="x", pady=10)

        # ===== Grafik =====
        self.chart_frame = ttk.Frame(container, padding=10, relief="groove")
        self.chart_frame.pack(fill="both", expand=True)

    def show_report(self):
        period = self.filter_period.get()
        pay_method = self.filter_pay.get()

        if not period:
            messagebox.showwarning("Peringatan", "Pilih periode laporan.")
            return

        data = self.report_model.get_report(period)

        if pay_method != "Semua":
            data = [row for row in data if row[2].lower() == pay_method.lower()]

        for row in self.tree.get_children():
            self.tree.delete(row)

        for t in data:
            self.tree.insert("", tk.END, values=t)

        total_income = sum([row[1] for row in data]) if data else 0
        self.label_total.config(text=f"Total Pendapatan: Rp {total_income}")

    def show_chart(self):
        period = self.filter_period.get()
        pay_method = self.filter_pay.get()

        if not period:
            messagebox.showwarning("Peringatan", "Pilih periode grafik.")
            return

        data = self.report_model.get_report(period)

        if pay_method != "Semua":
            data = [row for row in data if row[2].lower() == pay_method.lower()]

        if not data:
            messagebox.showinfo("Info", "Tidak ada data untuk ditampilkan.")
            return

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        labels = [row[0] for row in data]
        totals = [row[1] for row in data]

        fig = Figure(figsize=(7, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(labels, totals, marker="o")
        ax.set_title(f"Grafik Pendapatan ({period})")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Total Pendapatan")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()