import tkinter as tk

def global_logout(current_window_toplevel, root):
    """
    Destroys the current toplevel window, clears any children of root, 
    and re-initializes the LoginWindow on the root.
    """
    if current_window_toplevel:
        current_window_toplevel.destroy()
    
    # Clean up root children (in case anything else is lurking)
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
        # Note: We don't destroy root itself, keeping the main loop alive.

    # Re-import locally to avoid circular imports during startup
    from cafe_app.ui.login_window import LoginWindow
    LoginWindow(root)
