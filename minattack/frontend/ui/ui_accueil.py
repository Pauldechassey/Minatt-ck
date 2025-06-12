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
        Accueil.resize(1404, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Accueil.sizePolicy().hasHeightForWidth())
        Accueil.setSizePolicy(sizePolicy)
        Accueil.setMinimumSize(QSize(1400, 900))
        Accueil.setMaximumSize(QSize(16777215, 16777215))
        Accueil.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Accueil)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        self.infoLayout = QGridLayout()
        self.infoLayout.setObjectName(u"infoLayout")
        self.presentationLabel = QLabel(Accueil)
        self.presentationLabel.setObjectName(u"presentationLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.presentationLabel.sizePolicy().hasHeightForWidth())
        self.presentationLabel.setSizePolicy(sizePolicy1)
        self.presentationLabel.setMinimumSize(QSize(0, 340))
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(14)
        font.setBold(False)
        self.presentationLabel.setFont(font)
        self.presentationLabel.setMargin(30)

        self.infoLayout.addWidget(self.presentationLabel, 3, 1, 1, 1)

        self.labelLogo = QLabel(Accueil)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(380, 242))
        self.labelLogo.setMaximumSize(QSize(350, 242))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.labelLogo.setFont(font1)
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.infoLayout.addWidget(self.labelLogo, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.infoLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)


        self.gridLayout_2.addLayout(self.infoLayout, 3, 0, 1, 1)

        self.menuAccueil = QHBoxLayout()
        self.menuAccueil.setObjectName(u"menuAccueil")
        self.labelLogo_2 = QLabel(Accueil)
        self.labelLogo_2.setObjectName(u"labelLogo_2")
        self.labelLogo_2.setMinimumSize(QSize(65, 42))
        self.labelLogo_2.setMaximumSize(QSize(65, 42))
        self.labelLogo_2.setScaledContents(True)

        self.menuAccueil.addWidget(self.labelLogo_2)

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
"<p><span style=\"color:#FF0000\">\n"
"Vous \u00eates responsable de l'utilisation de cet outil. L\u2019audit d\u2019un site tiers peut <br> contrevenir aux conditions g\u00e9n\u00e9rales d\u2019utilisation de son h\u00e9bergeur. De telles <br>actions peuvent engager votre responsabilit\u00e9 et relever des infractions pr\u00e9vues <br> aux articles 323-1, 323-2, 323-3 et 323-4 du Code p\u00e9nal.</span>\n"
"</p>\n"
"</body>\n"
"</html>", None))
        self.labelLogo.setText("")
        self.labelLogo_2.setText("")
        self.pushButtonAccueilAccueil.setText(QCoreApplication.translate("Accueil", u"Accueil", None))
        self.pushButtonActualiteAccueil.setText(QCoreApplication.translate("Accueil", u"Actualit\u00e9", None))
        self.pushButtonDocumentationAccueil.setText(QCoreApplication.translate("Accueil", u"Documentation", None))
        self.pushButtonDeconnexionAccueil.setText("")
        self.pushButtonCreateAudit.setText(QCoreApplication.translate("Accueil", u"Cr\u00e9er un audit", None))
        self.pushButtonSelectAudit.setText(QCoreApplication.translate("Accueil", u"S\u00e9lectionner un audit", None))
    # retranslateUi

