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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Rapports(object):
    def setupUi(self, Rapports):
        if not Rapports.objectName():
            Rapports.setObjectName(u"Rapports")
        Rapports.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rapports.sizePolicy().hasHeightForWidth())
        Rapports.setSizePolicy(sizePolicy)
        Rapports.setMinimumSize(QSize(1400, 900))
        Rapports.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Rapports)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayoutMenuRapports = QGridLayout()
        self.gridLayoutMenuRapports.setObjectName(u"gridLayoutMenuRapports")
        self.pushButtonDeconnexionRapports = QPushButton(Rapports)
        self.pushButtonDeconnexionRapports.setObjectName(u"pushButtonDeconnexionRapports")
        icon = QIcon()
        icon.addFile(u"../resources/images/deconnexion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionRapports.setIcon(icon)
        self.pushButtonDeconnexionRapports.setIconSize(QSize(32, 32))

        self.gridLayoutMenuRapports.addWidget(self.pushButtonDeconnexionRapports, 0, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuRapports.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.labelLogo = QLabel(Rapports)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(65, 42))
        self.labelLogo.setMaximumSize(QSize(65, 42))
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.gridLayoutMenuRapports.addWidget(self.labelLogo, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuRapports.addItem(self.horizontalSpacer_2, 0, 5, 1, 1)

        self.pushButtonActualiteRapports = QPushButton(Rapports)
        self.pushButtonActualiteRapports.setObjectName(u"pushButtonActualiteRapports")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(12)
        font.setBold(True)
        self.pushButtonActualiteRapports.setFont(font)
        self.pushButtonActualiteRapports.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuRapports.addWidget(self.pushButtonActualiteRapports, 0, 3, 1, 1)

        self.pushButtonDocumentationRapports = QPushButton(Rapports)
        self.pushButtonDocumentationRapports.setObjectName(u"pushButtonDocumentationRapports")
        self.pushButtonDocumentationRapports.setFont(font)
        self.pushButtonDocumentationRapports.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuRapports.addWidget(self.pushButtonDocumentationRapports, 0, 4, 1, 1)

        self.pushButtonAccueilRapports = QPushButton(Rapports)
        self.pushButtonAccueilRapports.setObjectName(u"pushButtonAccueilRapports")
        self.pushButtonAccueilRapports.setFont(font)
        self.pushButtonAccueilRapports.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuRapports.addWidget(self.pushButtonAccueilRapports, 0, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayoutMenuRapports, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.labelNomRapports = QLabel(Rapports)
        self.labelNomRapports.setObjectName(u"labelNomRapports")
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.labelNomRapports.setFont(font1)

        self.gridLayout.addWidget(self.labelNomRapports, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.retranslateUi(Rapports)

        QMetaObject.connectSlotsByName(Rapports)
    # setupUi

    def retranslateUi(self, Rapports):
        Rapports.setWindowTitle(QCoreApplication.translate("Rapports", u"Rapports", None))
        self.pushButtonDeconnexionRapports.setText("")
        self.labelLogo.setText("")
        self.pushButtonActualiteRapports.setText(QCoreApplication.translate("Rapports", u"Actualit\u00e9", None))
        self.pushButtonDocumentationRapports.setText(QCoreApplication.translate("Rapports", u"Documentation", None))
        self.pushButtonAccueilRapports.setText(QCoreApplication.translate("Rapports", u"Accueil", None))
        self.labelNomRapports.setText(QCoreApplication.translate("Rapports", u"Rapports", None))
    # retranslateUi

