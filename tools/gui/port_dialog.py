# tools/gui/port_dialog.py
import http.client
import json
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Tuple

from tools.checker.port_checker import is_port_in_use
from tools.utils import auto_install_dependencies


def check_and_color(entry: tk.Entry, label: tk.Label) -> bool:
    try:
        port = int(entry.get())
        port_in_use = is_port_in_use(port)
        entry.config(bg="lightgreen" if not port_in_use else "lightcoral")
        label.config(
            text="✅ Available" if not port_in_use else "❌ Occupied",
            fg="green" if not port_in_use else "red",
        )
        return not port_in_use
    except ValueError:
        entry.config(bg="lightcoral")
        label.config(text="❌ Illegal input", fg="red")
        return False


def build_port_entry(root, key: str, value: dict, entries, status_labels):
    frame = tk.Frame(root)
    label_key = tk.Label(frame, text=f"{key}", width=12, anchor="w")
    label_key.pack(side="left", padx=(20, 5))
    entry = tk.Entry(frame, width=10)
    entry.insert(0, str(value["port"]))
    entry.pack(side="left", padx=5)
    label = tk.Label(frame, text="", width=12, anchor="w")
    label.pack(side="left", padx=5)

    entries[(key, "port")] = entry
    status_labels[(key, "port")] = label

    entry.bind("<KeyRelease>", lambda e, en=entry, la=label: check_and_color(en, la))
    check_and_color(entry, label)
    return frame


def build_max_model_entry(root, settings, entries):
    frame = tk.Frame(root)
    label = tk.Label(frame, text="Max Model Load", width=16, anchor="w")
    label.pack(side="left", padx=(20, 5))
    max_models_entry = tk.Entry(frame, width=10)
    max_models_entry.insert(
        0, str(settings["model_server"].get("MODEL_SERVER_MAX_LOADED_MODELS", 3))
    )
    max_models_entry.pack(side="left")
    entries[("model_server", "MODEL_SERVER_MAX_LOADED_MODELS")] = max_models_entry
    return frame


def build_accelbrain_status_row(root, port: int):
    frame = tk.Frame(root)
    label_left = tk.Label(
        frame,
        text="AccelBrain Status",
        font=("Arial", 12, "bold"),
        width=16,
        anchor="w",
    )
    label_left.pack(side="left", padx=(20, 5))
    status_label = tk.Label(
        frame, text="Checking...", width=20, fg="gray", font=("Arial", 12, "bold")
    )
    status_label.pack(side="left")

    def check_service():
        try:
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
            conn.request("GET", "/")
            resp = conn.getresponse()
            if resp.status == 200:
                status_label.config(text="Running", fg="green")
                frame.running = True
            else:
                status_label.config(text=f"HTTP {resp.status}", fg="orange")
                frame.running = False
        except Exception:
            status_label.config(text="Not running", fg="red")
            frame.running = False

    check_service()
    return frame


def collect_and_validate(entries, status_labels, settings):
    all_ok = True
    for (key, field), entry in entries.items():
        if field == "port" and not check_and_color(entry, status_labels[(key, field)]):
            all_ok = False
    if not all_ok:
        return False

    for (key, field), entry in entries.items():
        try:
            val = int(entry.get())
            settings[key][field] = val
        except ValueError:
            messagebox.showerror("Error", f"field {key}.{field} must be integer.")
            return False
    return True


def save_settings_to_file(settings: dict, path: str = "setting/setting.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def show_port_edit_dialog(settings):
    auto_install_dependencies()
    updated = False
    root = tk.Tk()
    root.title("Setting")
    root.geometry("400x300")

    entries: Dict[Tuple[str, str], tk.Entry] = {}
    status_labels: Dict[Tuple[str, str], tk.Label] = {}

    chatbot_port = settings.get("chatbot", {}).get("port", 3000)
    brain_status_frame = build_accelbrain_status_row(root, chatbot_port)
    brain_status_frame.pack(pady=(20, 15), anchor="w")

    for key, value in settings.items():
        if isinstance(value, dict) and "port" in value:
            frame = build_port_entry(root, key, value, entries, status_labels)
            frame.pack(pady=6, anchor="w")

    max_frame = build_max_model_entry(root, settings, entries)
    max_frame.pack(pady=10, anchor="w")

    def save():
        nonlocal updated
        if getattr(brain_status_frame, "running", False):
            messagebox.showwarning(
                "AccelBrain is running",
                "Please stop AccelBrain before modifying settings.",
            )
            return

        if not collect_and_validate(entries, status_labels, settings):
            messagebox.showerror(
                "Error", "Please correct the red fields before saving."
            )
            return

        save_settings_to_file(settings)
        updated = True
        root.destroy()

    tk.Button(root, text="Save Setting", command=save).pack(pady=20)
    root.mainloop()
    return updated
