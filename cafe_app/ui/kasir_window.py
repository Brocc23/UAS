import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys
from datetime import datetime
import csv
import pandas as pd # Menggunakan pandas untuk kemudahan manipulasi data (optional, tapi disarankan)

# --- Dummy Imports/Constants (TIDAK BERUBAH) ---

# Konstanta Warna dan Font
COLORS = {
    "primary": "#4A90E2",
    "secondary": "#50E3C2",
    "success": "#7ED321",
    "danger": "#D0021B",
    "bg": "#F5F5F5",
    "card": "white",
    "text_dark": "#333333",
    "text_grey": "#666666",
    "input_bg": "#EEEEEE",
    "warning": "#F5A623",
}

# Monospace font ditambahkan untuk efek struk
FONTS = {
    "h1": ("Segoe UI", 16, "bold"),
    "h2": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "receipt_mono": ("Monospace", 10),
    "receipt_bold": ("Monospace", 10, "bold"),
    "receipt_h1": ("Monospace", 12, "bold"),
    "data_mono": ("Monospace", 9),
}

# Dummy Fungsi Utilitas
def show_error(message):
    messagebox.showerror("Error", message)

def setup_global_styles():
    style = ttk.Style()
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("TLabel", background=COLORS["bg"], font=FONTS["body"])
    style.configure("TButton", font=FONTS["body"])
    style.configure("TRadiobutton", background=COLORS["card"], font=FONTS["body"])
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", font=("Segoe UI", 9))

def create_card(parent):
    # Simulasi Card: Frame dengan padding dan border
    card = tk.Frame(parent, bg=COLORS["card"], padx=15, pady=15, relief="flat", bd=1)
    return card

def create_button(parent, text, command, type="default"):
    color_map = {
        "primary": COLORS["primary"],
        "success": COLORS["success"],
        "secondary": COLORS["secondary"],
        "danger": COLORS["danger"],
        "default": COLORS["text_grey"],
        "warning": COLORS["warning"],
    }
    
    btn = tk.Button(
        parent, 
        text=text, 
        command=command, 
        bg=color_map.get(type, COLORS["primary"]), 
        fg="white", 
        font=FONTS["h2"], 
        relief="flat", 
        pady=8
    )
    return btn

def create_entry_with_label(parent, label_text, text_var):
    frame = tk.Frame(parent, bg=COLORS["card"])
    frame.pack(fill="x", pady=5)
    
    tk.Label(
        frame, 
        text=label_text, 
        font=("Segoe UI", 9, "bold"), 
        bg=COLORS["card"], 
        fg=COLORS["text_grey"]
    ).pack(anchor="w")
    
    entry = tk.Entry(
        frame, 
        textvariable=text_var, 
        font=FONTS["body"], 
        bg=COLORS["input_bg"], 
        fg=COLORS["text_dark"], 
        relief="flat", 
        bd=1,
        insertbackground=COLORS["primary"],
        highlightthickness=1,
        highlightbackground=COLORS["text_grey"],
        highlightcolor=COLORS["primary"]
    )
    entry.pack(fill="x", ipady=5)
    return entry

def global_logout(current_window, root):
    if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
        current_window.destroy()
        # Jika ada window utama, tampilkan lagi (opsional)
        # root.deiconify() 
        pass

# --- Penentuan Path & Log (TIDAK BERUBAH) ---

def get_base_dir():
    """Mencoba mendapatkan direktori proyek utama."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.path[0])
    
    try:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except NameError:
        return os.getcwd()

BASE_DIR = get_base_dir()

# Path untuk QRIS
QRIS_FILENAME = "qris_dummy.png" 
QRIS_PATH = os.path.join(BASE_DIR, "assets", "images", QRIS_FILENAME)

# Path untuk Log Transaksi
LOG_FILE = os.path.join(BASE_DIR, "data", "transaksi_log.csv")

# --- NEW: Fungsi Utilitas Log ---

def log_transaction(data):
    """Mencatat transaksi ke file CSV."""
    # Pastikan direktori 'data' ada
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Headers untuk CSV
    fieldnames = ['timestamp', 'tanggal', 'waktu', 'total', 'metode', 'kasir']
    
    # Cek apakah file sudah ada, jika tidak, tulis header
    file_exists = os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0

    with open(LOG_FILE, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(data)
    
    # print(f"LOG SUCCESS: {data}")


# --- NEW: Kelas LaporanWindow ---

class LaporanWindow:
    def __init__(self, root, parent_window):
        self.root = root
        self.parent_window = parent_window
        
        self.window = tk.Toplevel(parent_window)
        self.window.title("Laporan Harian")
        self.window.geometry("800x600")
        self.window.configure(bg=COLORS["bg"])
        self.window.transient(parent_window) # Jaga agar window tetap di atas parent
        
        self.build_ui()
        self.load_data()

    def build_ui(self):
        container = tk.Frame(self.window, bg=COLORS["bg"], padx=20, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(
            container, 
            text="LAPORAN HASIL PENJUALAN", 
            font=FONTS["h1"], 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        ).pack(pady=(0, 20))
        
        # Ringkasan Total
        self.summary_card = create_card(container)
        self.summary_card.pack(fill="x", pady=10)
        
        tk.Label(self.summary_card, text=f"Ringkasan Penjualan Hari Ini ({datetime.now().strftime('%Y-%m-%d')})", 
                 font=FONTS["h2"], bg=COLORS["card"], fg=COLORS["text_dark"]).pack(anchor="w")

        self.lbl_total = tk.Label(self.summary_card, text="TOTAL KESELURUHAN: Rp 0", 
                                  font=FONTS["h1"], bg=COLORS["card"], fg=COLORS["primary"], pady=5)
        self.lbl_total.pack(anchor="w", pady=(10, 0))

        self.lbl_qris = tk.Label(self.summary_card, text="QRIS: Rp 0", 
                                  font=FONTS["body"], bg=COLORS["card"], fg=COLORS["text_dark"])
        self.lbl_qris.pack(anchor="w")

        self.lbl_tunai = tk.Label(self.summary_card, text="TUNAI: Rp 0", 
                                  font=FONTS["body"], bg=COLORS["card"], fg=COLORS["text_dark"])
        self.lbl_tunai.pack(anchor="w")

        # Frame untuk Tabel Detail
        detail_frame = create_card(container)
        detail_frame.pack(fill="both", expand=True, pady=10)
        
        tk.Label(detail_frame, text="Detail Transaksi Hari Ini", 
                 font=FONTS["h2"], bg=COLORS["card"], fg=COLORS["text_dark"]).pack(anchor="w", pady=(0, 10))
        
        # Treeview (Tabel)
        columns = ("#1", "#2", "#3", "#4")
        self.tree = ttk.Treeview(detail_frame, columns=columns, show="headings")
        self.tree.heading("#1", text="Waktu")
        self.tree.heading("#2", text="Total")
        self.tree.heading("#3", text="Metode")
        self.tree.heading("#4", text="Kasir")
        
        # Pengaturan lebar kolom
        self.tree.column("#1", width=100, anchor="center")
        self.tree.column("#2", width=150, anchor="e")
        self.tree.column("#3", width=80, anchor="center")
        self.tree.column("#4", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        vsb = ttk.Scrollbar(detail_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")


    def load_data(self):
        # Bersihkan tabel lama
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not os.path.exists(LOG_FILE):
            self.lbl_total.config(text="TOTAL KESELURUHAN: Rp 0")
            self.lbl_qris.config(text="QRIS: Rp 0")
            self.lbl_tunai.config(text="TUNAI: Rp 0")
            tk.Label(self.tree, text="Belum ada data transaksi hari ini.").pack(pady=20)
            return

        try:
            # Gunakan pandas untuk membaca dan memfilter data
            df = pd.read_csv(LOG_FILE)
            today_str = datetime.now().strftime('%Y-%m-%d')
            
            # Filter hanya data hari ini
            df_today = df[df['tanggal'] == today_str].copy()
            
            if df_today.empty:
                self.lbl_total.config(text="TOTAL KESELURUHAN: Rp 0")
                self.lbl_qris.config(text="QRIS: Rp 0")
                self.lbl_tunai.config(text="TUNAI: Rp 0")
                return

            # Konversi kolom 'total' ke numerik (jika belum)
            df_today['total'] = pd.to_numeric(df_today['total'], errors='coerce').fillna(0).astype(int)

            # Hitung Total Keseluruhan
            total_sum = df_today['total'].sum()
            
            # Hitung Total per Metode
            grouped_sum = df_today.groupby('metode')['total'].sum()
            total_qris = grouped_sum.get('QRIS', 0)
            total_tunai = grouped_sum.get('TUNAI', 0)
            
            # Update Ringkasan
            self.lbl_total.config(text=f"TOTAL KESELURUHAN: Rp {total_sum:,.0f}")
            self.lbl_qris.config(text=f"QRIS: Rp {total_qris:,.0f}")
            self.lbl_tunai.config(text=f"TUNAI: Rp {total_tunai:,.0f}")

            # Isi Treeview (Tabel)
            for index, row in df_today.iterrows():
                self.tree.insert("", "end", values=(
                    row['waktu'], 
                    f"Rp {row['total']:,.0f}", 
                    row['metode'], 
                    row['kasir']
                ))

        except Exception as e:
            show_error(f"Gagal memuat data log: {e}")
            self.lbl_total.config(text="TOTAL KESELURUHAN: GAGAL MEMUAT DATA")


# --- Kelas KasirWindow (MODIFIKASI: Penambahan Laporan dan Logging) ---

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
        
        self.uang_diterima_var = tk.StringVar()
        self.kembalian_var = tk.StringVar(value="Rp 0")
        
        self.qr_photo = None 

        self.build_ui()

    def open_laporan_window(self):
        """Membuka window laporan harian."""
        LaporanWindow(self.root, self.window)

    def build_ui(self):
        container = tk.Frame(self.window, bg=COLORS["bg"], padx=20, pady=20)
        container.pack(fill="both", expand=True)
        
        # Header dan Logout
        header_frame = tk.Frame(container, bg=COLORS["bg"])
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            header_frame, 
            text="KASIR MANUAL", 
            font=FONTS["h1"], 
            bg=COLORS["bg"], 
            fg=COLORS["primary"]
        ).pack(side="left")

        # Tombol Log Out
        tk.Button(
            header_frame, 
            text="Log Out", 
            command=lambda: global_logout(self.window, self.root), 
            bg=COLORS["danger"], 
            fg="white", 
            relief="flat", 
            padx=10
        ).pack(side="right", padx=(10, 0))
        
        # Tombol Laporan Harian
        tk.Button(
            header_frame, 
            text="Laporan Harian", 
            command=self.open_laporan_window, 
            bg=COLORS["warning"], 
            fg="white", 
            relief="flat", 
            padx=10
        ).pack(side="right")


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
        
        # Tombol Tampilkan Struk
        create_button(btn_container, "TAMPILKAN STRUK", self.tampilkan_struk, "success").pack(fill="x", pady=(10,0))

        # Result Area
        self.result_frame = tk.Frame(card, bg=COLORS["card"])
        self.result_frame.pack(fill="both", expand=True, pady=10)

    def hitung_kembalian(self, total_tagihan):
        """Menghitung dan menampilkan kembalian saat metode pembayaran Tunai."""
        uang_diterima_str = self.uang_diterima_var.get()
        uang_diterima_str = uang_diterima_str.replace(',', '').replace('.', '')

        if not uang_diterima_str.isdigit() or not uang_diterima_str:
            show_error("Uang diterima harus berupa angka yang valid.")
            self.kembalian_var.set("Rp 0")
            return
        
        try:
            uang_diterima = int(uang_diterima_str)
        except ValueError:
            show_error("Uang diterima harus berupa bilangan bulat.")
            self.kembalian_var.set("Rp 0")
            return
            
        kembalian = uang_diterima - total_tagihan
        
        self.kembalian_var.set(f"Rp {kembalian:,.0f}")
        
        if kembalian < 0:
            show_error(f"Uang diterima kurang! Kurang: Rp {abs(kembalian):,.0f}")

    def proses_pembayaran(self):
        for w in self.result_frame.winfo_children():
            w.destroy()

        total_str = self.total_var.get()
        total_str_clean = total_str.replace(',', '').replace('.', '')
        
        if not total_str_clean.isdigit() or not total_str_clean:
            show_error("Total tagihan harus berupa angka yang valid.")
            return

        total = int(total_str_clean)
        metode = self.metode.get()

        if metode == "QRIS":
            self.show_qris(total)
            # LOGGING DI SINI: QRIS dianggap sukses setelah QR ditampilkan
            self.finalize_transaction(total, metode)
            
        else: # TUNAI
            self.show_tunai(total)
            self.finalize_transaction(total, metode)


    def finalize_transaction(self, total, metode):
        """Fungsi pembantu untuk mencatat transaksi."""
        now = datetime.now()
        data = {
            'timestamp': now.isoformat(),
            'tanggal': now.strftime('%Y-%m-%d'),
            'waktu': now.strftime('%H:%M:%S'),
            'total': total,
            'metode': metode,
            'kasir': self.user.get("username", "UNKNOWN")
        }
        log_transaction(data)

    def show_qris(self, total):
        # ... (Kode show_qris tidak banyak berubah, hanya tampilan) ...
        tk.Label(
            self.result_frame,
            text="Silakan Scan QRIS ini",
            font=FONTS["h2"],
            bg=COLORS["card"],
            fg=COLORS["text_dark"]
        ).pack(pady=10)

        if not os.path.exists(QRIS_PATH):
            tk.Label(self.result_frame, text=f"Gambar QRIS tidak ditemukan di path: {QRIS_PATH}", fg=COLORS["danger"], bg=COLORS["card"]).pack()
            return

        try:
            img = Image.open(QRIS_PATH)
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            self.qr_photo = ImageTk.PhotoImage(img)
            
            tk.Label(self.result_frame, image=self.qr_photo, bg=COLORS["card"]).pack(pady=10)
        except Exception as e:
            tk.Label(self.result_frame, text=f"Error memuat QRIS: {e}", fg=COLORS["danger"], bg=COLORS["card"]).pack()

        tk.Label(
            self.result_frame,
            text=f"Total: Rp {total:,.0f}",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack(pady=10)

    def show_tunai(self, total):
        # ... (Kode show_tunai tidak berubah) ...
        self.uang_diterima_var.set("")
        self.kembalian_var.set("Rp 0")

        tk.Label(
            self.result_frame,
            text="Pembayaran Tunai",
            font=FONTS["h2"],
            bg=COLORS["card"],
            fg=COLORS["text_dark"]
        ).pack(pady=20)

        tk.Label(
            self.result_frame,
            text=f"Tagihan: Rp {total:,.0f}",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack()

        create_entry_with_label(
            self.result_frame, 
            "Uang Diterima (Rp)", 
            self.uang_diterima_var
        )

        create_button(
            self.result_frame, 
            "HITUNG KEMBALIAN", 
            lambda: self.hitung_kembalian(total), 
            "secondary"
        ).pack(fill="x", pady=(10, 5))

        tk.Label(
            self.result_frame,
            text="Kembalian:",
            font=FONTS["body"],
            bg=COLORS["card"],
            fg=COLORS["text_dark"]
        ).pack(pady=(10, 0))
        
        tk.Label(
            self.result_frame,
            textvariable=self.kembalian_var, 
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["success"]
        ).pack()
        
        tk.Label(
            self.result_frame,
            text="Mohon terima uang dari pelanggan dan berikan kembalian.",
            font=FONTS["body"],
            bg=COLORS["card"],
            fg=COLORS["text_grey"],
            wraplength=300,
            justify="center"
        ).pack(pady=10)

    def tampilkan_struk(self):
        # ... (Kode tampilkan_struk tidak berubah) ...
        total_str = self.total_var.get()
        total_str_clean = total_str.replace(',', '').replace('.', '')
        
        if not total_str_clean.isdigit() or not total_str_clean:
            messagebox.showwarning("Peringatan Struk", "Total tagihan belum diisi atau tidak valid.")
            return

        total = int(total_str_clean)
        metode = self.metode.get()
        
        uang_diterima = 0
        kembalian = 0
        
        if metode == "TUNAI":
            uang_diterima_str = self.uang_diterima_var.get()
            uang_diterima_str_clean = uang_diterima_str.replace(',', '').replace('.', '')
            
            if uang_diterima_str_clean.isdigit():
                uang_diterima = int(uang_diterima_str_clean)
                kembalian = uang_diterima - total
            
            if uang_diterima == 0 and total > 0:
                 messagebox.showwarning("Peringatan Struk", "Struk Tunai dibuat, namun Uang Diterima belum dihitung/diinput.")
        
        struk_win = tk.Toplevel(self.window)
        struk_win.title("Struk Pembayaran")
        struk_win.geometry("300x450")
        struk_win.configure(bg="white")
        
        content_frame = tk.Frame(struk_win, bg="white", padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)
        
        def print_receipt_row(parent, label, value, row_index, font=FONTS["receipt_mono"], fg=COLORS["text_dark"]):
            tk.Label(parent, text=label, font=font, bg="white", fg=fg, anchor="w").grid(row=row_index, column=0, sticky="w")
            tk.Label(parent, text=f"Rp {value:,.0f}", font=font, bg="white", fg=fg, anchor="e").grid(row=row_index, column=1, sticky="e")
            parent.grid_columnconfigure(1, weight=1)

        tk.Label(content_frame, text="Café Sogok", font=FONTS["receipt_h1"], bg="white", fg=COLORS["text_dark"]).pack(pady=(0, 5))
        tk.Label(content_frame, text="Jl. Bebas No. 12", font=FONTS["receipt_mono"], bg="white").pack()
        tk.Label(content_frame, text=f"Kasir: {self.user.get('username', 'UNKNOWN')}", font=FONTS["receipt_mono"], bg="white").pack(pady=(0, 10))
        
        tk.Label(content_frame, text="--------------------------------", font=FONTS["receipt_mono"], bg="white").pack(fill="x", pady=5)
        
        summary_frame = tk.Frame(content_frame, bg="white")
        summary_frame.pack(fill="x")
        
        row_idx = 0
        
        print_receipt_row(summary_frame, "TOTAL TAGIHAN", total, row_idx, font=FONTS["receipt_h1"])
        row_idx += 1
        
        if metode == "TUNAI":
            tk.Label(content_frame, text="--------------------------------", font=FONTS["receipt_mono"], bg="white").pack(fill="x", pady=5)
            
            print_receipt_row(summary_frame, "Uang Diterima", uang_diterima, row_idx, font=FONTS["receipt_mono"])
            row_idx += 1
            
            print_receipt_row(summary_frame, "KEMBALIAN", kembalian, row_idx, font=FONTS["receipt_bold"], fg=COLORS["success"])
            row_idx += 1
        
        tk.Label(content_frame, text="--------------------------------", font=FONTS["receipt_mono"], bg="white").pack(fill="x", pady=5)

        tk.Label(content_frame, text=f"Metode: {metode}", font=FONTS["receipt_mono"], bg="white", anchor="w").pack(fill="x")
        tk.Label(content_frame, text=f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=FONTS["receipt_mono"], bg="white", anchor="w").pack(fill="x")

        tk.Label(content_frame, text="\n*** Terima kasih ***", font=FONTS["receipt_bold"], bg="white", fg=COLORS["text_dark"]).pack(pady=(15, 5))
        
        tk.Button(struk_win, text="Tutup", command=struk_win.destroy, bg=COLORS["primary"], fg="white").pack(pady=10)


if __name__ == '__main__':
    # Contoh penggunaan standalone
    root = tk.Tk()
    root.withdraw()

    # Pastikan direktori data ada
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    
    # Membuat file dummy QRIS jika tidak ditemukan
    qris_dir = os.path.dirname(QRIS_PATH)
    if not os.path.exists(QRIS_PATH):
        try:
            os.makedirs(qris_dir, exist_ok=True)
            dummy_png = Image.new('RGB', (200, 200), color = 'white')
            dummy_png.save(QRIS_PATH)
        except Exception:
             pass

    dummy_user = {"username": "aldi.kasir"} 
    
    app = KasirWindow(root, dummy_user)
    root.mainloop()