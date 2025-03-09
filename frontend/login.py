
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

class Ui_StackedWidget(object):
    def setupUi(self, StackedWidget):
        if not StackedWidget.objectName():
            StackedWidget.setObjectName(u"StackedWidget")
        StackedWidget.resize(1104, 623)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.widget = QWidget(self.page)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(150, 160, 144, 145))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit_username = QLineEdit(self.widget)
        self.lineEdit_username.setObjectName(u"lineEdit_username")

        self.verticalLayout.addWidget(self.lineEdit_username)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_password = QLineEdit(self.widget)
        self.lineEdit_password.setObjectName(u"lineEdit_password")

        self.verticalLayout.addWidget(self.lineEdit_password)

        self.button_login = QPushButton(self.widget)
        self.button_login.setObjectName(u"button_login")

        self.verticalLayout.addWidget(self.button_login)

        StackedWidget.addWidget(self.page)

        self.retranslateUi(StackedWidget)

        QMetaObject.connectSlotsByName(StackedWidget)
    # setupUi

    def retranslateUi(self, StackedWidget):
        StackedWidget.setWindowTitle(QCoreApplication.translate("StackedWidget", u"StackedWidget", None))
        self.label.setText(QCoreApplication.translate("StackedWidget", u"Username:", None))
        self.label_2.setText(QCoreApplication.translate("StackedWidget", u"Password:", None))
        self.button_login.setText(QCoreApplication.translate("StackedWidget", u"Login", None))
    # retranslateUi

