import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import datetime
from cafe_app.ui.style_utils import COLORS, FONTS, create_button, create_card
from cafe_app.logika.menu_model import MenuModel
from cafe_app.logika.voucher_model import VoucherModel
from cafe_app.database import get_connection

class PembeliWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.window = tk.Toplevel(root)
        self.window.title("Menu Pemesanan")
        self.window.state("zoomed")
        self.window.configure(bg=COLORS["bg"])

        self.menu_model = MenuModel()
        self.voucher_model = VoucherModel()
        self.cart = {} # {menu_id: {'data': item_tuple, 'qty': int}}
        self.voucher_applied = None

        self.setup_ui()
        self.load_menu_items()
        self.load_tables()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.window, bg="white", height=60, padx=20)
        header.pack(fill="x")
        
        tk.Label(header, text="CAFE SOGOK - PEMESANAN", font=FONTS["h2"], bg="white", fg=COLORS["primary"]).pack(side="left", pady=15)
        
        from cafe_app.ui.logout_utils import global_logout
        tk.Button(header, text="Log Out", command=lambda: global_logout(self.window, self.root), bg=COLORS["danger"], fg="white", relief="flat").pack(side="right", pady=15)

        # Main Layout
        content = tk.Frame(self.window, bg=COLORS["bg"], padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Left: Menu Grid (Scrollable)
        left_frame = tk.Frame(content, bg=COLORS["bg"])
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Search / Filter
        filter_frame = tk.Frame(left_frame, bg=COLORS["bg"])
        filter_frame.pack(fill="x", pady=(0, 10))
        
        self.search_var = tk.StringVar()
        entry_search = tk.Entry(filter_frame, textvariable=self.search_var, font=FONTS["body"], width=20)
        entry_search.pack(side="left", padx=(0, 10), ipady=5)
        
        # Category Filter
        self.cat_var = tk.StringVar(value="Semua")
        cat_combo = ttk.Combobox(filter_frame, textvariable=self.cat_var, state="readonly", width=15)
        cat_combo['values'] = ("Semua", "Makanan", "Minuman", "Snack") # Hardcoded or dynamic? Let's use standard + Semua
        cat_combo.pack(side="left", padx=(0, 10), ipady=5)
        
        tk.Button(filter_frame, text="Cari & Filter", command=self.load_menu_items, bg=COLORS["primary"], fg="white", relief="flat").pack(side="left")

        # Scrollable Canvas for Menu
        self.canvas = tk.Canvas(left_frame, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right: Order Summary
        # Right: Order Summary
        right_frame = create_card(content, padding=20)
        right_frame.pack(side="right", fill="y", ipadx=20)
        right_frame.config(width=400) # Min width hint
        # right_frame.pack_propagate(False) # Keep it flexible
        
        # --- Footer Section (Sticky Bottom) ---
        footer_frame = tk.Frame(right_frame, bg=COLORS["card"])
        footer_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        # Voucher
        v_frame = tk.Frame(footer_frame, bg=COLORS["card"])
        v_frame.pack(fill="x", pady=10)
        self.voucher_entry = tk.Entry(v_frame, font=FONTS["body"], bg=COLORS["input_bg"], relief="flat")
        self.voucher_entry.pack(side="left", fill="x", expand=True, ipady=5)
        tk.Button(v_frame, text="Pakai Kupon", command=self.apply_voucher, bg=COLORS["primary"], fg="white", relief="flat").pack(side="right", padx=(5, 0))

        self.lbl_discount = tk.Label(footer_frame, text="", bg=COLORS["card"], fg=COLORS["success"])
        self.lbl_discount.pack(anchor="e")

        # Total
        self.lbl_total = tk.Label(footer_frame, text="Total: Rp 0", font=FONTS["h1"], bg=COLORS["card"], fg=COLORS["primary"])
        self.lbl_total.pack(anchor="e", pady=(5, 20))

        # Checkout Button
        create_button(footer_frame, "BAYAR SEKARANG", self.checkout, "success").pack(fill="x")
        
        # --- Top Section (Expandable) ---
        top_frame = tk.Frame(right_frame, bg=COLORS["card"])
        top_frame.pack(side="top", fill="both", expand=True)

        # Header
        rx_header = tk.Frame(top_frame, bg=COLORS["card"])
        rx_header.pack(fill="x", pady=(0, 20))
        tk.Label(rx_header, text="Pesanan Anda", font=FONTS["h2"], bg=COLORS["card"]).pack(side="left")

        # Table Selection
        tk.Label(top_frame, text="Pilih Meja", font=("Segoe UI", 9, "bold"), bg=COLORS["card"], fg=COLORS["text_grey"]).pack(anchor="w")
        self.table_var = tk.StringVar()
        self.table_combo = ttk.Combobox(top_frame, textvariable=self.table_var, state="readonly")
        self.table_combo.pack(fill="x", pady=(5, 20))

        # Order List (Treeview)
        columns = ("Item", "Qty", "Harga", "Aksi")
        self.cart_tree = ttk.Treeview(top_frame, columns=columns, show="headings") # Removed fixed height
        self.cart_tree.heading("Item", text="Item")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Harga", text="Total")
        self.cart_tree.heading("Aksi", text="") 
        
        self.cart_tree.column("Item", width=120)
        self.cart_tree.column("Qty", width=40)
        self.cart_tree.column("Harga", width=80)
        self.cart_tree.column("Aksi", width=0, stretch=False) 
        
        self.cart_tree.pack(fill="both", expand=True)
        
        # Remove Button
        tk.Button(top_frame, text="Hapus Item Terpilih", command=self.remove_item, bg=COLORS["danger"], fg="white", relief="flat").pack(fill="x", pady=5)

    def load_menu_items(self):
        # Clear current grid
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        term = self.search_var.get()
        cat = self.cat_var.get()
        if cat == "Semua": cat = None
        
        items = self.menu_model.search_menu(term, kategori=cat)
        
        # Grid layout logic
        row = 0
        col = 0
        max_cols = 3

        for item in items:
            self.create_menu_card(item, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def create_menu_card(self, item, row, col):
        # item: (id, nama, kategori, harga, stok, foto)
        m_id, nama, kat, harga, stok, foto = item
        
        # Enforce fixed size for symmetry
        card_width = 220
        card_height = 320
        
        card = tk.Frame(self.scrollable_frame, bg="white", width=card_width, height=card_height, relief="raised", borderwidth=1)
        card.pack_propagate(False) # Prevent shrinking/expanding to fit content
        card.grid(row=row, column=col, padx=10, pady=10)
        
        # Inner content frame
        inner_content = tk.Frame(card, bg="white")
        inner_content.pack(fill="both", expand=True, padx=10, pady=10)

        # Image Handling
        if foto and os.path.exists(foto):
            try:
                img = Image.open(foto)
                img.thumbnail((150, 100)) # Resize for card
                photo = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(inner_content, image=photo, bg="white")
                lbl_img.image = photo # Keep reference
                lbl_img.pack(side="top", pady=(0, 10))
            except Exception:
                tk.Label(inner_content, text="[Gambar Rusak]", bg="#eee", width=20, height=5).pack(side="top", pady=(0, 10))
        else:
            tk.Label(inner_content, text="[No Image]", bg="#eee", width=20, height=5).pack(side="top", pady=(0, 10))
        
        # Product Info
        tk.Label(inner_content, text=nama, font=("Segoe UI", 11, "bold"), bg="white", wraplength=190, justify="left").pack(anchor="w", fill="x")
        tk.Label(inner_content, text=kat, font=("Segoe UI", 9), fg="grey", bg="white").pack(anchor="w")
        tk.Label(inner_content, text=f"Rp {harga:,}", font=("Segoe UI", 10, "bold"), fg=COLORS["primary"], bg="white").pack(anchor="w", pady=5)
        
        # Spacer to push button to bottom
        tk.Frame(inner_content, bg="white").pack(fill="both", expand=True) 
        
        state = "normal" if stok > 0 else "disabled"
        btn_text = "Tambah" if stok > 0 else "Habis"
        
        btn = tk.Button(
            inner_content, text=btn_text, 
            bg=COLORS["primary"] if stok > 0 else "grey", 
            fg="white", 
            state=state,
            relief="flat",
            command=lambda i=item: self.add_to_cart(i)
        )
        btn.pack(side="bottom", fill="x", pady=(5, 0))

    def load_tables(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nomor FROM tables WHERE status = 'kosong'")
        tables = cur.fetchall()
        conn.close()
        
        self.table_combo['values'] = [f"Meja {t[1]}" for t in tables]
        self.table_map = {f"Meja {t[1]}": t[0] for t in tables}

    def add_to_cart(self, item):
        m_id = item[0]
        if m_id in self.cart:
            if self.cart[m_id]['qty'] < item[4]: # Check stock
                self.cart[m_id]['qty'] += 1
            else:
                messagebox.showwarning("Stok Habis", "Stok tidak mencukupi")
                return
        else:
            self.cart[m_id] = {'data': item, 'qty': 1}
        
        self.update_cart_tree()

    def remove_item(self):
        selected = self.cart_tree.selection()
        if not selected: return
        
        item_id = self.cart_tree.item(selected[0])['tags'][0] # Check setup below
        # Wait, Treeview tags are tricky. Better to store ID in values or hidden col?
        # I didn't verify item_id mapping.
        
        # Let's use the 'Item' name to match? ID is safer.
        # Rework: I need to know which menu_id matches the selected row.
        # I'll store menu_id in the 'values' or use a map.
        # Simpler: Iterate cart, find matching row.
        
        # Better: use current selection index
        # But list order matches display? Not necessarily if sorted.
        
        # Let's map tree item iid to menu_id
        # I'll simply rebuild the tree with iid=menu_id string
        pass # Implemented in update_cart_tree

    def update_cart_tree(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        total_val = 0
        for m_id, content in self.cart.items():
            data = content['data']
            qty = content['qty']
            subtotal = data[3] * qty
            total_val += subtotal
            
            # Using m_id as iid for easy retrieval
            self.cart_tree.insert("", "end", iid=str(m_id), values=(data[1], qty, f"{subtotal:,}", "X"))

        self.calculate_total(total_val)

    def remove_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Pilih item yang mau dihapus")
            return
            
        m_id = int(selected[0]) # Since I used m_id as iid
        del self.cart[m_id]
        self.update_cart_tree()

    def apply_voucher(self):
        code = self.voucher_entry.get().strip()
        if not code: return
        
        valid, msg, val, tipe = self.voucher_model.validate_voucher(code)
        if valid:
            self.voucher_applied = {'code': code, 'val': val, 'tipe': tipe}
            messagebox.showinfo("Sukses", f"Voucher {code} dipasang!")
            self.update_cart_tree() # Recalc total
        else:
            messagebox.showerror("Gagal", msg)
            self.voucher_applied = None
            self.lbl_discount.config(text="")
            self.update_cart_tree()

    def calculate_total(self, subtotal):
        discount = 0
        if self.voucher_applied:
            if self.voucher_applied['tipe'] == 'persen':
                discount = subtotal * (self.voucher_applied['val'] / 100)
            else:
                discount = self.voucher_applied['val']
            
            # Cap discount at subtotal
            if discount > subtotal: discount = subtotal
            
            self.lbl_discount.config(text=f"Diskon: -Rp {int(discount):,}")
        else:
            self.lbl_discount.config(text="")

        final_total = subtotal - discount
        self.lbl_total.config(text=f"Total: Rp {int(final_total):,}")
        return int(final_total), int(discount)

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Kosong", "Keranjang belanja kosong")
            return
            
        table_name = self.table_var.get()
        if not table_name:
            messagebox.showwarning("Pilih Meja", "Silakan pilih meja dahulu")
            return
            
        table_id = self.table_map[table_name]
        
        # Calculate final
        subtotal = sum(i['data'][3] * i['qty'] for i in self.cart.values())
        total, discount = self.calculate_total(subtotal)
        
        # Save to DB
        conn = get_connection()
        cur = conn.cursor()
        
        try:
            # Transaksi
            cur.execute("""
                INSERT INTO transaksi (tanggal, total, metode_pembayaran, meja_id, status)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total, "Pending", table_id, "pending"))
            
            trans_id = cur.lastrowid
            
            # Use Voucher if any
            if self.voucher_applied:
                self.voucher_model.use_voucher(self.voucher_applied['code'])
                # Optionally store voucher_id in transaksi if column exists, 
                # but for now we haven't added it to schema strictly other than my thought.
                # Use total as net.
            
            # Detail Transaksi
            for m_id, content in self.cart.items():
                data = content['data']
                qty = content['qty']
                line_sub = data[3] * qty
                
                cur.execute("""
                    INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, subtotal, diskon)
                    VALUES (?, ?, ?, ?, 0)
                """, (trans_id, m_id, qty, line_sub))
                
                # Reduce stock
                cur.execute("UPDATE menu SET stok = stok - ? WHERE id = ?", (qty, m_id))

            # Update Table Status
            cur.execute("UPDATE tables SET status = 'terisi' WHERE id = ?", (table_id,))

            conn.commit()
            messagebox.showinfo("Sukses", "Pesanan berhasil dibuat! Mohon bayar di kasir.")
            
            # Close this window and open Kasir
            self.window.destroy()
            from cafe_app.ui.kasir_window import KasirWindow
            # We pass current user (Pembeli) to KasirWindow. 
            # In a real app this is weird, but per request "arahkan ke kasir window"
            KasirWindow(self.root, self.user) 
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Gagal membuat pesanan: {e}")
        finally:
            conn.close()