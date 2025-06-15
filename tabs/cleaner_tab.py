# tabs/cleaner_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import threading
from datetime import datetime

# Import the logic and helper functions from our new modules
from utils.windows_api import get_recycle_bin_size, empty_recycle_bin
from utils.helpers import get_dir_size, format_bytes, clean_directory

class SystemCleanerTab(ttk.Frame):
    """The UI and logic for the System Cleaner tab."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # --- UI Layout ---
        top_frame = ttk.Frame(self); top_frame.pack(pady=(15, 5), padx=20, fill="x")
        self.scan_button = ttk.Button(top_frame, text="Scan", style="Accent.TButton", command=self.start_scan)
        self.scan_button.pack(side="left")
        self.total_size_label = ttk.Label(top_frame, text="Total Selected: 0 B", font=("", 10, "bold")); self.total_size_label.pack(side="right")
        
        self.last_scanned_label = ttk.Label(self, text="Last scanned: Never", style="Secondary.TLabel")
        self.last_scanned_label.pack(padx=20, anchor="w", pady=(0, 5))

        self.options_frame = ttk.Frame(self, padding=(0, 10))
        self.options_frame.pack(pady=5, padx=20, fill="both", expand=True)

        self.categories = {
            "temp": {"name": "Temporary Files", "var": tk.BooleanVar(value=True), "path": os.environ.get('TEMP')},
            "recycle_bin": {"name": "Recycle Bin", "var": tk.BooleanVar(value=False), "path": "shell:RecycleBinFolder"},
            "downloads": {"name": "Downloads", "var": tk.BooleanVar(value=False), "path": os.path.join(os.path.expanduser('~'), 'Downloads')},
        }
        
        self.options_frame.columnconfigure(0, weight=1)
        
        for key, data in self.categories.items():
            data["size"] = 0
            data["size_label_var"] = tk.StringVar(value="-")
            row = len(self.options_frame.grid_slaves(column=0))
            name_frame = ttk.Frame(self.options_frame); name_frame.grid(row=row, column=0, sticky="w")
            chk = ttk.Checkbutton(name_frame, variable=data["var"], command=self.update_total_size); chk.pack(side="left")
            name_label = ttk.Label(name_frame, text=data["name"]); name_label.pack(side="left")
            size_label = ttk.Label(self.options_frame, textvariable=data["size_label_var"], style="Secondary.TLabel"); size_label.grid(row=row, column=1, sticky="e", padx=10)
            open_button = ttk.Button(self.options_frame, text="📂", width=3, command=lambda p=data["path"]: self.open_path_in_explorer(p)); open_button.grid(row=row, column=2, sticky="e")

        bottom_frame = ttk.Frame(self); bottom_frame.pack(pady=(10, 20), padx=20, fill="x")
        self.clean_button = ttk.Button(bottom_frame, text="Clean Selected", command=self.start_cleanup, state="disabled"); self.clean_button.pack(side="left")
        self.status_label = ttk.Label(bottom_frame, text="Ready. Click Scan to begin."); self.status_label.pack(side="right")

    def open_path_in_explorer(self, path):
        if not path: return
        try:
            if os.path.exists(path): os.startfile(path)
            elif path == "shell:RecycleBinFolder": subprocess.Popen(f'explorer.exe {path}', shell=True)
            else: messagebox.showinfo("Path Not Found", f"The folder '{path}' does not exist.")
        except Exception as e: messagebox.showerror("Error", f"Could not open the folder:\n{e}")

    def start_scan(self):
        self.scan_button.config(state="disabled"); self.clean_button.config(state="disabled")
        self.status_label.config(text="Scanning...")
        threading.Thread(target=self.scan_thread_worker, daemon=True).start()

    def scan_thread_worker(self):
        sizes = {}
        self.status_label.config(text="Scanning files...")
        sizes['temp'] = get_dir_size(self.categories['temp']['path'])
        sizes['downloads'] = get_dir_size(self.categories['downloads']['path'])
        
        self.status_label.config(text="Querying Recycle Bin...")
        sizes['recycle_bin'] = get_recycle_bin_size()
        
        self.master.after(0, self.update_ui_with_scan_results, sizes)

    def update_ui_with_scan_results(self, sizes):
        for key, data in self.categories.items():
            if key in sizes:
                data["size"] = sizes[key]
                data["size_label_var"].set(format_bytes(sizes[key]))
        self.last_scanned_label.config(text=f"Last scanned: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.status_label.config(text="Scan complete. Ready to clean.")
        self.scan_button.config(state="normal"); self.clean_button.config(state="normal")
        self.update_total_size()

    def update_total_size(self):
        total = sum(data["size"] for data in self.categories.values() if data["var"].get())
        self.total_size_label.config(text=f"Total Selected: {format_bytes(total)}")

    def start_cleanup(self):
        if self.categories['downloads']['var'].get():
            if not messagebox.askyesno("WARNING", "You have selected to delete the entire Downloads folder. This action is IRREVERSIBLE.\n\nAre you absolutely sure?", icon='warning'): return
        
        self.clean_button.config(state="disabled"); self.scan_button.config(state="disabled")
        self.status_label.config(text="Cleaning in progress...")
        threading.Thread(target=self.cleanup_thread_worker, daemon=True).start()

    def cleanup_thread_worker(self):
        if self.categories["temp"]["var"].get(): clean_directory(self.categories["temp"]["path"])
        if self.categories["downloads"]["var"].get(): clean_directory(self.categories["downloads"]["path"])
        if self.categories["recycle_bin"]["var"].get(): empty_recycle_bin()
        self.master.after(0, self.finish_cleanup)
        
    def finish_cleanup(self):
        self.status_label.config(text="Cleanup complete. Re-scanning...")
        messagebox.showinfo("Complete", "The selected items have been removed.")
        self.start_scan()