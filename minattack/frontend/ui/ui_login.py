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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        Login.setMinimumSize(QSize(1400, 900))
        Login.setMaximumSize(QSize(16777215, 16777215))
        Login.setStyleSheet(u"background-color: #300711;\n"
"color: white;\n"
"")
        self.gridLayout = QGridLayout(Login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.verticalLayoutLogin = QVBoxLayout()
        self.verticalLayoutLogin.setObjectName(u"verticalLayoutLogin")
        self.verticalLayoutLogin.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutLogin.addItem(self.verticalSpacer_4)

        self.labelUsernameLogin = QLabel(Login)
        self.labelUsernameLogin.setObjectName(u"labelUsernameLogin")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(14)
        self.labelUsernameLogin.setFont(font)

        self.verticalLayoutLogin.addWidget(self.labelUsernameLogin)

        self.lineEditUsernameLogin = QLineEdit(Login)
        self.lineEditUsernameLogin.setObjectName(u"lineEditUsernameLogin")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMonoNL Nerd Font"])
        font1.setPointSize(14)
        self.lineEditUsernameLogin.setFont(font1)
        self.lineEditUsernameLogin.setStyleSheet(u"QLineEdit {\n"
"border: 1px solid #ffffff;\n"
"border-radius: 4px;  \n"
"}")

        self.verticalLayoutLogin.addWidget(self.lineEditUsernameLogin)

        self.labelPasswordLogin = QLabel(Login)
        self.labelPasswordLogin.setObjectName(u"labelPasswordLogin")
        self.labelPasswordLogin.setFont(font1)

        self.verticalLayoutLogin.addWidget(self.labelPasswordLogin)

        self.lineEditPasswordLogin = QLineEdit(Login)
        self.lineEditPasswordLogin.setObjectName(u"lineEditPasswordLogin")
        self.lineEditPasswordLogin.setFont(font)
        self.lineEditPasswordLogin.setStyleSheet(u"QLineEdit {\n"
"border: 1px solid #ffffff;\n"
"border-radius: 4px;  \n"
"}")
        self.lineEditPasswordLogin.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayoutLogin.addWidget(self.lineEditPasswordLogin)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayoutLogin.addItem(self.verticalSpacer_5)

        self.buttonLogin = QPushButton(Login)
        self.buttonLogin.setObjectName(u"buttonLogin")
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMonoNL Nerd Font"])
        font2.setPointSize(14)
        font2.setBold(True)
        self.buttonLogin.setFont(font2)
        self.buttonLogin.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.verticalLayoutLogin.addWidget(self.buttonLogin)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutLogin.addItem(self.verticalSpacer_6)


        self.gridLayout.addLayout(self.verticalLayoutLogin, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Login", None))
        self.labelUsernameLogin.setText(QCoreApplication.translate("Login", u"Username:", None))
        self.labelPasswordLogin.setText(QCoreApplication.translate("Login", u"Password:", None))
        self.buttonLogin.setText(QCoreApplication.translate("Login", u"Login", None))
    # retranslateUi

