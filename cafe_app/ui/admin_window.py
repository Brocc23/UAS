import tkinter as tk
from tkinter import ttk, filedialog
from cafe_app.utils import show_info
from cafe_app.logika.menu_model import MenuModel
from cafe_app.logika.user_model import UserModel

import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class AdminWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.selected_menu_id = None
        self.selected_user_id = None
        self.foto_menu_path = ""

        self.window = tk.Toplevel(root)
        self.window.title("Admin Dashboard")
        self.window.state("zoomed")
        self.window.configure(bg="#f5f6fa")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook.Tab", padding=(14, 8))
        style.configure("Treeview", rowheight=30)
        style.configure("Header.TLabel", font=("Poppins", 18, "bold"))
        style.configure("Section.TLabelframe", padding=10)

        header = ttk.Label(self.window, text="Dashboard Admin", style="Header.TLabel")
        header.pack(pady=12)

        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True, fill="both", padx=15, pady=10)

        self.tab_menu = ttk.Frame(notebook)
        self.tab_user = ttk.Frame(notebook)
        self.tab_laporan = ttk.Frame(notebook)

        notebook.add(self.tab_menu, text="Kelola Menu")
        notebook.add(self.tab_user, text="Kelola User")
        notebook.add(self.tab_laporan, text="Laporan")

        self.build_menu_tab()
        self.build_user_tab()
        self.build_laporan_tab()

    # ======================================================
    # ==================== MENU TAB ========================
    # ======================================================
    def build_menu_tab(self):
        form = ttk.LabelFrame(self.tab_menu, text="Menu", style="Section.TLabelframe")
        form.pack(fill="x", padx=10, pady=10)

        labels = ["Nama Menu", "Kategori", "Harga", "Stok"]
        for i, text in enumerate(labels):
            ttk.Label(form, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=6)

        self.nama_menu = ttk.Entry(form, width=32)
        self.kategori_menu = ttk.Entry(form, width=32)
        self.harga_menu = ttk.Entry(form, width=32)
        self.stok_menu = ttk.Entry(form, width=32)

        entries = [self.nama_menu, self.kategori_menu, self.harga_menu, self.stok_menu]
        for i, ent in enumerate(entries):
            ent.grid(row=i, column=1, padx=5, pady=6)

        btn_row = ttk.Frame(form)
        btn_row.grid(row=0, column=2, rowspan=4, padx=15)

        ttk.Button(btn_row, text="Upload Foto", command=self.upload_foto).pack(fill="x", pady=5)
        ttk.Button(btn_row, text="Tambah Menu", command=self.add_menu).pack(fill="x", pady=5)

        table_box = ttk.LabelFrame(self.tab_menu, text="Daftar Menu", style="Section.TLabelframe")
        table_box.pack(expand=True, fill="both", padx=10, pady=10)

        cols = ("id", "nama", "kategori", "harga", "stok")
        self.menu_table = ttk.Treeview(table_box, columns=cols, show="headings")
        self.menu_table.pack(expand=True, fill="both")

        for col in cols:
            self.menu_table.heading(col, text=col.upper())
            self.menu_table.column(col, anchor="center")

        self.menu_table.bind("<ButtonRelease-1>", self.select_menu)
        self.load_menu()

        action = ttk.Frame(self.tab_menu)
        action.pack(pady=8)
        ttk.Button(action, text="Update Menu", command=self.update_menu).grid(row=0, column=0, padx=6)
        ttk.Button(action, text="Hapus Menu", command=self.delete_menu).grid(row=0, column=1, padx=6)

    def upload_foto(self):
        self.foto_menu_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg;*.png")]
        )

    def add_menu(self):
        MenuModel().add_menu(
            self.nama_menu.get(),
            self.kategori_menu.get(),
            self.harga_menu.get(),
            self.stok_menu.get(),
            self.foto_menu_path
        )
        show_info("Menu berhasil ditambahkan.")
        self.load_menu()

    def load_menu(self):
        self.menu_table.delete(*self.menu_table.get_children())
        for row in MenuModel().get_all_menu():
            self.menu_table.insert("", tk.END, values=row)

    def select_menu(self, event):
        selected = self.menu_table.focus()
        if not selected:
            return
        data = self.menu_table.item(selected)["values"]
        self.selected_menu_id = data[0]
        self.nama_menu.delete(0, tk.END); self.nama_menu.insert(0, data[1])
        self.kategori_menu.delete(0, tk.END); self.kategori_menu.insert(0, data[2])
        self.harga_menu.delete(0, tk.END); self.harga_menu.insert(0, data[3])
        self.stok_menu.delete(0, tk.END); self.stok_menu.insert(0, data[4])

    def update_menu(self):
        MenuModel().update_menu(
            self.selected_menu_id,
            self.nama_menu.get(),
            self.kategori_menu.get(),
            self.harga_menu.get(),
            self.stok_menu.get(),
            self.foto_menu_path
        )
        show_info("Menu berhasil diupdate.")
        self.load_menu()

    def delete_menu(self):
        MenuModel().delete_menu(self.selected_menu_id)
        show_info("Menu berhasil dihapus.")
        self.load_menu()

    # ======================================================
    # ==================== USER TAB ========================
    # ======================================================
    def build_user_tab(self):
        form = ttk.LabelFrame(self.tab_user, text="User", style="Section.TLabelframe")
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", padx=5, pady=6)
        ttk.Label(form, text="Role").grid(row=2, column=0, sticky="w", padx=5, pady=6)

        self.user_username = ttk.Entry(form, width=32)
        self.user_password = ttk.Entry(form, width=32)
        self.user_role = ttk.Combobox(
            form,
            values=["admin", "kasir", "waiter", "pembeli", "owner"],
            width=29
        )

        self.user_username.grid(row=0, column=1, pady=6)
        self.user_password.grid(row=1, column=1, pady=6)
        self.user_role.grid(row=2, column=1, pady=6)

        ttk.Button(form, text="Tambah User", command=self.add_user).grid(
            row=3, column=1, sticky="w", pady=8
        )

        table_box = ttk.LabelFrame(self.tab_user, text="Daftar User", style="Section.TLabelframe")
        table_box.pack(expand=True, fill="both", padx=10, pady=10)

        cols = ("id", "username", "role")
        self.user_table = ttk.Treeview(table_box, columns=cols, show="headings")
        self.user_table.pack(expand=True, fill="both")

        for col in cols:
            self.user_table.heading(col, text=col.upper())
            self.user_table.column(col, anchor="center")

        self.user_table.bind("<ButtonRelease-1>", self.select_user)
        self.load_users()

        action = ttk.Frame(self.tab_user)
        action.pack(pady=8)
        ttk.Button(action, text="Update User", command=self.update_user).grid(row=0, column=0, padx=6)
        ttk.Button(action, text="Hapus User", command=self.delete_user).grid(row=0, column=1, padx=6)

    def add_user(self):
        UserModel().register(
            self.user_username.get(),
            self.user_password.get(),
            self.user_role.get()
        )
        show_info("User berhasil ditambahkan.")
        self.load_users()

    def load_users(self):
        self.user_table.delete(*self.user_table.get_children())
        for row in UserModel().get_all_users():
            self.user_table.insert("", tk.END, values=row)

    def select_user(self, event):
        selected = self.user_table.focus()
        if not selected:
            return
        data = self.user_table.item(selected)["values"]
        self.selected_user_id = data[0]
        self.user_username.delete(0, tk.END); self.user_username.insert(0, data[1])
        self.user_role.set(data[2])

    def update_user(self):
        UserModel().update_user(
            self.selected_user_id,
            self.user_username.get(),
            self.user_role.get()
        )
        show_info("User berhasil diupdate.")
        self.load_users()

    def delete_user(self):
        UserModel().delete_user(self.selected_user_id)
        show_info("User berhasil dihapus.")
        self.load_users()

    # ======================================================
    # ================== LAPORAN TAB =======================
    # ======================================================
    def build_laporan_tab(self):
        container = ttk.Frame(self.tab_laporan, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Laporan Penjualan (Dummy)",
            font=("Poppins", 16, "bold")
        ).pack(pady=10)

        bulan = ["Januari", "Februari", "Maret"]
        penjualan = [random.randint(5_000_000, 15_000_000) for _ in bulan]

        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(bulan, penjualan, marker="o")
        ax.set_title("Penjualan 3 Bulan Terakhir")
        ax.set_ylabel("Total Penjualan (Rp)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
