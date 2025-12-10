import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from cafe_app.utils import show_info, show_error
from cafe_app.logika import menu_model
from cafe_app.logika import user_model
from cafe_app.ui.report_window import ReportWindow

class AdminWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.window = tk.Toplevel(root)
        self.window.title("Admin Dashboard")
        self.window.geometry("900x600")

        title = tk.Label(self.window, text="Dashboard Admin", font=("Poppins", 18, "bold"))
        title.pack(pady=10)

        tab_control = ttk.Notebook(self.window)
        tab_control.pack(expand=True, fill="both")

        self.tab_menu = tk.Frame(tab_control)
        self.tab_user = tk.Frame(tab_control)
        self.tab_report = tk.Frame(tab_control)

        tab_control.add(self.tab_menu, text="Kelola Menu")
        tab_control.add(self.tab_user, text="Kelola Pengguna")
        tab_control.add(self.tab_report, text="Laporan Penjualan")

        self.build_menu_tab()
        self.build_user_tab()
        self.build_report_tab()

    def build_menu_tab(self):
        frame = tk.Frame(self.tab_menu)
        frame.pack(pady=10)

        tk.Label(frame, text="Nama").grid(row=0, column=0)
        tk.Label(frame, text="Kategori").grid(row=1, column=0)
        tk.Label(frame, text="Harga").grid(row=2, column=0)
        tk.Label(frame, text="Stok").grid(row=3, column=0)

        self.nama_menu = tk.Entry(frame, width=25)
        self.kategori_menu = tk.Entry(frame, width=25)
        self.harga_menu = tk.Entry(frame, width=25)
        self.stok_menu = tk.Entry(frame, width=25)

        self.nama_menu.grid(row=0, column=1)
        self.kategori_menu.grid(row=1, column=1)
        self.harga_menu.grid(row=2, column=1)
        self.stok_menu.grid(row=3, column=1)

        self.foto_menu_path = ""

        tk.Button(frame, text="Upload Foto", command=self.upload_foto).grid(row=4, column=1, pady=5)
        tk.Button(frame, text="Tambah Menu", command=self.add_menu).grid(row=5, column=1, pady=5)

        self.menu_table = ttk.Treeview(self.tab_menu, columns=("id", "nama", "kategori", "harga", "stok"), show="headings")
        self.menu_table.pack(expand=True, fill="both", pady=10)

        for col in ("id", "nama", "kategori", "harga", "stok"):
            self.menu_table.heading(col, text=col.title())

        self.menu_table.bind("<ButtonRelease-1>", self.select_menu)
        self.load_menu()

        btn_frame = tk.Frame(self.tab_menu)
        btn_frame.pack()

        tk.Button(btn_frame, text="Update Menu", command=self.update_menu).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Hapus Menu", command=self.delete_menu).grid(row=0, column=1, padx=5)

    def upload_foto(self):
        self.foto_menu_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png")])

    def add_menu(self):
        menu = MenuModel()
        menu.add_menu(
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
        menu = MenuModel().get_all_menu()
        for row in menu:
            self.menu_table.insert("", tk.END, values=row)

    def select_menu(self, event):
        selected = self.menu_table.focus()
        if not selected:
            return
        data = self.menu_table.item(selected)["values"]
        self.selected_menu_id = data[0]
        self.nama_menu.delete(0, tk.END)
        self.nama_menu.insert(0, data[1])
        self.kategori_menu.delete(0, tk.END)
        self.kategori_menu.insert(0, data[2])
        self.harga_menu.delete(0, tk.END)
        self.harga_menu.insert(0, data[3])
        self.stok_menu.delete(0, tk.END)
        self.stok_menu.insert(0, data[4])

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

    def build_user_tab(self):
        frame = tk.Frame(self.tab_user)
        frame.pack(pady=10)

        tk.Label(frame, text="Username").grid(row=0, column=0)
        tk.Label(frame, text="Password").grid(row=1, column=0)
        tk.Label(frame, text="Role").grid(row=2, column=0)

        self.user_username = tk.Entry(frame, width=25)
        self.user_password = tk.Entry(frame, width=25)
        self.user_role = ttk.Combobox(frame, values=["admin", "kasir", "waiter", "pembeli", "owner"], width=22)

        self.user_username.grid(row=0, column=1)
        self.user_password.grid(row=1, column=1)
        self.user_role.grid(row=2, column=1)

        tk.Button(frame, text="Tambah User", command=self.add_user).grid(row=3, column=1, pady=5)

        self.user_table = ttk.Treeview(self.tab_user, columns=("id", "username", "role"), show="headings")
        self.user_table.pack(expand=True, fill="both", pady=10)

        for col in ("id", "username", "role"):
            self.user_table.heading(col, text=col.title())

        self.user_table.bind("<ButtonRelease-1>", self.select_user)
        self.load_users()

        btn_frame = tk.Frame(self.tab_user)
        btn_frame.pack()

        tk.Button(btn_frame, text="Update User", command=self.update_user).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Hapus User", command=self.delete_user).grid(row=0, column=1, padx=5)

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
        users = UserModel().get_all_users()
        for row in users:
            self.user_table.insert("", tk.END, values=row)

    def select_user(self, event):
        selected = self.user_table.focus()
        if not selected:
            return
        data = self.user_table.item(selected)["values"]
        self.selected_user_id = data[0]
        self.user_username.delete(0, tk.END)
        self.user_username.insert(0, data[1])
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

    def build_report_tab(self):
        tk.Button(self.tab_report, text="Buka Laporan", command=lambda: ReportWindow(self.root)).pack(pady=20)
