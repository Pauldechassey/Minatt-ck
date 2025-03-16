# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cartographie.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Cartographie(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 700)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 0, 221, 701))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.pushButtonDeconnexionCartographie = QPushButton(self.frame)
        self.pushButtonDeconnexionCartographie.setObjectName(u"pushButtonDeconnexionCartographie")
        self.pushButtonDeconnexionCartographie.setGeometry(QRect(0, 670, 221, 27))
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 10, 221, 130))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButtonOngletAccueilCartographie = QPushButton(self.widget)
        self.pushButtonOngletAccueilCartographie.setObjectName(u"pushButtonOngletAccueilCartographie")

        self.verticalLayout.addWidget(self.pushButtonOngletAccueilCartographie)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButtonOnglet1Cartographie = QPushButton(self.widget)
        self.pushButtonOnglet1Cartographie.setObjectName(u"pushButtonOnglet1Cartographie")

        self.verticalLayout_2.addWidget(self.pushButtonOnglet1Cartographie)

        self.pushButtonOnglet2Cartographie = QPushButton(self.widget)
        self.pushButtonOnglet2Cartographie.setObjectName(u"pushButtonOnglet2Cartographie")

        self.verticalLayout_2.addWidget(self.pushButtonOnglet2Cartographie)

        self.pushButtonOnglet3Cartographie = QPushButton(self.widget)
        self.pushButtonOnglet3Cartographie.setObjectName(u"pushButtonOnglet3Cartographie")

        self.verticalLayout_2.addWidget(self.pushButtonOnglet3Cartographie)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(460, 40, 121, 19))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButtonDeconnexionCartographie.setText(QCoreApplication.translate("Form", u"D\u00e9connexion", None))
        self.pushButtonOngletAccueilCartographie.setText(QCoreApplication.translate("Form", u"Accueil", None))
        self.pushButtonOnglet1Cartographie.setText(QCoreApplication.translate("Form", u"Attaques", None))
        self.pushButtonOnglet2Cartographie.setText(QCoreApplication.translate("Form", u"Rapports", None))
        self.pushButtonOnglet3Cartographie.setText(QCoreApplication.translate("Form", u"Cartographie", None))
        self.label.setText(QCoreApplication.translate("Form", u"Cartographie", None))
    # retranslateUi

