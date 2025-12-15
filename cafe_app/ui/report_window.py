import tkinter as tk
from tkinter import ttk
import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from cafe_app.ui.style_utils import COLORS, FONTS, setup_global_styles, create_card

class ReportWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Laporan Penjualan")
        self.window.state("zoomed")
        self.window.configure(bg=COLORS["bg"])

        setup_global_styles()

        container = tk.Frame(self.window, bg=COLORS["bg"], padx=20, pady=20)
        container.pack(fill="both", expand=True)

        card = create_card(container)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="LAPORAN PENJUALAN BULANAN",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 10))

        tk.Label(
            card,
            text="Menampilkan total penjualan 3 bulan terakhir",
            font=FONTS["body"],
            bg=COLORS["card"],
            fg=COLORS["text_grey"]
        ).pack(pady=(0, 20))

        self.chart_frame = tk.Frame(card, bg=COLORS["card"])
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

        fig = Figure(figsize=(9, 4.5), dpi=100, facecolor=COLORS["card"])
        ax = fig.add_subplot(111)
        ax.set_facecolor("#fcfcfc")
        ax.plot(bulan, penjualan, marker="o", color=COLORS["primary"], linewidth=2, markersize=8)
        
        ax.set_title("Grafik Penjualan", fontsize=12, pad=15, color=COLORS["text_dark"])
        ax.set_ylabel("Total Penjualan (Rp)", color=COLORS["text_grey"])
        
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
