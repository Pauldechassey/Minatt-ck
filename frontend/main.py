import sys
import subprocess
import time
from PySide6.QtWidgets import QApplication
from windows.MainWindow import MainWindow
from frontend.utils.env import load_env, get_path, get_backend_url, get_backend_port

def main():
    load_env()

    backend_path = get_path("backend/backend_launcher.py")
    root_dir = get_path(".")

    backend_process = subprocess.Popen(
        [sys.executable, backend_path, str(get_backend_port())],
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