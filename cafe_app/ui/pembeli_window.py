import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from cafe_app.logika.menu_model import MenuModel
from cafe_app.ui.style_utils import COLORS, FONTS, setup_global_styles, create_card, create_button

class PembeliWindow:
    def __init__(self, root, user):
        self.window = tk.Toplevel(root)
        self.window.title("Cafe App - Pemesanan")
        self.window.state("zoomed")
        self.window.configure(bg=COLORS["bg"])

        setup_global_styles()

        self.menu_model = MenuModel()
        self.cart = []
        self.images = [] 
        
        # --- LAYOUT UTAMA: SIDEBAR (KIRI) & KONTEN (KANAN) ---
        main_container = tk.Frame(self.window, bg=COLORS["bg"], padx=0, pady=0)
        main_container.pack(fill="both", expand=True)

        # 1. Sidebar (Filter & Cart)
        self.sidebar = tk.Frame(main_container, bg="white", width=350, padx=20, pady=20)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Fixed width

        self.build_sidebar()

        # 2. Main Content (Menu Grid)
        content_area = tk.Frame(main_container, bg=COLORS["bg"], padx=20, pady=20)
        content_area.pack(side="left", fill="both", expand=True)

        # Header
        header = tk.Frame(content_area, bg=COLORS["bg"])
        header.pack(fill="x", pady=(0, 20))
        
        tk.Label(header, text="Menu Favorit", font=FONTS["h1"], bg=COLORS["bg"], fg=COLORS["text_dark"]).pack(side="left")
        
        # Search Box Floating
        search_frame = tk.Frame(header, bg="white", padx=10, pady=5)
        search_frame.pack(side="right")
        
        tk.Label(search_frame, text="🔍", bg="white").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=FONTS["body"], relief="flat", bg="white", width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_menu())

        # Scrollable Grid Area
        self.canvas = tk.Canvas(content_area, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_area, orient="vertical", command=self.canvas.yview)
        
        self.menu_grid = tk.Frame(self.canvas, bg=COLORS["bg"])
        self.menu_grid.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.menu_grid, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_menu()

    def build_sidebar(self):
        # -- Logo / Brand --
        tk.Label(self.sidebar, text="CAFE APP", font=("Segoe UI", 18, "bold"), bg="white", fg=COLORS["primary"]).pack(pady=(0, 30))

        # -- Filter Kategori --
        tk.Label(self.sidebar, text="Kategori", font=FONTS["h3"], bg="white", fg=COLORS["text_grey"]).pack(anchor="w", pady=(0, 10))
        
        self.kategori_var = tk.StringVar(value="Semua")
        filter_box = ttk.Combobox(self.sidebar, textvariable=self.kategori_var, values=["Semua", "Makanan", "Minuman"], state="readonly", font=FONTS["body"])
        filter_box.pack(fill="x", pady=(0, 30))
        filter_box.bind("<<ComboboxSelected>>", lambda e: self.load_menu())

        # -- Keranjang Belanja --
        tk.Label(self.sidebar, text="Keranjang Saya", font=FONTS["h3"], bg="white", fg=COLORS["text_grey"]).pack(anchor="w", pady=(0, 10))
        
        # Cart List (Custom styled simple list)
        self.cart_frame = tk.Frame(self.sidebar, bg="#f8f9fa")
        self.cart_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Total & Checkout (Stick to bottom)
        checkout_section = tk.Frame(self.sidebar, bg="white", pady=10)
        checkout_section.pack(side="bottom", fill="x")

        tk.Frame(checkout_section, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 10)) # Separator

        self.total_label = tk.Label(checkout_section, text="Total: Rp 0", font=FONTS["h2"], bg="white", fg=COLORS["text_dark"])
        self.total_label.pack(anchor="e", pady=(0, 10))

        create_button(checkout_section, "Bayar Sekarang", self.pilih_pembayaran, "primary").pack(fill="x")

        # Initial render cart placeholders
        self.refresh_cart_display()


    def load_menu(self):
        # Clear existing
        for w in self.menu_grid.winfo_children(): w.destroy()
        self.images.clear()

        # Get Data
        keyword = self.search_var.get()
        kategori = self.kategori_var.get()
        if kategori == "Semua": kategori = None
        menus = self.menu_model.search_menu(keyword, kategori)

        # Render Grid (3 columns)
        columns = 3
        for index, m in enumerate(menus):
            row = index // columns
            col = index % columns
            
            # Use create_card but with pack_propagate allowed for inner content
            card_frame = tk.Frame(self.menu_grid, bg="white", padx=0, pady=0) 
            # Drop shadow simulation (optional, skip for clean flat look)
            
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # --- Image Area ---
            img_height = 160
            img_container = tk.Frame(card_frame, bg="#ecf0f1", height=img_height, width=220)
            img_container.pack_propagate(False)
            img_container.pack(fill="x")
            
            lbl_img = tk.Label(img_container, bg="#ecf0f1")
            lbl_img.pack(expand=True)
            
            if m[5] and os.path.exists(m[5]):
                try:
                    img = Image.open(m[5])
                    # Crop/Resize logic could be better, but resize is fast
                    img = img.resize((220, img_height))
                    photo = ImageTk.PhotoImage(img)
                    lbl_img.config(image=photo)
                    self.images.append(photo)
                except:
                    lbl_img.config(text="Error", fg="red")
            else:
                lbl_img.config(text="No Photo", fg="#95a5a6")

            # --- Info Area ---
            info_box = tk.Frame(card_frame, bg="white", padx=15, pady=15)
            info_box.pack(fill="both", expand=True)

            tk.Label(info_box, text=m[1], font=("Segoe UI", 11, "bold"), bg="white", fg=COLORS["text_dark"], anchor="w").pack(fill="x")
            tk.Label(info_box, text=m[2], font=("Segoe UI", 9), bg="white", fg=COLORS["text_grey"], anchor="w").pack(fill="x", pady=(2, 5))
            
            # Price & Add Button Row
            action_row = tk.Frame(info_box, bg="white")
            action_row.pack(fill="x", pady=(10, 0))
            
            tk.Label(action_row, text=f"Rp {m[3]:,}", font=("Segoe UI", 11, "bold"), bg="white", fg=COLORS["primary"]).pack(side="left")
            
            btn_add = tk.Button(
                action_row, text="+", font=("Segoe UI", 12, "bold"), 
                bg=COLORS["bg"], fg=COLORS["primary"], relief="flat", cursor="hand2",
                command=lambda x=m: self.add_to_cart(x)
            )
            btn_add.pack(side="right") # Small round-ish button

    def add_to_cart(self, menu):
        # Logic: if exists, increment
        for item in self.cart:
            if item["id"] == menu[0]:
                item["jumlah"] += 1
                self.refresh_cart_display()
                return

        self.cart.append({"id": menu[0], "nama": menu[1], "harga": menu[3], "jumlah": 1})
        self.refresh_cart_display()

    def refresh_cart_display(self):
        # Clear sidebar list
        for w in self.cart_frame.winfo_children(): w.destroy()

        if not self.cart:
            tk.Label(self.cart_frame, text="Keranjang Kosong", font=FONTS["body"], bg="#f8f9fa", fg=COLORS["text_grey"]).pack(pady=20)
            self.total_label.config(text="Total: Rp 0")
            return

        total = 0
        for i, item in enumerate(self.cart):
            row = tk.Frame(self.cart_frame, bg="#f8f9fa", pady=5)
            row.pack(fill="x", padx=10)
            
            # Name & Price
            tk.Label(row, text=f"{item['jumlah']}x {item['nama']}", font=("Segoe UI", 10), bg="#f8f9fa", anchor="w").pack(side="left", fill="x", expand=True)
            
            subtotal = item['harga'] * item['jumlah']
            total += subtotal
            
            tk.Label(row, text=f"Rp{subtotal:,}", font=("Segoe UI", 10, "bold"), bg="#f8f9fa").pack(side="right")
            
            # Minus Button (Optional feature for later)
        
        self.total_label.config(text=f"Total: Rp {total:,}")

    def pilih_pembayaran(self):
        if not self.cart: return
        messagebox.showinfo("Checkout", "Fitur checkout akan membuka window pembayaran.")
        self.cart.clear()
        self.refresh_cart_display()