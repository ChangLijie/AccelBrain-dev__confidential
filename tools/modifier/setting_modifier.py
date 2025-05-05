# tools/modifier/setting_modifier.py
import json
import os
import re

import yaml

from tools import BASE_DIR


def load_settings(setting_path):
    with open(setting_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_settings(setting_path, settings):
    with open(setting_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def update_ports_and_env(setting_path, compose_path, nginx_conf_path):
    settings = load_settings(setting_path)

    def abspath(relative):
        full_path = os.path.join(BASE_DIR, relative)
        # If it's a folder and doesn't exist, create it (skip files)
        if not os.path.splitext(relative)[1] and not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
        return full_path.replace(os.sep, "/")

    # 1. Update docker-compose.yml
    with open(compose_path, "r", encoding="utf-8") as f:
        compose_data = yaml.safe_load(f)

    ports_to_update = {
        "nginx": settings["nginx"]["port"],
        "chatbot": settings["chatbot"]["port"],
    }

    for service, port in ports_to_update.items():
        if service in compose_data["services"]:
            container_port = compose_data["services"][service]["ports"][0].split(":")[
                -1
            ]
            compose_data["services"][service]["ports"][0] = f"{port}:{container_port}"

    # Update volumes as absolute path.
    volume_map = {
        "chatbot": [
            ("chatbot/data", "/app/backend/data"),
            ("CHANGELOG.md", "/app/CHANGELOG.md"),
        ],
        "model_handler": [
            ("model_handler/log", "/workspace/log"),
            ("models", "/workspace/models"),
        ],
        "model_server": [("models/ollama", "/root/.ollama"), ("models/inno", "/home")],
        "nginx": [("setting/nginx.conf", "/etc/nginx/nginx.conf:ro")],
    }

    for service, mounts in volume_map.items():
        if service in compose_data["services"]:
            compose_data["services"][service]["volumes"] = [
                f"{abspath(src)}:{target}" for src, target in mounts
            ]

    # Update env parameter.
    new_env = [
        f"OLLAMA_MAX_LOADED_MODELS={settings['model_server']['MODEL_SERVER_MAX_LOADED_MODELS']}"
    ]
    compose_data["services"]["model_server"]["environment"] = new_env

    with open(compose_path, "w", encoding="utf-8") as f:
        yaml.dump(compose_data, f, default_flow_style=False, sort_keys=False)

    # 2. update nginx.conf (listen port)
    with open(nginx_conf_path, "r", encoding="utf-8") as f:
        nginx_conf = f.read()

    nginx_port = settings["nginx"]["port"]
    nginx_conf = re.sub(r"listen \d+;", f"listen {nginx_port};", nginx_conf)

    with open(nginx_conf_path, "w", encoding="utf-8") as f:
        f.write(nginx_conf)

    print(
        "✅ Configuration has been updated based on setting.json. Docker Compose and nginx settings (including absolute paths for all volumes) are now synchronized."
    )
