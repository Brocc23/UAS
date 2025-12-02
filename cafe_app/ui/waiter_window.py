import tkinter as tk
from tkinter import ttk
from cafe_app.utils import show_info, show_error

class WaiterWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        self.window = tk.Toplevel(root)
        self.window.title("Waiter Panel")
        self.window.geometry("600x450")

        tk.Label(self.window, text=f"Waiter: {user['username']}", font=("Arial", 12, "bold")).pack(pady=10)

        frame = tk.Frame(self.window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame, text="Daftar Pesanan Menunggu").grid(row=0, column=0, padx=5, pady=5)
        self.tree = ttk.Treeview(frame, columns=("id", "meja", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("meja", text="Meja")
        self.tree.heading("status", text="Status")
        self.tree.grid(row=1, column=0, padx=5, pady=5)

        tk.Button(frame, text="Tandai Diantar", command=self.set_delivered).grid(row=2, column=0, pady=10)

        self.load_pending_orders()

    def load_pending_orders(self):
        orders = [
            {"id": 101, "meja": 3, "status": "Menunggu Diantar"},
            {"id": 102, "meja": 5, "status": "Menunggu Diantar"},
        ]

        for order in orders:
            self.tree.insert("", "end", values=(order["id"], order["meja"], order["status"]))

    def set_delivered(self):
        selected = self.tree.focus()
        if not selected:
            show_error("Pilih pesanan terlebih dahulu!")
            return

        values = self.tree.item(selected, "values")
        order_id = values[0]

        show_info(f"Pesanan {order_id} sudah diantar!")
        self.tree.delete(selected)