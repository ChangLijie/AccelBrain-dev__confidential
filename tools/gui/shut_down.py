# tools/gui/progress_ui.py
import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext

from tools.gui.log_buffer import set_log_handler
from tools.utils import DotDict

# from tools.utils import DotDict, auto_install_dependencies

SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def create_gui(theme_setting):
    root = tk.Tk()
    root.title(theme_setting.title)
    root.geometry(theme_setting.window_size)
    root.configure(bg=theme_setting.background_color)

    header = tk.Label(
        root,
        text=theme_setting.header_label.text,
        font=theme_setting.header_label.font,
        bg=theme_setting.header_label.background_color,
        name="header_label",  # <-- 為了之後修改方便加上 name
    )
    header.pack(pady=theme_setting.header_label.padding_y)

    log_box = scrolledtext.ScrolledText(root, height=10, font=("Courier New", 10))
    log_box.pack(
        fill=theme_setting.log_box.fill,
        padx=theme_setting.log_box.padding_x,
        pady=theme_setting.log_box.padding_y,
        expand=theme_setting.log_box.expand,
    )

    return root, log_box


def setup_log_handler(log_box):
    def log_to_box(line):
        try:
            if log_box.winfo_exists():
                log_box.insert(tk.END, line)
                log_box.see(tk.END)
                log_box.update_idletasks()  # 即時刷新 GUI
        except tk.TclError:
            pass

    def safe_append_log(line):
        try:
            log_to_box(line)
        except Exception:
            pass

    set_log_handler(log_to_box)
    return safe_append_log


def run_and_stream(cmd, log_func):
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
    )
    for line in proc.stdout:
        log_func(line)
    proc.wait()


def load_theme():
    return DotDict(
        {
            "title": "AccelBrain Shut down",
            "window_size": "640x480",
            "background_color": "white",
            "header_label": {
                "text": "🔍 Stop ...",
                "font": ("Arial", 14, "bold"),
                "background_color": "white",
                "padding_y": 12,
            },
            "check_items": {
                "labels": [
                    "NVIDIA Driver (nvidia-smi)",
                    "Docker",
                    "NVIDIA Docker (nvidia-container-cli)",
                    "Check necessary file",
                ],
                "font": ("Courier New", 11),
                "font_location": {"anchor": "w", "justify": "left"},
                "background_color": "white",
                "not_finished_color": "gray",
                "fill": "x",
                "padding_x": 30,
                "padding_y": 2,
            },
            "log_box": {
                "fill": "both",
                "padding_x": 20,
                "padding_y": (10, 5),
                "expand": True,
            },
        }
    )


def stop_accelbrain(root_path: str, log_func):
    # auto_install_dependencies(log_func)
    log_func("🧹 Stopping existing AccelBrain containers...\n")
    stop_sh_path = os.path.join(root_path, "stop.sh")
    run_and_stream(["bash", stop_sh_path], log_func)

    # 成功後更新標題為 Stop ✅
    try:
        header_label = tk._default_root.nametowidget("header_label")
        header_label.config(text="✅ Stop Success", fg="green")
    except Exception:
        pass
