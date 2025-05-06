import sys
import os
import subprocess
import time
from PySide6.QtWidgets import QApplication
from windows.MainWindow import MainWindow
from utils.env import load_env, get_path, set_dynamic_backend_port
from utils.port_handler import find_available_port

def main():


    backend_port = find_available_port()
    set_dynamic_backend_port(backend_port)

    print(f"Backend running on port: {backend_port}")

    load_env()

    backend_launcher_path = get_path("backend/backend_launcher.py")
    root_dir = get_path(".")

    backend_process = subprocess.Popen(
        [sys.executable, backend_launcher_path, str(backend_port)],
        cwd=root_dir
    )

    time.sleep(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    exit_code = app.exec()
    backend_process.terminate()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()