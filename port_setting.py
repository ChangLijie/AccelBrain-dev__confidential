# launcher.py
import os

from tools import BASE_DIR
from tools.gui.port_dialog import show_port_edit_dialog
from tools.modifier.setting_modifier import load_settings, update_ports_and_env


def main():
    setting_path = os.path.join(BASE_DIR, "setting", "setting.json")
    docker_compose_path = os.path.join(BASE_DIR, "docker-compose.yml")
    nginx_setting_path = os.path.join(BASE_DIR, "setting", "nginx.conf")
    settings = load_settings(setting_path)
    updated = show_port_edit_dialog(settings)
    if updated:
        update_ports_and_env(
            setting_path=setting_path,
            compose_path=docker_compose_path,
            nginx_conf_path=nginx_setting_path,
        )


if __name__ == "__main__":
    main()
