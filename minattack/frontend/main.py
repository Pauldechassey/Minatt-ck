import sys
import os
from multiprocessing import Process
import time
from PySide6.QtWidgets import QApplication
from minattack.backend.backend_launcher import run_backend
from minattack.frontend.windows.MainWindow import MainWindow
from minattack.frontend.utils.port_handler import find_available_port
from minattack.shared.env import set_dynamic_backend_port


def main():
    backend_port = find_available_port()
    set_dynamic_backend_port(backend_port)

    print(f"[FRONTEND] Running in PID: {os.getpid()}")
    print(f"[INFO] Backend running on port: {backend_port}")

    backend_process = Process(target=run_backend, args=(backend_port,), daemon=True)
    backend_process.start()

    time.sleep(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    exit_code = app.exec()

    backend_process.terminate()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
