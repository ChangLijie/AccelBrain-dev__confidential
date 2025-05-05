# launcher.py

from tools import BASE_DIR
from tools.gui.shut_down import (
    create_gui,
    load_theme,
    setup_log_handler,
    stop_accelbrain,
)


def main():
    # 顯示環境檢查與 docker compose 啟動進度（帶 log）
    # env_ok = show_env_check_ui(BASE_DIR, check_all_env)
    # if not env_ok:
    #     return

    # 檢查 port 狀態，必要時開啟 GUI 讓使用者修改
    # settings = load_settings("setting/setting.json")
    # port_conflict = check_ports(settings)
    # if port_conflict:
    #     updated = show_port_edit_dialog(settings)
    #     if updated:
    #         update_ports_and_env(
    #             setting_path="setting/setting.json",
    #             compose_path="docker-compose.yml",
    #             nginx_conf_path="setting/nginx.conf",
    #         )

    theme = load_theme()
    root, log_box = create_gui(theme)
    log_func = setup_log_handler(log_box)
    root.after(
        300,
        lambda: stop_accelbrain(BASE_DIR, log_func),
    )
    root.mainloop()


if __name__ == "__main__":
    main()
