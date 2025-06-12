import sys
import os
from multiprocessing import Process, set_start_method
import time
from multiprocessing.spawn import freeze_support

from PySide6.QtWidgets import QApplication
import requests
from minattack.backend.backend_launcher import run_backend
from minattack.frontend.windows.MainWindow import MainWindow
from minattack.frontend.utils.port_handler import find_available_port
from minattack.shared.env import set_dynamic_backend_port


def wait_for_backend(port: int, timeout: float = 20.0) -> bool:
    deadline = time.time() + timeout
    url = f"http://127.0.0.1:{port}/health"
    while time.time() < deadline:
        try:
            response = requests.get(url, timeout=0.1)
            if response.ok:
                return True
        except requests.RequestException:
            pass
        time.sleep(0.1)
    return False


def main():
    backend_port = find_available_port()
    set_dynamic_backend_port(backend_port)

    print(f"[FRONTEND] Running in PID: {os.getpid()}")
    print(f"[INFO] Backend will run on port: {backend_port}")

    backend_process = Process(
        target=run_backend, args=(backend_port,), daemon=True
    )
    backend_process.start()

    if not wait_for_backend(backend_port):
        print("[INFO] Backend failed to start")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    exit_code = app.exec()

    backend_process.terminate()
    sys.exit(exit_code)


if __name__ == "__main__":
    freeze_support()
    set_start_method("spawn", force=True)
    main()
