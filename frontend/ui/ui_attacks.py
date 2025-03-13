# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'attacks.ui'
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

class Ui_Attacks(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 700)
        self.lineEditURLAttaques = QLineEdit(Form)
        self.lineEditURLAttaques.setObjectName(u"lineEditURLAttaques")
        self.lineEditURLAttaques.setGeometry(QRect(410, 270, 291, 27))
        self.labelURL = QLabel(Form)
        self.labelURL.setObjectName(u"labelURL")
        self.labelURL.setGeometry(QRect(410, 240, 121, 19))
        self.pushButtonURLAttaques = QPushButton(Form)
        self.pushButtonURLAttaques.setObjectName(u"pushButtonURLAttaques")
        self.pushButtonURLAttaques.setGeometry(QRect(510, 320, 88, 27))
        self.pushButtonDeconnexionAttaques = QPushButton(Form)
        self.pushButtonDeconnexionAttaques.setObjectName(u"pushButtonDeconnexionAttaques")
        self.pushButtonDeconnexionAttaques.setGeometry(QRect(110, 620, 111, 27))
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(110, 50, 99, 61))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButtonOnglet2Attaques = QPushButton(self.layoutWidget)
        self.pushButtonOnglet2Attaques.setObjectName(u"pushButtonOnglet2Attaques")

        self.verticalLayout.addWidget(self.pushButtonOnglet2Attaques)

        self.pushButtonOnglet3Attaques = QPushButton(self.layoutWidget)
        self.pushButtonOnglet3Attaques.setObjectName(u"pushButtonOnglet3Attaques")

        self.verticalLayout.addWidget(self.pushButtonOnglet3Attaques)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelURL.setText(QCoreApplication.translate("Form", u"Rentrer l'URL:", None))
        self.pushButtonURLAttaques.setText(QCoreApplication.translate("Form", u"Rechercher", None))
        self.pushButtonDeconnexionAttaques.setText(QCoreApplication.translate("Form", u"D\u00e9connexion", None))
        self.pushButtonOnglet2Attaques.setText(QCoreApplication.translate("Form", u"Rapports", None))
        self.pushButtonOnglet3Attaques.setText(QCoreApplication.translate("Form", u"Cartographie", None))
    # retranslateUi

