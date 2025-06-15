# utils/windows_api.py
import platform
import ctypes
from ctypes import wintypes
import sv_ttk

def set_dark_title_bar(window):
    """Sets the title bar to dark mode on Windows 10/11."""
    if platform.system() == 'Windows':
        try:
            value = ctypes.c_int(2) if sv_ttk.get_theme() == "dark" else ctypes.c_int(0)
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception: pass

def apply_system_theme():
    """Applies the current Windows theme (light/dark) to the app."""
    try:
        if platform.system() == "Windows":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            sv_ttk.set_theme("light" if value == 1 else "dark")
        else:
            sv_ttk.set_theme("dark")
    except Exception:
        sv_ttk.set_theme("dark")

def get_recycle_bin_size():
    """Gets the Recycle Bin size instantly using a Windows API call."""
    class SHQUERYRBINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', wintypes.DWORD),
            ('i64Size', ctypes.c_longlong),
            ('i64NumItems', ctypes.c_longlong),
        ]
    
    try:
        shell32 = ctypes.windll.shell32
        info = SHQUERYRBINFO()
        info.cbSize = ctypes.sizeof(info)
        result = shell32.SHQueryRecycleBinW(None, ctypes.byref(info))
        if result == 0: # S_OK
            return info.i64Size
    except Exception as e:
        print(f"Failed to get Recycle Bin size via WinAPI: {e}")
    return 0

def empty_recycle_bin():
    """Empties the Recycle Bin using a direct Windows API call."""
    try:
        # Flags: No confirmation, no progress UI, no sound
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 1 | 2 | 4)
        if result != 0:
            print(f"SHEmptyRecycleBinW failed with code: {result}")
    except Exception as e:
        print(f"Error emptying recycle bin: {e}")