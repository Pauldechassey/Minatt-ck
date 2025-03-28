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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Rapports(object):
    def setupUi(self, Rapports):
        if not Rapports.objectName():
            Rapports.setObjectName(u"Rapports")
        Rapports.resize(1000, 700)
        Rapports.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Rapports)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayoutMenuRapports = QGridLayout()
        self.gridLayoutMenuRapports.setObjectName(u"gridLayoutMenuRapports")
        self.pushButtonHomeRapports = QPushButton(Rapports)
        self.pushButtonHomeRapports.setObjectName(u"pushButtonHomeRapports")
        self.pushButtonHomeRapports.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuRapports.addWidget(self.pushButtonHomeRapports, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuRapports.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButtonCartographieRapports = QPushButton(Rapports)
        self.pushButtonCartographieRapports.setObjectName(u"pushButtonCartographieRapports")
        self.pushButtonCartographieRapports.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuRapports.addWidget(self.pushButtonCartographieRapports, 0, 4, 1, 1)

        self.pushButton = QPushButton(Rapports)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayoutMenuRapports.addWidget(self.pushButton, 0, 6, 1, 1)

        self.pushButtonAttaquesRapports = QPushButton(Rapports)
        self.pushButtonAttaquesRapports.setObjectName(u"pushButtonAttaquesRapports")
        self.pushButtonAttaquesRapports.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuRapports.addWidget(self.pushButtonAttaquesRapports, 0, 2, 1, 1)

        self.pushButtonRapportsRapports = QPushButton(Rapports)
        self.pushButtonRapportsRapports.setObjectName(u"pushButtonRapportsRapports")
        self.pushButtonRapportsRapports.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuRapports.addWidget(self.pushButtonRapportsRapports, 0, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuRapports.addItem(self.horizontalSpacer_2, 0, 5, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayoutMenuRapports, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.retranslateUi(Rapports)

        QMetaObject.connectSlotsByName(Rapports)
    # setupUi

    def retranslateUi(self, Rapports):
        Rapports.setWindowTitle(QCoreApplication.translate("Rapports", u"Rapports", None))
        self.pushButtonHomeRapports.setText(QCoreApplication.translate("Rapports", u"Home", None))
        self.pushButtonCartographieRapports.setText(QCoreApplication.translate("Rapports", u"Cartographie", None))
        self.pushButton.setText("")
        self.pushButtonAttaquesRapports.setText(QCoreApplication.translate("Rapports", u"Attaques", None))
        self.pushButtonRapportsRapports.setText(QCoreApplication.translate("Rapports", u"Rapports", None))
    # retranslateUi

