# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(1000, 700)
        self.layoutWidget = QWidget(Login)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(320, 270, 381, 191))
        self.verticalLayoutLogin = QVBoxLayout(self.layoutWidget)
        self.verticalLayoutLogin.setObjectName(u"verticalLayoutLogin")
        self.verticalLayoutLogin.setContentsMargins(0, 0, 0, 0)
        self.labelUsernameLogin = QLabel(self.layoutWidget)
        self.labelUsernameLogin.setObjectName(u"labelUsernameLogin")

        self.verticalLayoutLogin.addWidget(self.labelUsernameLogin)

        self.lineEdit_username_2 = QLineEdit(self.layoutWidget)
        self.lineEdit_username_2.setObjectName(u"lineEdit_username_2")

        self.verticalLayoutLogin.addWidget(self.lineEdit_username_2)

        self.labelPasswordLogin = QLabel(self.layoutWidget)
        self.labelPasswordLogin.setObjectName(u"labelPasswordLogin")

        self.verticalLayoutLogin.addWidget(self.labelPasswordLogin)

        self.lineEditPasswordLogin = QLineEdit(self.layoutWidget)
        self.lineEditPasswordLogin.setObjectName(u"lineEditPasswordLogin")

        self.verticalLayoutLogin.addWidget(self.lineEditPasswordLogin)

        self.buttonLogin = QPushButton(self.layoutWidget)
        self.buttonLogin.setObjectName(u"buttonLogin")

        self.verticalLayoutLogin.addWidget(self.buttonLogin)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Login", None))
        self.labelUsernameLogin.setText(QCoreApplication.translate("Login", u"Username:", None))
        self.labelPasswordLogin.setText(QCoreApplication.translate("Login", u"Password:", None))
        self.buttonLogin.setText(QCoreApplication.translate("Login", u"Login", None))
    # retranslateUi

