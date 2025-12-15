import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from cafe_app.utils import show_info
from cafe_app.logika.menu_model import MenuModel
from cafe_app.logika.user_model import UserModel

class AdminWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.selected_menu_id = None
        self.selected_user_id = None
        self.foto_menu_path = ""
        self.menu_image = None

        # --- Warna & Font ---
        self.colors = {
            "bg": "#f0f2f5",          
            "card": "#ffffff",        
            "primary": "#4a90e2",     
            "text_dark": "#2d3436",   
            "text_grey": "#636e72",
            "danger": "#d63031",
        }
        self.fonts = {
            "h1": ("Segoe UI", 24, "bold"),
            "h2": ("Segoe UI", 12),
            "body": ("Segoe UI", 10),
            "btn": ("Segoe UI", 10, "bold"),
            "table_head": ("Segoe UI", 10, "bold"),
            "table_body": ("Segoe UI", 9)
        }

        self.window = tk.Toplevel(root)
        self.window.title(f"Admin Dashboard - {user['username']}")
        self.window.state("zoomed")
        self.window.configure(bg=self.colors["bg"])

        self.setup_styles()
        self.build_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=self.colors["bg"], 
                        foreground=self.colors["text_grey"],
                        padding=(20, 10),
                        font=self.fonts["btn"])
        style.map("TNotebook.Tab", 
                  background=[("selected", self.colors["primary"])], 
                  foreground=[("selected", "white")])
        style.configure("Treeview", 
                        background="white",
                        fieldbackground="white",
                        foreground=self.colors["text_dark"],
                        rowheight=35,
                        font=self.fonts["table_body"],
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background=self.colors["bg"],
                        foreground=self.colors["text_dark"],
                        font=self.fonts["table_head"],
                        relief="flat")
        style.map("Treeview", background=[("selected", self.colors["primary"])])

    def build_layout(self):
        # Header
        header = tk.Frame(self.window, bg=self.colors["card"], height=60, padx=20)
        header.pack(fill="x")
        tk.Label(header, text="CAFE APP ADMIN", font=("Segoe UI",16,"bold"),
                 bg=self.colors["card"], fg=self.colors["primary"]).pack(side="left", pady=15)
        tk.Label(header, text=f"Halo, {self.user['username']} ({self.user['role']})",
                 font=self.fonts["body"], bg=self.colors["card"], fg=self.colors["text_grey"]).pack(side="right", pady=15)

        # Container
        container = tk.Frame(self.window, bg=self.colors["bg"], padx=20, pady=20)
        container.pack(fill="both", expand=True)
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(expand=True, fill="both")

        self.tab_menu = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.tab_user = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_menu, text="  KELOLA MENU  ")
        self.notebook.add(self.tab_user, text="  KELOLA USER  ")

        self.build_menu_tab()
        self.build_user_tab()

    # --- Utilities ---
    def create_card(self, parent):
        return tk.Frame(parent, bg=self.colors["card"], padx=20, pady=20)

    def create_custom_button(self, parent, text, command, bg_color, width=None):
        btn = tk.Button(parent, text=text, font=self.fonts["btn"], bg=bg_color,
                        fg="white", activebackground=bg_color, activeforeground="white",
                        relief="flat", cursor="hand2", pady=8, command=command)
        if width: btn.config(width=width)
        def on_enter(e): btn.config(bg="#357abd" if bg_color == self.colors["primary"] else "#c0392b")
        def on_leave(e): btn.config(bg=bg_color)
        if bg_color in [self.colors["primary"], self.colors["danger"]]:
            btn.bind("<Enter>", on_enter); btn.bind("<Leave>", on_leave)
        return btn

    def create_custom_entry(self, parent, variable=None):
        container = tk.Frame(parent, bg=self.colors["card"], pady=2)
        entry = tk.Entry(container, font=("Segoe UI", 11), bg="#f7f9fc", relief="flat", textvariable=variable)
        entry.pack(fill="x", ipady=6, padx=10)
        line = tk.Frame(container, bg="#e1e4e8", height=2)
        line.pack(fill="x", side="bottom")
        entry.bind("<FocusIn>", lambda e: line.config(bg=self.colors["primary"]))
        entry.bind("<FocusOut>", lambda e: line.config(bg="#e1e4e8"))
        return container, entry

    # --- MENU TAB ---
    def build_menu_tab(self):
        layout = tk.Frame(self.tab_menu, bg=self.colors["bg"])
        layout.pack(fill="both", expand=True, padx=10, pady=10)

        left = tk.Frame(layout, bg=self.colors["bg"], width=350)
        left.pack(side="left", fill="y", padx=(0,20))
        left.pack_propagate(False)
        form_card = self.create_card(left); form_card.pack(fill="x", pady=(0,20))
        tk.Label(form_card, text="Input Menu", font=self.fonts["h2"], bg=self.colors["card"], fg=self.colors["primary"]).pack(anchor="w", pady=(0,15))

        # Form fields
        self.nama_menu = self._add_form_field(form_card,"Nama Menu")
        self.kategori_menu = self._add_form_field(form_card,"Kategori")
        self.harga_menu = self._add_form_field(form_card,"Harga (Rp)")
        self.stok_menu = self._add_form_field(form_card,"Stok Awal")

        tk.Label(form_card, text="Foto Menu", font=("Segoe UI",9,"bold"),
                 bg=self.colors["card"], fg=self.colors["text_grey"]).pack(anchor="w", pady=(10,5))
        self.btn_upload = self.create_custom_button(form_card,"Pilih Foto...",self.upload_foto,"#636e72")
        self.btn_upload.pack(fill="x")

        btn_box = tk.Frame(form_card, bg=self.colors["card"]); btn_box.pack(fill="x", pady=20)
        self.create_custom_button(btn_box,"Simpan Menu",self.add_menu,self.colors["primary"]).pack(fill="x", pady=5)
        self.create_custom_button(btn_box,"Update Selected",self.update_menu,self.colors["text_grey"]).pack(fill="x", pady=5)
        self.create_custom_button(btn_box,"Hapus Selected",self.delete_menu,self.colors["danger"]).pack(fill="x", pady=5)

        preview_card = self.create_card(left); preview_card.pack(fill="x", expand=True)
        tk.Label(preview_card, text="Preview Foto", font=self.fonts["h2"], bg=self.colors["card"], fg=self.colors["primary"]).pack(anchor="w", pady=(0,10))
        self.preview_label = tk.Label(preview_card, text="No Image", bg="#f0f2f5", height=10)
        self.preview_label.pack(fill="both", expand=True)

        # Right table
        right = tk.Frame(layout, bg=self.colors["bg"]); right.pack(side="left", fill="both", expand=True)
        table_card = self.create_card(right); table_card.pack(fill="both", expand=True)
        tk.Label(table_card, text="Daftar Menu Tersedia", font=self.fonts["h2"], bg=self.colors["card"], fg=self.colors["primary"]).pack(anchor="w", pady=(0,15))

        table_frame = tk.Frame(table_card, bg="white"); table_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical"); scrollbar.pack(side="right", fill="y")
        cols = ("id","nama","kategori","harga","stok","foto")
        self.menu_table = ttk.Treeview(table_frame, columns=cols, show="headings", yscrollcommand=scrollbar.set, style="Treeview")
        self.menu_table.pack(side="left", fill="both", expand=True); scrollbar.config(command=self.menu_table.yview)
        for c in cols: self.menu_table.heading(c,text=c.upper()); self.menu_table.column(c, anchor="center")
        self.menu_table.bind("<ButtonRelease-1>", self.select_menu)
        self.load_menu()

    def _add_form_field(self,parent,label):
        tk.Label(parent, text=label, font=("Segoe UI",9,"bold"), bg=self.colors["card"], fg=self.colors["text_grey"]).pack(anchor="w", pady=(5,0))
        container, entry = self.create_custom_entry(parent); container.pack(fill="x", pady=(0,10))
        return entry

    def upload_foto(self):
        path = filedialog.askopenfilename(filetypes=[("Images","*.jpg;*.png")])
        if not path: return
        self.foto_menu_path = path
        self.show_preview_foto(path)

    def show_preview_foto(self,path):
        self.preview_label.config(image="", text=""); self.menu_image=None
        if not path or path=="None":
            self.preview_label.config(text="No Image Selected", fg=self.colors["text_grey"]); return
        if not os.path.exists(path):
            self.preview_label.config(text=f"File tidak ditemukan:\n{path}", fg=self.colors["danger"]); return
        try:
            img = Image.open(path); img.thumbnail((200,200))
            self.menu_image = ImageTk.PhotoImage(img, master=self.window)
            self.preview_label.config(image=self.menu_image)
        except Exception as e:
            self.preview_label.config(text=f"Gagal memuat gambar:\n{str(e)}", fg=self.colors["danger"])

    def add_menu(self):
        try:
            MenuModel().add_menu(self.nama_menu.get(), self.kategori_menu.get(),
                                 self.harga_menu.get(), self.stok_menu.get(), self.foto_menu_path)
            show_info("Menu berhasil ditambahkan.")
            self.load_menu(); self._clear_menu_form()
        except Exception as e: messagebox.showerror("Error", str(e))

    def load_menu(self):
        self.menu_table.delete(*self.menu_table.get_children())
        for r in MenuModel().get_all_menu(): self.menu_table.insert("",tk.END,values=r)

    def select_menu(self,event):
        s = self.menu_table.focus()
        if not s: return
        d = self.menu_table.item(s)["values"]
        self.selected_menu_id = d[0]
        self.nama_menu.delete(0,tk.END); self.nama_menu.insert(0,d[1])
        self.kategori_menu.delete(0,tk.END); self.kategori_menu.insert(0,d[2])
        self.harga_menu.delete(0,tk.END); self.harga_menu.insert(0,d[3])
        self.stok_menu.delete(0,tk.END); self.stok_menu.insert(0,d[4])
        self.foto_menu_path = d[5]; self.show_preview_foto(self.foto_menu_path)

    def update_menu(self):
        if not self.selected_menu_id: 
            messagebox.showwarning("Peringatan","Pilih menu terlebih dahulu!"); return
        try:
            MenuModel().update_menu(self.selected_menu_id,self.nama_menu.get(),
                                    self.kategori_menu.get(),self.harga_menu.get(),
                                    self.stok_menu.get(),self.foto_menu_path)
            show_info("Menu berhasil diupdate.")
            self.load_menu()
            # fokus ke item yang baru diupdate
            for item in self.menu_table.get_children():
                if self.menu_table.item(item)["values"][0]==self.selected_menu_id:
                    self.menu_table.selection_set(item); self.menu_table.focus(item); self.menu_table.see(item); break
            self.select_menu(None)  # reload form
        except Exception as e: messagebox.showerror("Error",str(e))

    def delete_menu(self):
        if not self.selected_menu_id: return
        if messagebox.askyesno("Konfirmasi","Yakin hapus menu ini?"):
            MenuModel().delete_menu(self.selected_menu_id)
            show_info("Menu berhasil dihapus.")
            self.load_menu(); self._clear_menu_form()
            self.selected_menu_id = None

    def _clear_menu_form(self):
        self.nama_menu.delete(0,tk.END); self.kategori_menu.delete(0,tk.END)
        self.harga_menu.delete(0,tk.END); self.stok_menu.delete(0,tk.END)
        self.foto_menu_path=""; self.show_preview_foto("")

    # --- USER TAB ---
    def build_user_tab(self):
        layout = tk.Frame(self.tab_user,bg=self.colors["bg"]); layout.pack(fill="both",expand=True,padx=20,pady=20)
        form_card = self.create_card(layout); form_card.pack(fill="x", pady=(0,20))
        tk.Label(form_card,text="Kelola User",font=self.fonts["h2"],bg=self.colors["card"],fg=self.colors["primary"]).pack(anchor="w", pady=(0,15))

        form_grid = tk.Frame(form_card,bg=self.colors["card"]); form_grid.pack(fill="x")
        # Row1
        self._add_grid_field(form_grid,"Username",0,0)
        self.user_username = self.create_custom_entry(form_grid)[1]; self.user_username.master.grid(row=0,column=1,sticky="ew",padx=10)
        self._add_grid_field(form_grid,"Password",0,2)
        self.user_password = self.create_custom_entry(form_grid)[1]; self.user_password.master.grid(row=0,column=3,sticky="ew",padx=10)
        # Row2
        self._add_grid_field(form_grid,"Role",1,0)
        self.user_role = ttk.Combobox(form_grid, values=["admin","kasir","waiter","pembeli","owner"], font=("Segoe UI",11), state="readonly")
        self.user_role.grid(row=1,column=1,sticky="ew",padx=10,ipady=5,pady=10)
        action_box = tk.Frame(form_card,bg=self.colors["card"]); action_box.pack(fill="x", pady=10)
        self.create_custom_button(action_box,"Tambah User",self.add_user,self.colors["primary"],width=15).pack(side="left",padx=5)
        self.create_custom_button(action_box,"Update User",self.update_user,self.colors["text_grey"],width=15).pack(side="left",padx=5)
        self.create_custom_button(action_box,"Hapus User",self.delete_user,self.colors["danger"],width=15).pack(side="left",padx=5)
        form_grid.columnconfigure(1,weight=1); form_grid.columnconfigure(3,weight=1)

        # Table
        table_card = self.create_card(layout); table_card.pack(fill="both",expand=True)
        cols=("id","username","role")
        self.user_table = ttk.Treeview(table_card,columns=cols,show="headings",style="Treeview"); self.user_table.pack(expand=True,fill="both")
        for c in cols: self.user_table.heading(c,text=c.upper()); self.user_table.column(c,anchor="center")
        self.user_table.bind("<ButtonRelease-1>",self.select_user)
        self.load_users()

    def _add_grid_field(self,parent,text,r,c):
        tk.Label(parent,text=text,font=("Segoe UI",9,"bold"),bg=self.colors["card"],fg=self.colors["text_grey"]).grid(row=r,column=c,sticky="w")

    def add_user(self):
        try:
            UserModel().register(self.user_username.get(),self.user_password.get(),self.user_role.get())
            show_info("User berhasil ditambahkan."); self.load_users()
        except Exception as e: messagebox.showerror("Error",str(e))

    def load_users(self):
        self.user_table.delete(*self.user_table.get_children())
        for r in UserModel().get_all_users(): self.user_table.insert("",tk.END,values=r)

    def select_user(self,event):
        s=self.user_table.focus()
        if not s: return
        d=self.user_table.item(s)["values"]
        self.selected_user_id=d[0]; self.user_username.delete(0,tk.END); self.user_username.insert(0,d[1])
        self.user_role.set(d[2])

    def update_user(self):
        if not self.selected_user_id: return
        UserModel().update_user(self.selected_user_id,self.user_username.get(),self.user_role.get())
        show_info("User berhasil diupdate."); self.load_users()

    def delete_user(self):
        if not self.selected_user_id: return
        if messagebox.askyesno("Konfirmasi","Yakin hapus user ini?"):
            UserModel().delete_user(self.selected_user_id)
            show_info("User berhasil dihapus."); self.load_users()
