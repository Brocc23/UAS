import tkinter as tk
from tkinter import ttk
from cafe_app.ui.admin_window import AdminWindow
from cafe_app.ui.report_window import ReportWindow
from cafe_app.ui.style_utils import COLORS, FONTS, setup_global_styles, create_card, create_button

class OwnerWindow:
    def __init__(self, master, user):
        self.master = master
        self.user = user

        self.window = tk.Toplevel(master)
        self.window.title("Owner Panel")
        self.window.state("zoomed")
        self.window.configure(bg=COLORS["bg"])
        
        setup_global_styles()

        center_frame = tk.Frame(self.window, bg=COLORS["bg"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        card = create_card(center_frame, padding=40)
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="OWNER",
            font=FONTS["h1"],
            bg=COLORS["card"],
            fg=COLORS["primary"]
        ).pack(pady=(0, 10))

        tk.Label(
            card,
            text=f"Selamat Datang, {self.user['username']}",
            font=FONTS["h3"],
            bg=COLORS["card"],
            fg=COLORS["text_grey"]
        ).pack(pady=(0, 30))

        btn_frame = tk.Frame(card, bg=COLORS["card"])
        btn_frame.pack(fill="x")

        create_button(
            btn_frame,
            "KELOLA DATA (ADMIN PANEL)",
            self.open_admin,
            "primary",
            width=30
        ).pack(pady=10)

        create_button(
            btn_frame,
            "LIHAT LAPORAN KEUANGAN",
            self.open_report,
            "success",
            width=30
        ).pack(pady=10)

        create_button(
            btn_frame,
            "KELOLA KUPON DISKON",
            self.open_voucher,
            "warning",
            width=30
        ).pack(pady=10)

        tk.Label(card, text="", bg=COLORS["card"]).pack(pady=10)
        
        create_button(
            btn_frame,
            "LOGOUT",
            self.logout_to_login,
            "danger",
            width=30
        ).pack(pady=10)
        
    def open_voucher(self):
        from cafe_app.ui.voucher_window import VoucherWindow
        VoucherWindow(self.master)
    
    def open_admin(self):
        AdminWindow(self.master, self.user)

    def open_report(self):
        ReportWindow(self.master)

    def logout_to_login(self):
        self.window.destroy()
        from cafe_app.ui.login_window import LoginWindow
        # Re-initialize LoginWindow with the master (root)
        # Note: self.master is root
        for widget in self.master.winfo_children():
            # Safety cleanup if any
            if isinstance(widget, tk.Toplevel): widget.destroy()
            
        LoginWindow(self.master)

    def open_admin(self):
        AdminWindow(self.master, self.user)

    def open_report(self):
        ReportWindow(self.master)
