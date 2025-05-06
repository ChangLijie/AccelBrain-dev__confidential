# tools/gui/log_buffer.py
log_callback = None


def set_log_handler(callback):
    global log_callback
    log_callback = callback


def append_log(line: str):
    if log_callback:
        log_callback(line)
