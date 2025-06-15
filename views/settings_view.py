# views/settings_view.py
import tkinter as tk
from tkinter import ttk
import sv_ttk

from utils.windows_api import set_dark_title_bar, apply_system_theme

class SettingsView(ttk.Frame):
    """The UI and logic for the settings area."""
    def __init__(self, parent, root_window, show_tabs_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.root_window = root_window
        self.always_on_top_var = tk.BooleanVar(value=root_window.attributes("-topmost"))
        
        top_bar = ttk.Frame(self)
        top_bar.pack(fill='x', padx=10, pady=(10,0))
        back_button = ttk.Button(top_bar, text="< Back", command=show_tabs_callback)
        back_button.pack(side='left')
        
        # --- Appearance ---
        theme_frame = ttk.LabelFrame(self, text="Appearance", padding=15)
        theme_frame.pack(expand=True, fill='x', padx=20, pady=(10, 10))
        
        ttk.Label(theme_frame, text="Theme:").pack(side="left", padx=(0, 10))
        self.theme_combobox = ttk.Combobox(theme_frame, values=['System', 'Dark', 'Light'], state="readonly")
        self.theme_combobox.pack(side="left", fill='x', expand=True)
        current_theme = sv_ttk.get_theme().capitalize()
        self.theme_combobox.set('System' if current_theme not in ['Dark', 'Light'] else current_theme)
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)
        
        # --- Window Behavior ---
        window_frame = ttk.LabelFrame(self, text="Window Behavior", padding=15)
        window_frame.pack(expand=True, fill='x', padx=20, pady=10)
        self.on_top_check = ttk.Checkbutton(window_frame, text="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        self.on_top_check.pack(anchor='w')
        
        # --- Info ---
        info_frame = ttk.Frame(self, padding=15)
        info_frame.pack(side='bottom', fill='x', padx=10)
        ttk.Label(info_frame, text="MasterTool v1.0", foreground="gray").pack(side='right')

    def change_theme(self, event=None):
        """Changes the application theme."""
        selection = self.theme_combobox.get()
        if selection == 'System':
            apply_system_theme()
        else:
            sv_ttk.set_theme(selection.lower())
        set_dark_title_bar(self.root_window)

    def toggle_always_on_top(self):
        """Toggles the window's always-on-top attribute."""
        self.root_window.attributes("-topmost", self.always_on_top_var.get())