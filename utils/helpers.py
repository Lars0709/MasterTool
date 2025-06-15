# utils/helpers.py
import os
import sys
import shutil
import math

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_dir_size(path='.'):
    """
    Calculates the total size of a directory.
    Uses os.walk for robust traversal, skipping symlinks and ignoring errors.
    """
    total = 0
    if not path or not os.path.exists(path):
        return 0
    try:
        for dirpath, _, filenames in os.walk(path, topdown=True, followlinks=False):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    try:
                        total += os.path.getsize(fp)
                    except FileNotFoundError:
                        continue 
    except PermissionError:
        pass
    return total

def clean_directory(dir_path):
    """Deletes all contents of a given directory."""
    if not dir_path or not os.path.exists(dir_path):
        return
    try:
        with os.scandir(dir_path) as it:
            for entry in it:
                try:
                    if entry.is_dir(follow_symlinks=False):
                        shutil.rmtree(entry.path)
                    else:
                        os.unlink(entry.path)
                except (PermissionError, FileNotFoundError, OSError):
                    continue
    except FileNotFoundError:
        pass

def format_bytes(size_bytes):
    """Formats bytes into a human-readable string (KB, MB, GB)."""
    if size_bytes <= 0: return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024))) if size_bytes > 0 else 0
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2) if i > 0 else size_bytes
    return f"{s} {size_name[i]}"