import os
from typing import List, Tuple

from tools import BASE_DIR


def check_necessary_file() -> List[Tuple[str, bool]]:
    def exists(relative):
        return os.path.exists(os.path.join(BASE_DIR, relative))

    checks = [
        ("setting.json", exists("setting/setting.json")),
        ("nginx.conf", exists("setting/nginx.conf")),
        ("docker-compose.yml", exists("docker-compose.yml")),
        ("CHANGELOG.md", exists("CHANGELOG.md")),
    ]
    return checks
