import tkinter as tk
from tkinter import ttk
import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ReportWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Laporan Penjualan")
        self.window.state("zoomed")
        self.window.configure(bg="#f5f6fa")

        style = ttk.Style()
        style.configure("Header.TLabel", font=("Poppins", 18, "bold"))

        container = ttk.Frame(self.window, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Laporan Penjualan Bulanan",
            style="Header.TLabel"
        ).pack(pady=10)

        info = ttk.Label(
            container,
            text="Menampilkan total penjualan 3 bulan terakhir",
            foreground="#555"
        )
        info.pack(pady=(0, 10))

        self.chart_frame = ttk.Frame(container)
        self.chart_frame.pack(fill="both", expand=True)

        self.show_chart()

    def show_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        bulan = ["September", "Oktober", "November"]
        penjualan = [
            random.randint(7_000_000, 12_000_000),
            random.randint(7_000_000, 12_000_000),
            random.randint(7_000_000, 12_000_000),
        ]

        fig = Figure(figsize=(9, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(bulan, penjualan, marker="o")
        ax.set_title("Grafik Penjualan Bulanan")
        ax.set_ylabel("Total Penjualan (Rp)")
        ax.set_xlabel("Bulan")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
