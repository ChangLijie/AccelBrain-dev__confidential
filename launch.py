# launcher.py

from tools import BASE_DIR
from tools.checker.env_checker import check_all_env
from tools.gui.launcher import (
    create_gui,
    load_theme,
    run_check_sequence,
    setup_log_handler,
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
    root, status_labels, log_box = create_gui(theme)
    log_func = setup_log_handler(log_box)
    root.after(
        300,
        lambda: run_check_sequence(
            root, BASE_DIR, check_all_env, status_labels, log_func
        ),
    )
    root.mainloop()


if __name__ == "__main__":
    main()
