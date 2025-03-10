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
        self.gridLayoutWidget = QWidget(Login)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(110, 33, 871, 581))
        self.gridLayoutLogin = QGridLayout(self.gridLayoutWidget)
        self.gridLayoutLogin.setObjectName(u"gridLayoutLogin")
        self.gridLayoutLogin.setContentsMargins(0, 0, 0, 0)
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
        self.labelUsernameLogin = QLabel(self.gridLayoutWidget)
        self.labelUsernameLogin.setObjectName(u"labelUsernameLogin")

        self.verticalLayoutLogin.addWidget(self.labelUsernameLogin)

        self.lineEditUsernameLogin = QLineEdit(self.gridLayoutWidget)
        self.lineEditUsernameLogin.setObjectName(u"lineEditUsernameLogin")

        self.verticalLayoutLogin.addWidget(self.lineEditUsernameLogin)

        self.labelPasswordLogin = QLabel(self.gridLayoutWidget)
        self.labelPasswordLogin.setObjectName(u"labelPasswordLogin")

        self.verticalLayoutLogin.addWidget(self.labelPasswordLogin)

        self.lineEditPasswordLogin = QLineEdit(self.gridLayoutWidget)
        self.lineEditPasswordLogin.setObjectName(u"lineEditPasswordLogin")
        self.lineEditPasswordLogin.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayoutLogin.addWidget(self.lineEditPasswordLogin)

        self.buttonLogin = QPushButton(self.gridLayoutWidget)
        self.buttonLogin.setObjectName(u"buttonLogin")

        self.verticalLayoutLogin.addWidget(self.buttonLogin)


        self.gridLayoutLogin.addLayout(self.verticalLayoutLogin, 1, 1, 1, 1)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Login", None))
        self.labelUsernameLogin.setText(QCoreApplication.translate("Login", u"Username:", None))
        self.labelPasswordLogin.setText(QCoreApplication.translate("Login", u"Password:", None))
        self.buttonLogin.setText(QCoreApplication.translate("Login", u"Login", None))
    # retranslateUi

