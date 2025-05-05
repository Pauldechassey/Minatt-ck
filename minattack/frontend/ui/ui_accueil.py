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
        Accueil.resize(1400, 900)
        Accueil.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Accueil)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        self.infoLayout = QGridLayout()
        self.infoLayout.setObjectName(u"infoLayout")
        self.labelLogo = QLabel(Accueil)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(380, 242))
        self.labelLogo.setMaximumSize(QSize(350, 242))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.labelLogo.setFont(font)
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.infoLayout.addWidget(self.labelLogo, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.infoLayout.addItem(self.verticalSpacer, 1, 1, 1, 1)

        self.presentationLabel = QLabel(Accueil)
        self.presentationLabel.setObjectName(u"presentationLabel")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(14)
        font1.setBold(False)
        self.presentationLabel.setFont(font1)
        self.presentationLabel.setMargin(30)

        self.infoLayout.addWidget(self.presentationLabel, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.infoLayout, 3, 0, 1, 1)

        self.menuAccueil = QHBoxLayout()
        self.menuAccueil.setObjectName(u"menuAccueil")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.menuAccueil.addItem(self.horizontalSpacer)

        self.pushButtonAccueilAccueil = QPushButton(Accueil)
        self.pushButtonAccueilAccueil.setObjectName(u"pushButtonAccueilAccueil")
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMono Nerd Font"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.pushButtonAccueilAccueil.setFont(font2)
        self.pushButtonAccueilAccueil.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.menuAccueil.addWidget(self.pushButtonAccueilAccueil)

        self.pushButtonActualiteAccueil = QPushButton(Accueil)
        self.pushButtonActualiteAccueil.setObjectName(u"pushButtonActualiteAccueil")
        self.pushButtonActualiteAccueil.setFont(font2)
        self.pushButtonActualiteAccueil.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.menuAccueil.addWidget(self.pushButtonActualiteAccueil)

        self.pushButtonDocumentationAccueil = QPushButton(Accueil)
        self.pushButtonDocumentationAccueil.setObjectName(u"pushButtonDocumentationAccueil")
        self.pushButtonDocumentationAccueil.setFont(font2)
        self.pushButtonDocumentationAccueil.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.menuAccueil.addWidget(self.pushButtonDocumentationAccueil)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.menuAccueil.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionAccueil = QPushButton(Accueil)
        self.pushButtonDeconnexionAccueil.setObjectName(u"pushButtonDeconnexionAccueil")
        icon = QIcon()
        icon.addFile(u"../resources/images/deconnexion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionAccueil.setIcon(icon)
        self.pushButtonDeconnexionAccueil.setIconSize(QSize(32, 32))

        self.menuAccueil.addWidget(self.pushButtonDeconnexionAccueil)


        self.gridLayout_2.addLayout(self.menuAccueil, 1, 0, 1, 1)

        self.auditSelectLayout = QVBoxLayout()
        self.auditSelectLayout.setObjectName(u"auditSelectLayout")
        self.auditSelectLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalSpacer_3 = QSpacerItem(20, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.auditSelectLayout.addItem(self.verticalSpacer_3)

        self.pushButtonCreateAudit = QPushButton(Accueil)
        self.pushButtonCreateAudit.setObjectName(u"pushButtonCreateAudit")
        font3 = QFont()
        font3.setFamilies([u"JetBrainsMono Nerd Font"])
        font3.setPointSize(14)
        font3.setBold(True)
        self.pushButtonCreateAudit.setFont(font3)
        self.pushButtonCreateAudit.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.auditSelectLayout.addWidget(self.pushButtonCreateAudit)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.auditSelectLayout.addItem(self.verticalSpacer_4)

        self.pushButtonSelectAudit = QPushButton(Accueil)
        self.pushButtonSelectAudit.setObjectName(u"pushButtonSelectAudit")
        self.pushButtonSelectAudit.setFont(font3)
        self.pushButtonSelectAudit.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.auditSelectLayout.addWidget(self.pushButtonSelectAudit)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.auditSelectLayout.addItem(self.verticalSpacer_5)


        self.gridLayout_2.addLayout(self.auditSelectLayout, 4, 0, 1, 1)


        self.retranslateUi(Accueil)

        QMetaObject.connectSlotsByName(Accueil)
    # setupUi

    def retranslateUi(self, Accueil):
        Accueil.setWindowTitle(QCoreApplication.translate("Accueil", u"Accueil", None))
        self.labelLogo.setText("")
        self.presentationLabel.setText(QCoreApplication.translate("Accueil", u"<html>\n"
"<body>\n"
"<span style=\"font-weight: bold; font-size:20pt;\">\n"
"<p>\n"
"Bienvenue sur <span style=\"color:#00FFAA;\">Minattack</span>\n"
"</p>\n"
"</span>\n"
"<p>\n"
"Auditer votre site web !\n"
"  <ul>\n"
"    <li>Lancer des attaques cibl\u00e9es (SQLi, CSRF...)</li>\n"
"    <li>G\u00e9n\u00e9rer des rapports d\u00e9taill\u00e9s</li>\n"
"    <li>Visualiser la cartographie des ressources</li>\n"
"  </ul>\n"
"</p>\n"
"</body>\n"
"</html>", None))
        self.pushButtonAccueilAccueil.setText(QCoreApplication.translate("Accueil", u"Accueil", None))
        self.pushButtonActualiteAccueil.setText(QCoreApplication.translate("Accueil", u"Actualit\u00e9", None))
        self.pushButtonDocumentationAccueil.setText(QCoreApplication.translate("Accueil", u"Documentation", None))
        self.pushButtonDeconnexionAccueil.setText("")
        self.pushButtonCreateAudit.setText(QCoreApplication.translate("Accueil", u"Cr\u00e9er un audit", None))
        self.pushButtonSelectAudit.setText(QCoreApplication.translate("Accueil", u"S\u00e9lectionner un audit", None))
    # retranslateUi

