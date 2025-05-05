# tools/checker/env_checker.py
import os
import shutil
import subprocess
from typing import List, Tuple

from tools import BASE_DIR


def is_installed(command: str) -> bool:
    return shutil.which(command) is not None


def check_command(command: List[str]) -> bool:
    try:
        subprocess.run(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        return True
    except Exception:
        return False


def check_all_env() -> List[Tuple[str, bool]]:
    def exists(relative):
        return os.path.exists(os.path.join(BASE_DIR, relative))

    checks = [
        (
            "NVIDIA Driver (nvidia-smi)",
            is_installed("nvidia-smi") and check_command(["nvidia-smi"]),
        ),
        ("Docker", is_installed("docker") and check_command(["docker", "version"])),
        (
            "NVIDIA Docker (nvidia-container-cli)",
            is_installed("nvidia-container-cli")
            and check_command(["nvidia-container-cli", "--version"]),
        ),
        # ("setting.json", exists("setting/setting.json")),
        # ("nginx.conf", exists("setting/nginx.conf")),
        # ("docker-compose.yml", exists("docker-compose.yml")),
        # ("CHANGELOG.md", exists("CHANGELOG.md")),
    ]
    return checks
