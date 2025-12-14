import tkinter as tk
from tkinter import ttk

# --- CONFIGURATION MATCHING LOGIN & ADMIN WIDOW ---
COLORS = {
    "bg": "#f0f2f5",          # Main background
    "card": "#ffffff",        # Card background
    "primary": "#4a90e2",     # Primary Action (Blue)
    "primary_hover": "#357abd",
    "text_dark": "#2d3436",   # Main Text
    "text_grey": "#636e72",   # Subtitle/Label Text
    "danger": "#d63031",      # Red
    "danger_hover": "#c0392b",
    "success": "#2ecc71",     # Green
    "input_bg": "#f7f9fc",
    "border": "#e1e4e8"
}

FONTS = {
    "h1": ("Segoe UI", 24, "bold"),
    "h2": ("Segoe UI", 14, "bold"),
    "h3": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "small": ("Segoe UI", 9),
    "btn": ("Segoe UI", 10, "bold"),
}

def setup_global_styles():
    """Configures global ttk styles to match the theme."""
    style = ttk.Style()
    style.theme_use("clam")
    
    # Generic Notebook
    style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
    style.configure("TNotebook.Tab", 
                    background=COLORS["bg"], 
                    foreground=COLORS["text_grey"],
                    padding=(20, 10),
                    font=FONTS["btn"])
    style.map("TNotebook.Tab", 
              background=[("selected", COLORS["primary"])], 
              foreground=[("selected", "white")])

    # Treeview (Table)
    style.configure("Treeview", 
                    background="white",
                    fieldbackground="white",
                    foreground=COLORS["text_dark"],
                    rowheight=40, # More spacious
                    font=FONTS["body"],
                    borderwidth=0)
    style.configure("Treeview.Heading", 
                    background=COLORS["bg"],
                    foreground=COLORS["text_dark"],
                    font=FONTS["btn"],
                    relief="flat")
    style.map("Treeview", background=[("selected", COLORS["primary"])])
    
    # Standard Label
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text_dark"], font=FONTS["body"])
    
    # Card Frames
    style.configure("Card.TFrame", background=COLORS["card"])
    style.configure("Main.TFrame", background=COLORS["bg"])

def create_card(parent, padding=20):
    """Creates a white card frame."""
    card = tk.Frame(parent, bg=COLORS["card"], padx=padding, pady=padding)
    return card

def create_button(parent, text, command, type="primary", width=None):
    """Creates a styled Tkinter Button."""
    bg_color = COLORS["primary"] if type == "primary" else COLORS["danger"] if type == "danger" else COLORS["text_grey"]
    
    btn = tk.Button(
        parent,
        text=text,
        font=FONTS["btn"],
        bg=bg_color,
        fg="white",
        activebackground=bg_color, # Simplification
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        pady=10,
        command=command
    )
    if width:
        btn.config(width=width)

    # Hover Effects
    def on_enter(e):
        hover_col = "#357abd" if type == "primary" else "#c0392b" if type == "danger" else "#2d3436"
        btn.config(bg=hover_col)
    
    def on_leave(e):
        btn.config(bg=bg_color)
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

def create_entry_with_label(parent, label_text, variable=None, is_password=False):
    """Creates a label + underlined entry pair."""
    # Label
    tk.Label(
        parent, 
        text=label_text, 
        font=("Segoe UI", 9, "bold"), 
        bg=COLORS["card"], 
        fg=COLORS["text_grey"]
    ).pack(anchor="w", pady=(10, 5))
    
    # Container for Entry (to handle underline and padding)
    container = tk.Frame(parent, bg=COLORS["card"])
    container.pack(fill="x")
    
    entry = tk.Entry(
        container,
        font=("Segoe UI", 11),
        bg=COLORS["input_bg"],
        relief="flat",
        textvariable=variable,
        show="•" if is_password else ""
    )
    entry.pack(fill="x", ipady=8, padx=10) # ipady makes it taller

    # Animated Underline
    line = tk.Frame(container, bg=COLORS["border"], height=2)
    line.pack(fill="x", side="bottom")

    def on_focus(e): line.config(bg=COLORS["primary"])
    def on_blur(e): line.config(bg=COLORS["border"])
    
    entry.bind("<FocusIn>", on_focus)
    entry.bind("<FocusOut>", on_blur)
    
    return entry
