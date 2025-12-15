import tkinter as tk
from tkinter import ttk, messagebox
from cafe_app.ui.style_utils import COLORS, FONTS, create_button, create_card
from cafe_app.logika.voucher_model import VoucherModel

class VoucherWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Kelola Voucher")
        self.window.geometry("800x600")
        self.window.configure(bg=COLORS["bg"])
        
        self.model = VoucherModel()
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.window, bg=COLORS["primary"], height=80)
        header.pack(fill="x")
        tk.Label(header, text="Manajemen Voucher", font=FONTS["h1"], bg=COLORS["primary"], fg="white").pack(pady=20)

        # Content Area
        content = tk.Frame(self.window, bg=COLORS["bg"], padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Left: Form
        form_frame = create_card(content)
        form_frame.pack(side="left", fill="y", padx=(0, 20))

        tk.Label(form_frame, text="Tambah Voucher Baru", font=FONTS["h2"], bg=COLORS["card"]).pack(pady=(0, 20))

        self.create_input(form_frame, "Kode Voucher", "kode_entry")
        
        tk.Label(form_frame, text="Tipe Diskon", bg=COLORS["card"], fg=COLORS["text_grey"]).pack(anchor="w", pady=(10, 0))
        self.tipe_var = tk.StringVar(value="persen")
        r_frame = tk.Frame(form_frame, bg=COLORS["card"])
        r_frame.pack(fill="x", pady=5)
        tk.Radiobutton(r_frame, text="Persen (%)", variable=self.tipe_var, value="persen", bg=COLORS["card"]).pack(side="left")
        tk.Radiobutton(r_frame, text="Nominal (Rn)", variable=self.tipe_var, value="nominal", bg=COLORS["card"]).pack(side="left", padx=10)

        self.create_input(form_frame, "Nilai Potongan", "nilai_entry")
        self.create_input(form_frame, "Kuota", "kuota_entry")

        create_button(form_frame, "SIMPAN VOUCHER", self.save_voucher, "primary").pack(fill="x", pady=20)

        # Right: Table
        table_frame = create_card(content)
        table_frame.pack(side="right", fill="both", expand=True)

        columns = ("ID", "Kode", "Tipe", "Nilai", "Kuota")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        
        self.tree.pack(fill="both", expand=True, pady=(0, 10))

        create_button(table_frame, "HAPUS TERPILIH", self.delete_voucher, "danger").pack(fill="x")

    def create_input(self, parent, label, attr_name):
        tk.Label(parent, text=label, bg=COLORS["card"], fg=COLORS["text_grey"]).pack(anchor="w", pady=(10, 0))
        entry = tk.Entry(parent, font=("Segoe UI", 10))
        entry.pack(fill="x", pady=5)
        setattr(self, attr_name, entry)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        vouchers = self.model.get_all_vouchers()
        for v in vouchers:
            self.tree.insert("", "end", values=v)

    def save_voucher(self):
        kode = self.kode_entry.get().strip()
        tipe = self.tipe_var.get()
        nilai = self.nilai_entry.get().strip()
        kuota = self.kuota_entry.get().strip()

        if not kode or not nilai or not kuota:
            messagebox.showwarning("Warning", "Semua field harus diisi")
            return

        try:
            nilai = int(nilai)
            kuota = int(kuota)
        except ValueError:
            messagebox.showerror("Error", "Nilai dan Kuota harus angka")
            return

        success, msg = self.model.add_voucher(kode, tipe, nilai, kuota)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.kode_entry.delete(0, "end")
            self.nilai_entry.delete(0, "end")
            self.kuota_entry.delete(0, "end")
            self.load_data()
        else:
            messagebox.showerror("Gagal", msg)

    def delete_voucher(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih voucher yang akan dihapus")
            return
            
        if messagebox.askyesno("Konfirmasi", "Yakin hapus voucher ini?"):
            item = self.tree.item(selected[0])
            v_id = item['values'][0]
            if self.model.delete_voucher(v_id):
                messagebox.showinfo("Sukses", "Voucher dihapus")
                self.load_data()
            else:
                messagebox.showerror("Error", "Gagal menghapus voucher")
