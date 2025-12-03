import tkinter as tk
from tkinter import ttk, messagebox
from cafe_app.logika.report_model import report_model

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ReportWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Laporan Penjualan")
        self.master.geometry("900x600")

        self.report_model = ReportModel()

        filter_frame = tk.Frame(self.master)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter Periode:").grid(row=0, column=0, padx=5)
        self.filter_period = tk.StringVar()
        self.combo_period = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_period,
            values=["Harian", "Mingguan", "Bulanan"],
            state="readonly",
            width=15
        )
        self.combo_period.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Metode:").grid(row=0, column=2, padx=5)
        self.filter_pay = tk.StringVar()
        self.combo_payment = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_pay,
            values=["Semua", "Cash", "QRIS", "E-Wallet"],
            state="readonly",
            width=15
        )
        self.combo_payment.current(0)
        self.combo_payment.grid(row=0, column=3, padx=5)

        btn_show = tk.Button(filter_frame, text="Tampilkan", command=self.show_report)
        btn_show.grid(row=0, column=4, padx=10)

        btn_chart = tk.Button(filter_frame, text="Tampilkan Grafik", command=self.show_chart)
        btn_chart.grid(row=0, column=5, padx=10)

        self.tree = ttk.Treeview(
            self.master,
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
        self.tree.column("total", width=90)
        self.tree.column("metode", width=120)
        self.tree.column("meja", width=80)
        self.tree.column("status", width=100)

        self.tree.pack(pady=10)

        self.label_total = tk.Label(self.master, text="Total Pendapatan: Rp 0", font=("Arial", 12, "bold"))
        self.label_total.pack()

        self.chart_frame = tk.Frame(self.master)
        self.chart_frame.pack(pady=10)

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

        if not period:
            messagebox.showwarning("Peringatan", "Pilih periode untuk grafik.")
            return

        data = self.report_model.get_report(period)

        if not data:
            messagebox.showinfo("Info", "Tidak ada data untuk ditampilkan pada grafik.")
            return

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        dates = [row[0] for row in data]
        totals = [row[1] for row in data]

        fig = Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, totals, marker="o")
        ax.set_title("Grafik Penjualan")
        ax.set_ylabel("Total Pendapatan")
        ax.set_xlabel("Tanggal")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
