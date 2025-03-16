# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rapports.ui'
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

class Ui_Rapports(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 700)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 221, 701))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.pushButtonDeconnexionRapports = QPushButton(self.frame)
        self.pushButtonDeconnexionRapports.setObjectName(u"pushButtonDeconnexionRapports")
        self.pushButtonDeconnexionRapports.setGeometry(QRect(0, 670, 221, 27))
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 10, 221, 130))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButtonOngletAccueilRapports = QPushButton(self.widget)
        self.pushButtonOngletAccueilRapports.setObjectName(u"pushButtonOngletAccueilRapports")

        self.verticalLayout.addWidget(self.pushButtonOngletAccueilRapports)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButtonOnglet1Rapports = QPushButton(self.widget)
        self.pushButtonOnglet1Rapports.setObjectName(u"pushButtonOnglet1Rapports")

        self.verticalLayout_2.addWidget(self.pushButtonOnglet1Rapports)

        self.pushButtonOnglet2Rapports = QPushButton(self.widget)
        self.pushButtonOnglet2Rapports.setObjectName(u"pushButtonOnglet2Rapports")

        self.verticalLayout_2.addWidget(self.pushButtonOnglet2Rapports)

        self.pushButtonOnglet3Rapports = QPushButton(self.widget)
        self.pushButtonOnglet3Rapports.setObjectName(u"pushButtonOnglet3Rapports")

        self.verticalLayout_2.addWidget(self.pushButtonOnglet3Rapports)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.labelRapports = QLabel(Form)
        self.labelRapports.setObjectName(u"labelRapports")
        self.labelRapports.setGeometry(QRect(470, 40, 66, 19))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButtonDeconnexionRapports.setText(QCoreApplication.translate("Form", u"D\u00e9connexion", None))
        self.pushButtonOngletAccueilRapports.setText(QCoreApplication.translate("Form", u"Accueil", None))
        self.pushButtonOnglet1Rapports.setText(QCoreApplication.translate("Form", u"Attaques", None))
        self.pushButtonOnglet2Rapports.setText(QCoreApplication.translate("Form", u"Rapports", None))
        self.pushButtonOnglet3Rapports.setText(QCoreApplication.translate("Form", u"Cartographie", None))
        self.labelRapports.setText(QCoreApplication.translate("Form", u"Rapports", None))
    # retranslateUi

