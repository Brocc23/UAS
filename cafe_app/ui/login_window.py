import tkinter as tk
from tkinter import ttk, messagebox
from cafe_app.auth import login
from cafe_app.logika.user_model import UserModel

# Import window lain
from cafe_app.ui.admin_window import AdminWindow
from cafe_app.ui.kasir_window import KasirWindow
from cafe_app.ui.waiter_window import WaiterWindow
from cafe_app.ui.pembeli_window import PembeliWindow
from cafe_app.ui.owner_window import OwnerWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.mode = "login"

        # --- KONFIGURASI WARNA & FONT ---
        self.colors = {
            "bg": "#f0f2f5",          # Abu-abu sangat muda (seperti Facebook/Google)
            "card": "#ffffff",        # Putih bersih
            "primary": "#4a90e2",     # Biru modern
            "primary_hover": "#357abd",
            "text_dark": "#2d3436",   # Hitam lembut
            "text_grey": "#636e72",   # Abu-abu teks
            "danger": "#d63031"       # Merah soft
        }
        self.fonts = {
            "h1": ("Segoe UI", 24, "bold"),
            "h2": ("Segoe UI", 12),
            "body": ("Segoe UI", 10),
            "btn": ("Segoe UI", 10, "bold")
        }

        # Setup Window Utama
        self.root.title("Masuk Aplikasi")
        self.root.geometry("450x600")
        self.root.configure(bg=self.colors["bg"])
        
        # Center Window
        self.center_window(450, 600)

        # --- STYLE CONFIGURATION (Rahasia Tkinter Ganteng) ---
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam' adalah base tema yang paling mudah dikustomisasi
        
        # Style untuk Frame
        self.style.configure("Card.TFrame", background=self.colors["card"])
        
        # Style untuk Entry (Kotak Input)
        self.style.configure("Modern.TEntry", 
                             fieldbackground=self.colors["bg"], 
                             borderwidth=0, 
                             padding=10)
        
        # --- UI LAYOUT ---
        # Container Utama (Background)
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(fill="both", expand=True)

        # Kartu Login (Floating Card)
        # Menggunakan Frame biasa agar bisa set highlightthickness (border halus)
        self.card = tk.Frame(
            self.main_container, 
            bg=self.colors["card"], 
            padx=40, pady=40
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380)

        # 1. Judul
        self.lbl_title = tk.Label(
            self.card, 
            text="CAFE SOGOK", 
            font=self.fonts["h1"], 
            bg=self.colors["card"], 
            fg=self.colors["text_dark"]
        )
        self.lbl_title.pack(pady=(0, 5))

        # 2. Subjudul
        self.lbl_subtitle = tk.Label(
            self.card, 
            text="Silakan login untuk melanjutkan", 
            font=self.fonts["h2"], 
            bg=self.colors["card"], 
            fg=self.colors["text_grey"]
        )
        self.lbl_subtitle.pack(pady=(0, 30))

        # 3. Input Username
        self.create_label("USERNAME")
        self.username_entry = self.create_input(show_char="")
        
        # 4. Input Password
        self.create_label("PASSWORD")
        self.password_entry = self.create_input(show_char="•")

        # 5. Tombol Aksi (Custom Button murni Tkinter agar bisa warna custom)
        self.btn_action = tk.Button(
            self.card,
            text="LOGIN SEKARANG",
            font=self.fonts["btn"],
            bg=self.colors["primary"],
            fg="white",
            activebackground=self.colors["primary_hover"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.submit_action
        )
        self.btn_action.pack(fill="x", pady=(20, 10))

        # 6. Tombol Switch (Link Text)
        self.btn_switch = tk.Label(
            self.card,
            text="Belum punya akun? Daftar disini",
            font=self.fonts["body"],
            bg=self.colors["card"],
            fg=self.colors["primary"],
            cursor="hand2"
        )
        self.btn_switch.pack(pady=5)
        self.btn_switch.bind("<Button-1>", lambda e: self.switch_mode())
        
        # Efek Hover pada Link
        self.btn_switch.bind("<Enter>", lambda e: self.btn_switch.config(font=("Segoe UI", 10, "underline")))
        self.btn_switch.bind("<Leave>", lambda e: self.btn_switch.config(font=self.fonts["body"]))

    def create_label(self, text):
        lbl = tk.Label(
            self.card, 
            text=text, 
            font=("Segoe UI", 8, "bold"), 
            bg=self.colors["card"], 
            fg=self.colors["text_grey"],
            anchor="w"
        )
        lbl.pack(fill="x", pady=(10, 0))

    def create_input(self, show_char=""):
        # Trik membuat input terlihat modern: Bungkus Entry di dalam Frame dengan border bawah
        container = tk.Frame(self.card, bg=self.colors["card"], pady=5)
        container.pack(fill="x")
        
        entry = tk.Entry(
            container, 
            font=("Segoe UI", 11), 
            bg="#f7f9fc", # Warna input sedikit beda
            relief="flat",
            show=show_char
        )
        entry.pack(fill="x", ipady=8, padx=10) # ipady membuat input terlihat 'gemuk'/tinggi
        
        # Garis bawah berwarna (Underline effect)
        frame_line = tk.Frame(container, bg="#e1e4e8", height=2)
        frame_line.pack(fill="x", side="bottom")

        # Efek Focus (Garis berubah biru saat diklik)
        def on_focus_in(e): frame_line.config(bg=self.colors["primary"])
        def on_focus_out(e): frame_line.config(bg="#e1e4e8")
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def switch_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.lbl_title.config(text="Buat Akun")
            self.lbl_subtitle.config(text="Isi data untuk mendaftar")
            self.btn_action.config(text="DAFTAR", bg="#2ecc71", activebackground="#27ae60") # Hijau
            self.btn_switch.config(text="Sudah punya akun? Login")
        else:
            self.mode = "login"
            self.lbl_title.config(text="CAFE SOGOK")
            self.lbl_subtitle.config(text="Silakan login untuk melanjutkan pemesanan")
            self.btn_action.config(text="LOGIN SEKARANG", bg=self.colors["primary"], activebackground=self.colors["primary_hover"])
            self.btn_switch.config(text="Belum punya akun? Daftar disini")

    def submit_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username dan password wajib diisi")
            return

        if self.mode == "login":
            self.do_login(username, password)
        else:
            self.do_register(username, password)

    def do_login(self, username, password):
        user = login(username, password)
        if not user:
            messagebox.showerror("Gagal", "Username atau password salah")
            return

        user_data = {"id": user[0], "username": user[1], "role": user[2]}
        self.open_role_window(user_data)

    def do_register(self, username, password):
        success = UserModel().register(username, password, "pembeli")
        if not success:
            messagebox.showerror("Gagal", "Username sudah digunakan")
            return
        
        messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan login.")
        self.switch_mode()

    def open_role_window(self, user):
        role = user["role"]
        self.card.destroy() # Hapus UI Login
        self.main_container.destroy()
        
        # Restore default geometry or maximize for dashboard
        self.root.state("zoomed") 
        
        if role == "admin": AdminWindow(self.root, user)
        elif role == "kasir": KasirWindow(self.root, user)
        elif role == "waiter": WaiterWindow(self.root, user)
        elif role == "pembeli": PembeliWindow(self.root, user)
        elif role == "owner": OwnerWindow(self.root, user)
        else: messagebox.showerror("Error", "Role tidak dikenali!")