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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Cartographie(object):
    def setupUi(self, Cartographie):
        if not Cartographie.objectName():
            Cartographie.setObjectName(u"Cartographie")
        Cartographie.resize(1000, 700)
        Cartographie.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_4 = QGridLayout(Cartographie)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayoutMenuCartographie = QGridLayout()
        self.gridLayoutMenuCartographie.setObjectName(u"gridLayoutMenuCartographie")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuCartographie.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButtonAttaquesCartographie = QPushButton(Cartographie)
        self.pushButtonAttaquesCartographie.setObjectName(u"pushButtonAttaquesCartographie")
        self.pushButtonAttaquesCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonAttaquesCartographie, 0, 1, 1, 1)

        self.pushButtonDeconnexionCartographie = QPushButton(Cartographie)
        self.pushButtonDeconnexionCartographie.setObjectName(u"pushButtonDeconnexionCartographie")
        self.pushButtonDeconnexionCartographie.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        icon = QIcon()
        icon.addFile(u"../../../../Downloads/image.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionCartographie.setIcon(icon)
        self.pushButtonDeconnexionCartographie.setIconSize(QSize(32, 32))

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonDeconnexionCartographie, 0, 6, 1, 1)

        self.pushButtonHomeCartographie = QPushButton(Cartographie)
        self.pushButtonHomeCartographie.setObjectName(u"pushButtonHomeCartographie")
        self.pushButtonHomeCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonHomeCartographie, 0, 2, 1, 1)

        self.pushButtonRapportsCartographie = QPushButton(Cartographie)
        self.pushButtonRapportsCartographie.setObjectName(u"pushButtonRapportsCartographie")
        self.pushButtonRapportsCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonRapportsCartographie, 0, 3, 1, 1)

        self.pushButtonCartographieCartographie = QPushButton(Cartographie)
        self.pushButtonCartographieCartographie.setObjectName(u"pushButtonCartographieCartographie")
        self.pushButtonCartographieCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonCartographieCartographie, 0, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuCartographie.addItem(self.horizontalSpacer_2, 0, 5, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutMenuCartographie, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.retranslateUi(Cartographie)

        QMetaObject.connectSlotsByName(Cartographie)
    # setupUi

    def retranslateUi(self, Cartographie):
        Cartographie.setWindowTitle(QCoreApplication.translate("Cartographie", u"Cartographie", None))
        self.pushButtonAttaquesCartographie.setText(QCoreApplication.translate("Cartographie", u"Attaques", None))
        self.pushButtonDeconnexionCartographie.setText("")
        self.pushButtonHomeCartographie.setText(QCoreApplication.translate("Cartographie", u"Home", None))
        self.pushButtonRapportsCartographie.setText(QCoreApplication.translate("Cartographie", u"Rapports", None))
        self.pushButtonCartographieCartographie.setText(QCoreApplication.translate("Cartographie", u"Cartographie", None))
    # retranslateUi

