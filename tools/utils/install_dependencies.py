import subprocess


def auto_install_dependencies(log_func=None):
    def try_apt(pkg):
        if log_func:
            log_func(f"🔧 Checking `{pkg}`...\n")
        result = subprocess.run(
            ["dpkg", "-s", pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            if log_func:
                log_func(f"📦 Installing `{pkg}`...\n")
            subprocess.run(["sudo", "apt", "install", "-y", pkg])

    def try_pip(pkg):
        if log_func:
            log_func(f"🔧 Checking Python package `{pkg}`...\n")
        try:
            __import__(pkg)
        except ImportError:
            if log_func:
                log_func(f"📦 Installing `{pkg}`...\n")
            subprocess.run(["pip3", "install", pkg])

    try_apt("python3-tk")
    try_apt("unifont")
    try_pip("yaml")
