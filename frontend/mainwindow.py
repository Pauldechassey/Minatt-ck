import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QStackedWidget
from PySide6.QtCore import Qt


# Login widget
class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout()
        self.label = QLabel("Login")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button = QPushButton("Login")
        self.button.clicked.connect(self.check_credentials)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.username)
        self.main_layout.addWidget(self.password)
        self.main_layout.addWidget(self.button)
        self.setLayout(self.main_layout)

    def check_credentials(self):
        if self.username.text() == "admin" and self.password.text() == "admin":
            parent = self.parentWidget()
            if isinstance(parent, QStackedWidget):
                parent.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")


# Main widget with buttons to switch layouts
class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout()

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        self.button1 = QPushButton("Image Viewer")
        self.button1.clicked.connect(self.show_image_viewer)
        self.button2 = QPushButton("Text Editor")
        self.button2.clicked.connect(self.show_text_editor)

        self.sidebar_layout.addWidget(self.button1)
        self.sidebar_layout.addWidget(self.button2)

        self.main_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.image_viewer = QLabel("Image Viewer", self)
        self.image_viewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_editor = QLabel("Text Editor", self)
        self.text_editor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stacked_widget.addWidget(self.image_viewer)
        self.stacked_widget.addWidget(self.text_editor)

        self.setLayout(self.main_layout)

    def show_image_viewer(self):
        self.stacked_widget.setCurrentIndex(0)
        self.image_viewer.setText("Image Viewer")

    def show_text_editor(self):
        self.stacked_widget.setCurrentIndex(1)
        self.text_editor.setText("Text Editor")


# Main window with buttons to switch layout
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(800, 600)
        self.central_widget = QStackedWidget()  # SUPER IMPORTANT
        self.setCentralWidget(self.central_widget)

        self.login_widget = LoginWidget(self.central_widget)
        self.central_widget.addWidget(self.login_widget)

        self.main_widget = MainWidget(self.central_widget)
        self.central_widget.addWidget(self.main_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
