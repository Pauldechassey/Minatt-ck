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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_Accueil(object):
    def setupUi(self, Accueil):
        if not Accueil.objectName():
            Accueil.setObjectName(u"Accueil")
        Accueil.resize(1000, 700)
        Accueil.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Accueil)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.menuAccueil = QHBoxLayout()
        self.menuAccueil.setObjectName(u"menuAccueil")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.menuAccueil.addItem(self.horizontalSpacer)

        self.pushButtonHomeAccueil = QPushButton(Accueil)
        self.pushButtonHomeAccueil.setObjectName(u"pushButtonHomeAccueil")
        self.pushButtonHomeAccueil.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.menuAccueil.addWidget(self.pushButtonHomeAccueil)

        self.pushButtonAttaquesAccueil = QPushButton(Accueil)
        self.pushButtonAttaquesAccueil.setObjectName(u"pushButtonAttaquesAccueil")
        self.pushButtonAttaquesAccueil.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.menuAccueil.addWidget(self.pushButtonAttaquesAccueil)

        self.pushButtonRapportsAccueil = QPushButton(Accueil)
        self.pushButtonRapportsAccueil.setObjectName(u"pushButtonRapportsAccueil")
        self.pushButtonRapportsAccueil.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.menuAccueil.addWidget(self.pushButtonRapportsAccueil)

        self.pushButtonCartographieAccueil = QPushButton(Accueil)
        self.pushButtonCartographieAccueil.setObjectName(u"pushButtonCartographieAccueil")
        self.pushButtonCartographieAccueil.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.menuAccueil.addWidget(self.pushButtonCartographieAccueil)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.menuAccueil.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionAccueil = QPushButton(Accueil)
        self.pushButtonDeconnexionAccueil.setObjectName(u"pushButtonDeconnexionAccueil")

        self.menuAccueil.addWidget(self.pushButtonDeconnexionAccueil)


        self.gridLayout_2.addLayout(self.menuAccueil, 0, 0, 1, 1)

        self.labelNomAccueil = QLabel(Accueil)
        self.labelNomAccueil.setObjectName(u"labelNomAccueil")

        self.gridLayout_2.addWidget(self.labelNomAccueil, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)


        self.retranslateUi(Accueil)

        QMetaObject.connectSlotsByName(Accueil)
    # setupUi

    def retranslateUi(self, Accueil):
        Accueil.setWindowTitle(QCoreApplication.translate("Accueil", u"Accueil", None))
        self.pushButtonHomeAccueil.setText(QCoreApplication.translate("Accueil", u"Home", None))
        self.pushButtonAttaquesAccueil.setText(QCoreApplication.translate("Accueil", u"Attaques", None))
        self.pushButtonRapportsAccueil.setText(QCoreApplication.translate("Accueil", u"Rapports", None))
        self.pushButtonCartographieAccueil.setText(QCoreApplication.translate("Accueil", u"Cartographie", None))
        self.pushButtonDeconnexionAccueil.setText("")
        self.labelNomAccueil.setText(QCoreApplication.translate("Accueil", u"MinAtt&ck", None))
    # retranslateUi

