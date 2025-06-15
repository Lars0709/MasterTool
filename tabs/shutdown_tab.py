# tabs/shutdown_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import platform
import subprocess

class ShutdownTab(ttk.Frame):
    """The UI and logic for the shutdown timer tab."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.label = ttk.Label(self, text="Shutdown in (minutes):")
        self.label.pack(pady=(20, 10))

        self.time_entry = ttk.Entry(self, width=12, justify="center")
        self.time_entry.pack(pady=10)
        self.time_entry.focus()

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.schedule_shutdown, style='Accent.TButton')
        self.start_button.pack(side="left", padx=5)

        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_shutdown)
        self.cancel_button.pack(side="left", padx=5)

    def schedule_shutdown(self):
        try:
            minutes = int(self.time_entry.get())
            if minutes <= 0:
                messagebox.showerror("Invalid Input", "Please enter a positive number of minutes.")
                return
            
            seconds = minutes * 60
            if platform.system() == "Windows":
                subprocess.run(f"shutdown /s /t {seconds}".split(), check=True)
            else:
                messagebox.showerror("Unsupported OS", "This feature is only for Windows.")
                return
            
            messagebox.showinfo("Success", f"Your PC will shut down in {minutes} minutes.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            messagebox.showerror("Error", f"Failed to schedule shutdown.\nDetails: {e}")

    def cancel_shutdown(self):
        if platform.system() == "Windows":
            try:
                subprocess.run("shutdown /a".split(), check=True)
                messagebox.showinfo("Cancelled", "The scheduled shutdown has been cancelled.")
            except (subprocess.CalledProcessError, FileNotFoundError):
                messagebox.showerror("Error", "No scheduled shutdown to cancel.")
        else:
            messagebox.showerror("Unsupported OS", "This feature is only for Windows.")