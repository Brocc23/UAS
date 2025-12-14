# CATATAN PENTING
# File ini HANYA memperbagus tampilan UI
# TIDAK mengubah fungsi, alur, maupun pemanggilan window lain

import tkinter as tk
from tkinter import ttk
from cafe_app.ui.admin_window import AdminWindow
from cafe_app.ui.report_window import ReportWindow

class OwnerWindow:
    def __init__(self, master, user):
        self.master = master
        self.user = user

        self.window = tk.Toplevel(master)
        self.window.title("Owner Panel")
        self.window.geometry("420x320")
        self.window.resizable(False, False)
        self.window.configure(bg="#f5f6fa")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Title.TLabel", font=("Poppins", 16, "bold"))
        style.configure("Sub.TLabel", font=("Poppins", 11))
        style.configure("Action.TButton", padding=8)

        container = ttk.Frame(self.window, padding=20)
        container.pack(expand=True, fill="both")

        ttk.Label(container, text="Owner Panel", style="Title.TLabel").pack(pady=(0, 5))
        ttk.Label(
            container,
            text=f"Login sebagai: {self.user['username']}",
            style="Sub.TLabel"
        ).pack(pady=(0, 20))

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x")

        ttk.Button(
            btn_frame,
            text="Buka Admin Panel",
            style="Action.TButton",
            command=self.open_admin
        ).pack(fill="x", pady=6)

        ttk.Button(
            btn_frame,
            text="Lihat Laporan",
            style="Action.TButton",
            command=self.open_report
        ).pack(fill="x", pady=6)

        ttk.Separator(container).pack(fill="x", pady=15)

        ttk.Button(container, text="Logout", command=self.window.destroy).pack(fill="x")

    def open_admin(self):
        AdminWindow(self.master, self.user)

    def open_report(self):
        ReportWindow(self.master)
