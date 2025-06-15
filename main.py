# main.py
import tkinter as tk
import ctypes
import platform

import sv_ttk
from app_window import MasterTool
from utils.helpers import resource_path
from utils.windows_api import apply_system_theme, set_dark_title_bar

if __name__ == "__main__":
    # Set high-DPI awareness for a crisp UI on Windows
    if platform.system() == "Windows":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except AttributeError:
            # For older versions of Windows
            pass

    # Create the main window
    root = tk.Tk()

    # Set the initial theme
    apply_system_theme()

    # Set the application icon
    try:
        icon_path = resource_path("black_hole.ico")
        root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not load application icon: {e}")

    # Create and run the application
    # ### FIXED ###: Instantiating the correct class name
    app = MasterTool(root)
    root.after(10, set_dark_title_bar, root)
    root.mainloop()