import tkinter as tk
from cafe_app.ui.admin_window import AdminWindow
from cafe_app.ui.report_window import ReportWindow

class OwnerWindow:
    def __init__(self, master, user):
        self.master = master
        self.user = user

        self.window = tk.Toplevel(master)
        self.window.title("Owner Panel")
        self.window.geometry("400x300")

        tk.Label(
            self.window,
            text=f"Owner: {self.user['username']}",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        tk.Button(
            self.window,
            text="Buka Admin Panel",
            width=25,
            command=self.open_admin
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Lihat Laporan",
            width=25,
            command=self.open_report
        ).pack(pady=10)

        tk.Button(
            self.window,
            text="Logout",
            width=25,
            command=self.window.destroy
        ).pack(pady=20)

    def open_admin(self):
        AdminWindow(self.master, self.user)

    def open_report(self):

        ReportWindow(self.master)
