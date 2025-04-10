import sys
from model import UserModel
from PySide6.QtWidgets import QApplication
from windows.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
