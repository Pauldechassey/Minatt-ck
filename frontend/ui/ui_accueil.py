# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'accueil.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Accueil(object):
    def setupUi(self, Accueil):
        if not Accueil.objectName():
            Accueil.setObjectName(u"Accueil")
        Accueil.resize(1000, 700)
        self.labelNomAccueil = QLabel(Accueil)
        self.labelNomAccueil.setObjectName(u"labelNomAccueil")
        self.labelNomAccueil.setGeometry(QRect(440, 20, 81, 71))
        self.pushButtonDeconnexionAccueil = QPushButton(Accueil)
        self.pushButtonDeconnexionAccueil.setObjectName(u"pushButtonDeconnexionAccueil")
        self.pushButtonDeconnexionAccueil.setGeometry(QRect(30, 650, 111, 27))
        self.widget = QWidget(Accueil)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(50, 40, 99, 95))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButtonOnglet1Accueil = QPushButton(self.widget)
        self.pushButtonOnglet1Accueil.setObjectName(u"pushButtonOnglet1Accueil")

        self.verticalLayout.addWidget(self.pushButtonOnglet1Accueil)

        self.pushButtonOnglet2Accueil = QPushButton(self.widget)
        self.pushButtonOnglet2Accueil.setObjectName(u"pushButtonOnglet2Accueil")

        self.verticalLayout.addWidget(self.pushButtonOnglet2Accueil)

        self.pushButtonOnglet3Accueil = QPushButton(self.widget)
        self.pushButtonOnglet3Accueil.setObjectName(u"pushButtonOnglet3Accueil")

        self.verticalLayout.addWidget(self.pushButtonOnglet3Accueil)


        self.retranslateUi(Accueil)

        QMetaObject.connectSlotsByName(Accueil)
    # setupUi

    def retranslateUi(self, Accueil):
        Accueil.setWindowTitle(QCoreApplication.translate("Accueil", u"Accueil", None))
        self.labelNomAccueil.setText(QCoreApplication.translate("Accueil", u"MinAtt&ck", None))
        self.pushButtonDeconnexionAccueil.setText(QCoreApplication.translate("Accueil", u"D\u00e9connexion", None))
        self.pushButtonOnglet1Accueil.setText(QCoreApplication.translate("Accueil", u"Attaques", None))
        self.pushButtonOnglet2Accueil.setText(QCoreApplication.translate("Accueil", u"Rapports", None))
        self.pushButtonOnglet3Accueil.setText(QCoreApplication.translate("Accueil", u"Cartographie", None))
    # retranslateUi

