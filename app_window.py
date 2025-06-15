# app_window.py
import tkinter as tk
from tkinter import ttk
import platform

# Import UI components from their new modules
from tabs.home_tab import HomeTab
from tabs.shutdown_tab import ShutdownTab
from tabs.cleaner_tab import SystemCleanerTab
from views.settings_view import SettingsView

class MasterTool:
    """The main application class that builds and manages the user interface."""
    def __init__(self, master: tk.Tk):
        """Initializes the main application window."""
        self.master = master
        master.title("MasterTool")
        master.geometry("550x380")
        master.minsize(500, 380)
        
        # --- Main Notebook for Tabs ---
        self.notebook = ttk.Notebook(master)
        
        # --- Create and Add Tabs ---
        home_tab = HomeTab(self.notebook, self.show_settings)
        shutdown_tab = ShutdownTab(self.notebook)

        self.notebook.add(home_tab, text='Home')
        
        # The System Cleaner is a Windows-only feature
        if platform.system() == "Windows":
             cleaner_tab = SystemCleanerTab(self.notebook)
             self.notebook.add(cleaner_tab, text='System Cleaner')

        self.notebook.add(shutdown_tab, text='Shutdown Timer')

        # --- Settings View (initially hidden) ---
        self.settings_frame = SettingsView(self.master, self.master, self.show_tabs)
        
        # Show the main tabs by default
        self.show_tabs()

    def handle_back_navigation(self, event=None):
        """Callback for mouse-button back navigation."""
        self.show_tabs()

    def show_settings(self):
        """Hides the main notebook and shows the settings view."""
        self.notebook.pack_forget()
        self.settings_frame.pack(expand=True, fill='both')
        self.master.bind("<Button-4>", self.handle_back_navigation)
        self.master.bind("<Button-5>", self.handle_back_navigation)

    def show_tabs(self):
        """Hides the settings view and shows the main notebook."""
        self.settings_frame.pack_forget()
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.master.unbind("<Button-4>")
        self.master.unbind("<Button-5>")