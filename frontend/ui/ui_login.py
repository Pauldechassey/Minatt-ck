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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(1000, 700)
        self.gridLayout = QGridLayout(Login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayoutLogin = QGridLayout()
        self.gridLayoutLogin.setObjectName(u"gridLayoutLogin")
        self.verticalSpacerTopLogin = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayoutLogin.addItem(self.verticalSpacerTopLogin, 0, 1, 1, 1)

        self.horizontalSpacerLeftLogin = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutLogin.addItem(self.horizontalSpacerLeftLogin, 1, 0, 1, 1)

        self.horizontalSpacerRightLogin = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutLogin.addItem(self.horizontalSpacerRightLogin, 1, 2, 1, 1)

        self.verticalSpacerBottomLogin = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayoutLogin.addItem(self.verticalSpacerBottomLogin, 2, 1, 1, 1)

        self.verticalLayoutLogin = QVBoxLayout()
        self.verticalLayoutLogin.setObjectName(u"verticalLayoutLogin")
        self.labelUsernameLogin = QLabel(Login)
        self.labelUsernameLogin.setObjectName(u"labelUsernameLogin")

        self.verticalLayoutLogin.addWidget(self.labelUsernameLogin)

        self.lineEditUsernameLogin = QLineEdit(Login)
        self.lineEditUsernameLogin.setObjectName(u"lineEditUsernameLogin")

        self.verticalLayoutLogin.addWidget(self.lineEditUsernameLogin)

        self.labelPasswordLogin = QLabel(Login)
        self.labelPasswordLogin.setObjectName(u"labelPasswordLogin")

        self.verticalLayoutLogin.addWidget(self.labelPasswordLogin)

        self.lineEditPasswordLogin = QLineEdit(Login)
        self.lineEditPasswordLogin.setObjectName(u"lineEditPasswordLogin")
        self.lineEditPasswordLogin.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayoutLogin.addWidget(self.lineEditPasswordLogin)

        self.buttonLogin = QPushButton(Login)
        self.buttonLogin.setObjectName(u"buttonLogin")

        self.verticalLayoutLogin.addWidget(self.buttonLogin)


        self.gridLayoutLogin.addLayout(self.verticalLayoutLogin, 1, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayoutLogin, 0, 0, 1, 1)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Login", None))
        self.labelUsernameLogin.setText(QCoreApplication.translate("Login", u"Username:", None))
        self.labelPasswordLogin.setText(QCoreApplication.translate("Login", u"Password:", None))
        self.buttonLogin.setText(QCoreApplication.translate("Login", u"Login", None))
    # retranslateUi

