# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_new.ui'
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
        Login.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        Login.setMinimumSize(QSize(1400, 900))
        Login.setMaximumSize(QSize(1400, 900))
        Login.setStyleSheet(u"background-color: rgb(18, 18, 18);\n"
"color:white")
        self.gridLayout = QGridLayout(Login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayoutLogin_2 = QVBoxLayout()
        self.verticalLayoutLogin_2.setObjectName(u"verticalLayoutLogin_2")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutLogin_2.addItem(self.verticalSpacer_4)

        self.labelUsernameLogin_2 = QLabel(Login)
        self.labelUsernameLogin_2.setObjectName(u"labelUsernameLogin_2")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(14)
        self.labelUsernameLogin_2.setFont(font)

        self.verticalLayoutLogin_2.addWidget(self.labelUsernameLogin_2)

        self.lineEditUsernameLogin_2 = QLineEdit(Login)
        self.lineEditUsernameLogin_2.setObjectName(u"lineEditUsernameLogin_2")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMonoNL Nerd Font"])
        font1.setPointSize(14)
        self.lineEditUsernameLogin_2.setFont(font1)
        self.lineEditUsernameLogin_2.setStyleSheet(u"QLineEdit {\n"
"border: 1px solid #ffffff;\n"
"border-radius: 4px;  \n"
"}")

        self.verticalLayoutLogin_2.addWidget(self.lineEditUsernameLogin_2)

        self.labelPasswordLogin_2 = QLabel(Login)
        self.labelPasswordLogin_2.setObjectName(u"labelPasswordLogin_2")
        self.labelPasswordLogin_2.setFont(font1)

        self.verticalLayoutLogin_2.addWidget(self.labelPasswordLogin_2)

        self.lineEditPasswordLogin_2 = QLineEdit(Login)
        self.lineEditPasswordLogin_2.setObjectName(u"lineEditPasswordLogin_2")
        self.lineEditPasswordLogin_2.setFont(font)
        self.lineEditPasswordLogin_2.setStyleSheet(u"QLineEdit {\n"
"border: 1px solid #ffffff;\n"
"border-radius: 4px;  \n"
"}")
        self.lineEditPasswordLogin_2.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayoutLogin_2.addWidget(self.lineEditPasswordLogin_2)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayoutLogin_2.addItem(self.verticalSpacer_5)

        self.buttonLogin_2 = QPushButton(Login)
        self.buttonLogin_2.setObjectName(u"buttonLogin_2")
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMonoNL Nerd Font"])
        font2.setPointSize(14)
        font2.setBold(True)
        self.buttonLogin_2.setFont(font2)
        self.buttonLogin_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.verticalLayoutLogin_2.addWidget(self.buttonLogin_2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutLogin_2.addItem(self.verticalSpacer_6)


        self.gridLayout.addLayout(self.verticalLayoutLogin_2, 0, 0, 1, 1)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Login", None))
        self.labelUsernameLogin_2.setText(QCoreApplication.translate("Login", u"Username:", None))
        self.labelPasswordLogin_2.setText(QCoreApplication.translate("Login", u"Password:", None))
        self.buttonLogin_2.setText(QCoreApplication.translate("Login", u"Login", None))
    # retranslateUi

