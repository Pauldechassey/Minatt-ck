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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Accueil(object):
    def setupUi(self, Accueil):
        if not Accueil.objectName():
            Accueil.setObjectName(u"Accueil")
        Accueil.resize(1367, 682)
        Accueil.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.verticalLayout = QVBoxLayout(Accueil)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonHomeAccueil = QPushButton(Accueil)
        self.pushButtonHomeAccueil.setObjectName(u"pushButtonHomeAccueil")

        self.horizontalLayout.addWidget(self.pushButtonHomeAccueil)

        self.pushButtonAttaquesAccueil = QPushButton(Accueil)
        self.pushButtonAttaquesAccueil.setObjectName(u"pushButtonAttaquesAccueil")

        self.horizontalLayout.addWidget(self.pushButtonAttaquesAccueil)

        self.pushButtonRapportsAccueil = QPushButton(Accueil)
        self.pushButtonRapportsAccueil.setObjectName(u"pushButtonRapportsAccueil")

        self.horizontalLayout.addWidget(self.pushButtonRapportsAccueil)

        self.pushButtonCartographieAccueil = QPushButton(Accueil)
        self.pushButtonCartographieAccueil.setObjectName(u"pushButtonCartographieAccueil")

        self.horizontalLayout.addWidget(self.pushButtonCartographieAccueil)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionAccueil = QPushButton(Accueil)
        self.pushButtonDeconnexionAccueil.setObjectName(u"pushButtonDeconnexionAccueil")

        self.horizontalLayout.addWidget(self.pushButtonDeconnexionAccueil)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelNomAccueil = QLabel(Accueil)
        self.labelNomAccueil.setObjectName(u"labelNomAccueil")

        self.verticalLayout.addWidget(self.labelNomAccueil)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


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

