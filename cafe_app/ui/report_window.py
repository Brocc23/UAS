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
            text="LAPORAN PENJUALAN",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 10))

        tk.Label(
            card,
            text="Pilih periode penjualan:",
            font=FONTS["body"],
            bg=COLORS["card"],
            fg=COLORS["text_grey"]
        ).pack(pady=(0, 10))

        # Pilihan periode: Harian / Mingguan / Bulanan
        self.periode_var = tk.StringVar(value="BULANAN")
        periode_frame = tk.Frame(card, bg=COLORS["card"])
        periode_frame.pack(pady=(0, 20))

        ttk.Radiobutton(periode_frame, text="Harian", variable=self.periode_var, value="HARI").pack(side="left", padx=10)
        ttk.Radiobutton(periode_frame, text="Mingguan", variable=self.periode_var, value="MINGGU").pack(side="left", padx=10)
        ttk.Radiobutton(periode_frame, text="Bulanan", variable=self.periode_var, value="BULANAN").pack(side="left", padx=10)

        self.chart_frame = tk.Frame(card, bg=COLORS["card"])
        self.chart_frame.pack(fill="both", expand=True)

        # Tombol refresh chart
        tk.Button(card, text="Tampilkan Grafik", command=self.show_chart, bg=COLORS["primary"], fg="white").pack(pady=(10,0))

        self.show_chart()

    def show_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        periode = self.periode_var.get()
        if periode == "HARI":
            labels = [f"Hari {i+1}" for i in range(7)]  # misal 7 hari terakhir
            values = [random.randint(500_000, 1_500_000) for _ in range(7)]
        elif periode == "MINGGU":
            labels = [f"Minggu {i+1}" for i in range(4)]  # 4 minggu terakhir
            values = [random.randint(3_000_000, 5_000_000) for _ in range(4)]
        else:  # BULANAN
            labels = ["September", "Oktober", "November"]
            values = [random.randint(7_000_000, 12_000_000) for _ in range(3)]

        fig = Figure(figsize=(9, 4.5), dpi=100, facecolor=COLORS["card"])
        ax = fig.add_subplot(111)
        ax.set_facecolor("#fcfcfc")
        ax.plot(labels, values, marker="o", color=COLORS["primary"], linewidth=2, markersize=8)

        ax.set_title(f"Grafik Penjualan {periode.capitalize()}", fontsize=12, pad=15, color=COLORS["text_dark"])
        ax.set_ylabel("Total Penjualan (Rp)", color=COLORS["text_grey"])
        
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
