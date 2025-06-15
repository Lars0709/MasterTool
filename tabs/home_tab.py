# tabs/home_tab.py
import tkinter as tk
from tkinter import ttk

class HomeTab(ttk.Frame):
    """The UI for the Home tab, containing app info and the settings button."""
    def __init__(self, parent, show_settings_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        title_label = ttk.Label(self, text="MasterTool", font=("", 18, "bold"))
        title_label.pack(pady=(40, 10))

        desc_label = ttk.Label(
            self,
            text="A collection of simple tools to help manage your PC.",
            wraplength=400,
            justify="center",
            style="Secondary.TLabel"
        )
        desc_label.pack(pady=(0, 30), padx=30)

        settings_button = ttk.Button(self, text="Settings", command=show_settings_callback)
        settings_button.pack(pady=20)