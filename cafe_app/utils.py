import tkinter as tk
from tkinter import messagebox, filedialog

def show_info(msg):
    messagebox.showinfo("Info", msg)

def show_error(msg):
    messagebox.showerror("Error", msg)

def ask_yes_no(msg):
    return messagebox.askyesno("Konfirmasi", msg)

def open_image_file():
    path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    return path
