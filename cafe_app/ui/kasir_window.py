import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# --- Dummy Imports/Constants untuk Menjalankan Kode Secara Mandiri ---

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
}

FONTS = {
    "h1": ("Segoe UI", 16, "bold"),
    "h2": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
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
        "default": COLORS["text_grey"]
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
        # Jika root adalah window utama, ia akan tetap terbuka, biasanya kita akan menampilkan 
        # jendela login lagi di aplikasi penuh.
        # Di sini kita hanya menutup top level window.
        pass

# --- Path Gambar QRIS (Sesuaikan jika Anda ingin menguji) ---
# Ubah path ini ke lokasi gambar QRIS dummy Anda. 
# Untuk pengujian mandiri, Anda mungkin perlu mengubahnya menjadi path relatif yang sesuai 
# atau menempatkan gambar di folder yang sama.
QRIS_PATH = "qris_dummy.png" # Ganti dengan nama file gambar dummy Anda

# Jika Anda tidak memiliki file qris_dummy.png, Anda bisa membuat dummy file PNG kosong 
# atau mengomentari bagian QRIS untuk pengujian.

# --- Kelas KasirWindow ---

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
        
        # Tambahan untuk Tunai
        self.uang_diterima_var = tk.StringVar()
        self.kembalian_var = tk.StringVar(value="Rp 0")
        
        # Simpan referensi photo agar tidak dihapus garbage collector
        self.qr_photo = None 

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
        
        tk.Button(
            container, 
            text="Log Out", 
            command=lambda: global_logout(self.window, self.root), 
            bg=COLORS["danger"], 
            fg="white", 
            relief="flat", 
            padx=10
        ).place(relx=1.0, rely=0.0, anchor="ne")

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
        
        if not uang_diterima_str.isdigit():
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
        
        self.kembalian_var.set(f"Rp {kembalian:,}")
        
        if kembalian < 0:
            show_error(f"Uang diterima kurang! Kurang: Rp {abs(kembalian):,}")

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
            tk.Label(self.result_frame, text=f"Gambar QRIS tidak ditemukan di: {QRIS_PATH}", fg=COLORS["danger"], bg=COLORS["card"]).pack()
            return

        try:
            img = Image.open(QRIS_PATH)
            img = img.resize((200, 200))
            self.qr_photo = ImageTk.PhotoImage(img)
            
            tk.Label(self.result_frame, image=self.qr_photo, bg=COLORS["card"]).pack(pady=10)
        except Exception as e:
            tk.Label(self.result_frame, text=f"Error memuat QRIS: {e}", fg=COLORS["danger"], bg=COLORS["card"]).pack()

        tk.Label(
            self.result_frame,
            text=f"Total: Rp {total:,}",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack(pady=10)

    def show_tunai(self, total):
        # Reset input dan kembalian
        self.uang_diterima_var.set("")
        self.kembalian_var.set("Rp 0")

        tk.Label(
            self.result_frame,
            text="Pembayaran Tunai",
            font=FONTS["h2"],
            bg=COLORS["card"],
            fg=COLORS["text_dark"]
        ).pack(pady=20)

        # Tampilkan Tagihan
        tk.Label(
            self.result_frame,
            text=f"Tagihan: Rp {total:,}",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack()

        # Input Uang Diterima
        create_entry_with_label(
            self.result_frame, 
            "Uang Diterima (Rp)", 
            self.uang_diterima_var
        )

        # Tombol Hitung Kembalian
        create_button(
            self.result_frame, 
            "HITUNG KEMBALIAN", 
            lambda: self.hitung_kembalian(total), 
            "secondary"
        ).pack(fill="x", pady=(10, 5))

        # Tampilkan Kembalian
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
        total = self.total_var.get()
        if not total.isdigit():
            show_error("Total harus berupa angka")
            return

        total = int(total)
        metode = self.metode.get()
        
        uang_diterima = 0
        kembalian = 0
        
        # Ambil data uang diterima/kembalian hanya jika metode Tunai
        if metode == "TUNAI":
            uang_diterima_str = self.uang_diterima_var.get()
            if uang_diterima_str.isdigit():
                uang_diterima = int(uang_diterima_str)
                kembalian = uang_diterima - total
            
            if uang_diterima == 0 and total > 0:
                 messagebox.showwarning("Peringatan Struk", "Struk Tunai dibuat, namun Uang Diterima belum dihitung/diinput.")
        

        # Window baru untuk struk
        struk_win = tk.Toplevel(self.window)
        struk_win.title("Struk Pembayaran")
        struk_win.geometry("300x450")
        struk_win.configure(bg="white")

        tk.Label(struk_win, text="STRUK PEMBAYARAN", font=FONTS["h2"], bg="white", fg=COLORS["primary"]).pack(pady=10)
        tk.Label(struk_win, text=f"Metode: {metode}", font=FONTS["body"], bg="white").pack(pady=5)
        
        # --- Detail Transaksi ---
        tk.Label(struk_win, text="------------------------------", bg="white").pack()
        tk.Label(struk_win, text=f"Total Tagihan:", font=FONTS["body"], bg="white", anchor="w").pack(fill="x", padx=20)
        tk.Label(struk_win, text=f"Rp {total:,}", font=FONTS["h1"], bg="white", fg=COLORS["text_dark"]).pack(pady=(0, 5))
        
        if metode == "TUNAI":
            tk.Label(struk_win, text=f"Uang Diterima:", font=FONTS["body"], bg="white", anchor="w").pack(fill="x", padx=20)
            tk.Label(struk_win, text=f"Rp {uang_diterima:,}", font=FONTS["h2"], bg="white").pack(pady=(0, 5))
            
            tk.Label(struk_win, text="------------------------------", bg="white").pack()
            tk.Label(struk_win, text=f"Kembalian:", font=FONTS["body"], bg="white", anchor="w").pack(fill="x", padx=20)
            tk.Label(struk_win, text=f"Rp {kembalian:,}", font=FONTS["h1"], bg="white", fg=COLORS["success"]).pack(pady=(0, 10))
        # --- Akhir Detail Transaksi ---

        tk.Label(struk_win, text="Terima kasih telah berbelanja!", font=FONTS["body"], bg="white").pack(pady=20)
        tk.Button(struk_win, text="Tutup", command=struk_win.destroy, bg=COLORS["primary"], fg="white").pack(pady=10)


if __name__ == '__main__':
    # Contoh penggunaan standalone
    root = tk.Tk()
    root.withdraw()  # Sembunyikan window root utama

    # Buat dummy file QRIS jika tidak ada untuk menghindari error saat mencoba load
    if not os.path.exists(QRIS_PATH):
        try:
            dummy_png = Image.new('RGB', (1, 1), color = 'white')
            dummy_png.save(QRIS_PATH)
            print(f"File dummy '{QRIS_PATH}' dibuat.")
        except Exception as e:
            print(f"Gagal membuat file dummy QRIS: {e}")

    # Dummy user object
    dummy_user = {"username": "kasir1"} 
    
    app = KasirWindow(root, dummy_user)
    root.mainloop()