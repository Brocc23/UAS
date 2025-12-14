import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from cafe_app.utils import show_error
from cafe_app.ui.style_utils import COLORS, FONTS, setup_global_styles, create_card, create_button, create_entry_with_label

QRIS_PATH = r"cafe_app\assets\images\qris_dummy.png"

class KasirWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.window = tk.Toplevel(root)
        self.window.title("Kasir - Café App")
        self.window.geometry("600x800")
        self.window.configure(bg=COLORS["bg"])
        
        setup_global_styles()

        self.metode = tk.StringVar(value="QRIS")
        self.total_var = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        # Center Container
        container = tk.Frame(self.window, bg=COLORS["bg"], padx=20, pady=20)
        container.pack(fill="both", expand=True)
        
        # Header
        tk.Label(
            container, 
            text="KASIR MANUAL", 
            font=FONTS["h1"], 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))

        # Main Card
        card = create_card(container)
        card.pack(fill="both", expand=True)

        # Input Total
        create_entry_with_label(card, "Total Tagihan (Rp)", self.total_var)

        # Metode Pembayaran
        tk.Label(
            card, 
            text="Metode Pembayaran", 
            font=("Segoe UI", 9, "bold"), 
            bg=COLORS["card"], 
            fg=COLORS["text_grey"]
        ).pack(anchor="w", pady=(20, 10))

        style = ttk.Style()
        style.configure("TRadiobutton", background=COLORS["card"], font=FONTS["body"])

        # Radio Buttons
        frame_radio = tk.Frame(card, bg=COLORS["card"])
        frame_radio.pack(fill="x")
        
        ttk.Radiobutton(frame_radio, text="QRIS (Scan)", variable=self.metode, value="QRIS").pack(anchor="w", pady=5)
        ttk.Radiobutton(frame_radio, text="Tunai / Cash", variable=self.metode, value="TUNAI").pack(anchor="w", pady=5)

        # Process Button
        btn_container = tk.Frame(card, bg=COLORS["card"])
        btn_container.pack(fill="x", pady=30)
        
        create_button(btn_container, "PROSES PEMBAYARAN", self.proses_pembayaran, "primary").pack(fill="x")

        # Result Area
        self.result_frame = tk.Frame(card, bg=COLORS["card"])
        self.result_frame.pack(fill="both", expand=True, pady=10)

    def proses_pembayaran(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

        total = self.total_var.get()
        if not total.isdigit():
            show_error("Total harus berupa angka")
            return

        total = int(total)

        if self.metode.get() == "QRIS":
            self.show_qris(total)
        else:
            self.show_tunai(total)

    def show_qris(self, total):
        tk.Label(
            self.result_frame,
            text="Silakan Scan QRIS ini",
            font=FONTS["h2"],
            bg=COLORS["card"],
            fg=COLORS["text_dark"]
        ).pack(pady=10)

        if not os.path.exists(QRIS_PATH):
            tk.Label(self.result_frame, text="Gambar QRIS tidak ditemukan", fg=COLORS["danger"], bg=COLORS["card"]).pack()
            return

        try:
            img = Image.open(QRIS_PATH)
            img = img.resize((200, 200))
            self.qr_photo = ImageTk.PhotoImage(img)
            
            tk.Label(self.result_frame, image=self.qr_photo, bg=COLORS["card"]).pack(pady=10)
        except Exception as e:
            tk.Label(self.result_frame, text=f"Error: {e}", fg=COLORS["danger"], bg=COLORS["card"]).pack()

        tk.Label(
            self.result_frame,
            text=f"Total: Rp {total:,}",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack(pady=10)

    def show_tunai(self, total):
        tk.Label(
            self.result_frame,
            text="Pembayaran Tunai",
            font=FONTS["h2"],
            bg=COLORS["card"],
            fg=COLORS["text_dark"]
        ).pack(pady=20)

        tk.Label(
            self.result_frame,
            text=f"Tagihan: Rp {total:,}",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack()
        
        tk.Label(
            self.result_frame,
            text="Mohon terima uang dari pelanggan dan berikan kembalian jika perlu.",
            font=FONTS["body"],
            bg=COLORS["card"],
            fg=COLORS["text_grey"],
            wraplength=300,
            justify="center"
        ).pack(pady=10)
