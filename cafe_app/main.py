import tkinter as tk
from cafe_app.database import init_db
from cafe_app.ui.login_window import LoginWindow

def main():
    print("test")
    init_db()
    root = tk.Tk()
    root.title("Aplikasi Café")
    root.geometry("480x360")
    LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
