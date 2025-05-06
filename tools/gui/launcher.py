# tools/gui/progress_ui.py
import http.client
import json
import os
import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

from tools.checker.necessary_file_checker import check_necessary_file
from tools.checker.port_checker import check_ports
from tools.gui.log_buffer import set_log_handler
from tools.gui.port_dialog import show_port_edit_dialog
from tools.modifier.setting_modifier import load_settings, update_ports_and_env
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
        name="header_label",
    )
    header.pack(pady=theme_setting.header_label.padding_y)

    status_labels = []
    for name in theme_setting.check_items.labels:
        display = (
            f"Necessary file {name}"
            if name.endswith((".json", ".conf", ".yml", ".md"))
            else name
        )
        lbl = tk.Label(
            root,
            text=f"\u1f501 {display:<45}",
            font=theme_setting.check_items.font,
            bg=theme_setting.check_items.background_color,
            fg=theme_setting.check_items.not_finished_color,
            anchor=theme_setting.check_items.font_location.anchor,
            justify=theme_setting.check_items.font_location.justify,
        )
        lbl.pack(
            fill=theme_setting.check_items.fill,
            padx=theme_setting.check_items.padding_x,
            pady=theme_setting.check_items.padding_y,
        )
        status_labels.append(lbl)

    log_box = scrolledtext.ScrolledText(root, height=10, font=("Courier New", 10))
    log_box.pack(
        fill=theme_setting.log_box.fill,
        padx=theme_setting.log_box.padding_x,
        pady=theme_setting.log_box.padding_y,
        expand=theme_setting.log_box.expand,
    )

    return root, status_labels, log_box


def setup_log_handler(log_box):
    def log_to_box(line):
        try:
            if log_box.winfo_exists():
                start = log_box.index(tk.END)
                log_box.insert(tk.END, line)
                end = log_box.index(tk.END)
                if "http://" in line or "https://" in line:
                    log_box.tag_add("link", start, end)
                    log_box.tag_config("link", foreground="blue", underline=True)
                log_box.see(tk.END)
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
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    for line in proc.stdout:
        log_func(line)
    proc.wait()


def load_theme():
    return DotDict(
        {
            "title": "AccelBrain Luncher",
            "window_size": "640x480",
            "background_color": "white",
            "header_label": {
                "text": "\U0001f50d Launching...",
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


def run_check_sequence(root, root_path, check_function, status_labels, log_func):
    # auto_install_dependencies(log_func)

    def spinner_loop():
        i = 0
        while not result_holder["done"]:
            for lbl in status_labels:
                if lbl.cget("fg") == "gray":
                    spinner = SPINNER_FRAMES[i % len(SPINNER_FRAMES)]
                    lbl.config(text=f"{spinner} {lbl.cget('text')[2:]}")
            i += 1
            root.update_idletasks()
            time.sleep(0.1)

    def check_thread():
        result_holder["done"] = False

        log_func("🔍 Starting environment, required file, and port conflict check...\n")
        env_results = check_function()
        file_result = check_necessary_file()

        for i, (name, success) in enumerate(env_results):
            icon = "✅" if success else "❌"
            color = "green" if success else "red"
            status_labels[i].config(text=f"{icon:<2} {name:<45}", fg=color, anchor="w")
            root.update_idletasks()
            time.sleep(0.3)

        icon = "✅" if all(success for _, success in file_result) else "❌"
        color = "green" if all(success for _, success in file_result) else "red"
        status_labels[-1].config(
            text=f"{icon:<2} {'Check necessary file':<45}", fg=color, anchor="w"
        )
        root.update_idletasks()
        time.sleep(0.3)
        result_holder["env_results"] = env_results
        result_holder["done"] = True

        if not all(success for _, success in env_results) or not all(
            success for _, success in file_result
        ):
            missing = [
                name
                for group in (env_results, file_result)
                for name, success in group
                if not success
            ]
            msg = (
                "The following environment or required files are missing:\n\n"
                + "\n".join(f"- {name}" for name in missing)
            )
            messagebox.showerror("Environment Check Failed", msg)
            log_func(
                f"⏳Environment Check Failed, {msg}\n\n\n AccelBrain Failed to launch.\n"
            )
        else:
            log_func("🧹 Stopping existing AccelBrain containers...\n")
            stop_sh_path = os.path.join(root_path, "stop.sh")
            run_and_stream(["bash", stop_sh_path], log_func)

            setting_path = os.path.join(root_path, "setting", "setting.json")
            docker_compose_path = os.path.join(root_path, "docker-compose.yml")
            nginx_setting_path = os.path.join(root_path, "setting", "nginx.conf")

            settings = load_settings(setting_path)
            port_conflict = check_ports(settings)
            if port_conflict:
                updated = show_port_edit_dialog(settings)
                if updated:
                    update_ports_and_env(
                        setting_path=setting_path,
                        compose_path=docker_compose_path,
                        nginx_conf_path=nginx_setting_path,
                    )

            log_func("🚀 Launching AccelBrain...\n\n")
            run_sh_path = os.path.join(root_path, "run_compose.sh")
            run_and_stream(["bash", run_sh_path], log_func)

            with open(setting_path) as f:
                port = json.load(f).get("chatbot", {}).get("port", 3000)
            url = f"http://127.0.0.1:{port}"
            log_func(f"🔎 Checking backend service readiness: {url}\n")

            for i in range(30):
                try:
                    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
                    conn.request("GET", "/")
                    resp = conn.getresponse()
                    if resp.status == 200:
                        log_func("✅ Backend HTTP responded 200. Service is ready.\n")
                        subprocess.Popen(["xdg-open", url])
                        break
                    else:
                        log_func(
                            f"⏳ Response code {resp.status}. Backend not ready yet.\n"
                        )
                except Exception:
                    log_func(f"⏳ Waiting for backend to start... ({i + 1}/30)\n")
                time.sleep(1)
            else:
                log_func("❌ Backend did not start in the expected time.\n")

            log_func("✅ AccelBrain is up and running! You may now close this window.")
            header_label = tk._default_root.nametowidget("header_label")
            header_label.config(text="✅ Launch Success", fg="green")

    result_holder = {"done": False, "results": []}
    threading.Thread(target=check_thread, daemon=True).start()
    threading.Thread(target=spinner_loop, daemon=True).start()
