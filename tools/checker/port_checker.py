# tools/checker/port_checker.py
import socket


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def check_ports(settings: dict) -> dict:
    used_ports = {}
    for key, value in settings.items():
        if isinstance(value, dict) and "port" in value:
            port = value["port"]
            if is_port_in_use(port):
                used_ports[key] = is_port_in_use(port)
    if used_ports:
        return used_ports
    return False
