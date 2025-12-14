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
            text="Laporan Penjualan (Dummy)",
            style="Header.TLabel"
        ).pack(pady=10)

        # ===== CONTROL =====
        control = ttk.Frame(container)
        control.pack(pady=10)

        ttk.Label(control, text="Periode:").pack(side="left", padx=5)

        self.periode = ttk.Combobox(
            control,
            values=["Harian", "Mingguan", "Bulanan"],
            state="readonly",
            width=15
        )
        self.periode.pack(side="left", padx=5)
        self.periode.current(2)

        ttk.Button(
            control,
            text="Tampilkan Laporan",
            command=self.show_chart
        ).pack(side="left", padx=10)

        # ===== CHART AREA (kosong awalnya) =====
        self.chart_frame = ttk.Frame(container)
        self.chart_frame.pack(fill="both", expand=True)

    def show_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        bulan = ["Jan", "Feb", "Mar", "Apr", "Mei"]
        penjualan = [random.randint(4_000_000, 15_000_000) for _ in bulan]

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(bulan, penjualan, marker="o")
        ax.set_title("Grafik Penjualan")
        ax.set_ylabel("Total (Rp)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
