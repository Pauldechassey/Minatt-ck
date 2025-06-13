# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'actualite.ui'
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
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Actualite(object):
    def setupUi(self, Actualite):
        if not Actualite.objectName():
            Actualite.setObjectName(u"Actualite")
        Actualite.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Actualite.sizePolicy().hasHeightForWidth())
        Actualite.setSizePolicy(sizePolicy)
        Actualite.setMinimumSize(QSize(1400, 900))
        Actualite.setStyleSheet(u"background-color: #300711;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Actualite)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButtonDocumentationActualite = QPushButton(Actualite)
        self.pushButtonDocumentationActualite.setObjectName(u"pushButtonDocumentationActualite")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(12)
        font.setBold(True)
        self.pushButtonDocumentationActualite.setFont(font)
        self.pushButtonDocumentationActualite.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayout.addWidget(self.pushButtonDocumentationActualite, 0, 4, 1, 1)

        self.pushButtonActualiteActualite = QPushButton(Actualite)
        self.pushButtonActualiteActualite.setObjectName(u"pushButtonActualiteActualite")
        self.pushButtonActualiteActualite.setFont(font)
        self.pushButtonActualiteActualite.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayout.addWidget(self.pushButtonActualiteActualite, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 5, 1, 1)

        self.pushButtonAccueilActualite = QPushButton(Actualite)
        self.pushButtonAccueilActualite.setObjectName(u"pushButtonAccueilActualite")
        self.pushButtonAccueilActualite.setFont(font)
        self.pushButtonAccueilActualite.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayout.addWidget(self.pushButtonAccueilActualite, 0, 2, 1, 1)

        self.labelLogo_2 = QLabel(Actualite)
        self.labelLogo_2.setObjectName(u"labelLogo_2")
        self.labelLogo_2.setMinimumSize(QSize(65, 42))
        self.labelLogo_2.setMaximumSize(QSize(65, 42))
        self.labelLogo_2.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo_2.setScaledContents(True)

        self.gridLayout.addWidget(self.labelLogo_2, 0, 0, 1, 1)

        self.pushButtonDeconnexionActualite = QPushButton(Actualite)
        self.pushButtonDeconnexionActualite.setObjectName(u"pushButtonDeconnexionActualite")
        self.pushButtonDeconnexionActualite.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 3px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")
        icon = QIcon()
        icon.addFile(u"../resources/images/deconnexion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionActualite.setIcon(icon)
        self.pushButtonDeconnexionActualite.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.pushButtonDeconnexionActualite, 0, 6, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(Actualite)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollBar::handle:vertical {\n"
"	background-color: #76061C; \n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"	background-color: #76061C; \n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1530, 991))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(13)
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.retranslateUi(Actualite)

        QMetaObject.connectSlotsByName(Actualite)
    # setupUi

    def retranslateUi(self, Actualite):
        Actualite.setWindowTitle(QCoreApplication.translate("Actualite", u"Actualit\u00e9", None))
        self.pushButtonDocumentationActualite.setText(QCoreApplication.translate("Actualite", u"Documentation", None))
        self.pushButtonActualiteActualite.setText(QCoreApplication.translate("Actualite", u"Actualit\u00e9", None))
        self.pushButtonAccueilActualite.setText(QCoreApplication.translate("Actualite", u"Accueil", None))
        self.labelLogo_2.setText("")
        self.pushButtonDeconnexionActualite.setText("")
        self.label.setText(QCoreApplication.translate("Actualite", u"<html>\n"
"  <head />\n"
"  <body>\n"
"    <h1 style=\"margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"      <span style=\"font-size:xx-large; font-weight:700;\">Actualit\u00e9s Cybers\u00e9curit\u00e9 et MITRE ATTACK \u2013 Juin 2025</span>\n"
"    </h1>\n"
"\n"
"    <p>\n"
"      Cette section pr\u00e9sente les derni\u00e8res \u00e9volutions en mati\u00e8re de s\u00e9curit\u00e9 offensive et d\u00e9fensive, en mettant l'accent sur les mises \u00e0 jour du framework <br />\n"
"      MITRE ATTACK, les tendances \u00e9mergentes en mati\u00e8re d'attaques, et les \u00e9v\u00e9nements cl\u00e9s du secteur.\n"
"    </p>\n"
"\n"
"    <h2 style=\"margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"      <span style=\"font-size:x-large; font-weight:700;\">MITRE ATTACK v17 \u2013 Nouveaut\u00e9s (Avril 2025)</span>\n"
"    </h2>\n"
"\n"
"    <p>En avril 2025, MITRE a publi\u00e9 la versio"
                        "n 17.0 de son framework ATTACK, introduisant des changements significatifs :</p>\n"
"    <ul style=\"margin: 0; -qt-list-indent: 1;\">\n"
"      <li style=\"margin:12px 0 0 0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\"font-weight:700;\">Ajout de la plateforme ESXi</span> :\n"
"        Une nouvelle matrice d\u00e9di\u00e9e aux hyperviseurs VMware ESXi a \u00e9t\u00e9 int\u00e9gr\u00e9e, refl\u00e9tant l'augmentation des attaques <br />\n"
"        ciblant ces environnements virtualis\u00e9s.\n"
"      </li>\n"
"      <li style=\"margin:0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\"font-weight:700;\">Renforcement des descriptions de mitigations</span> :\n"
"        Les sections de mitigation ont \u00e9t\u00e9 enrichies avec des conseils plus d\u00e9taill\u00e9s et des exemples <br />\n"
"        pratiques pour faciliter leur mise en \u0153uvre.\n"
"      </li>\n"
"      <li style=\"margin:0 0 12px 0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\""
                        "font-weight:700;\">Renommage de la plateforme \"Network\" en \"Network Devices\"</span> :\n"
"        Ce changement vise \u00e0 clarifier la port\u00e9e de cette cat\u00e9gorie, en se concentrant <br />\n"
"        sp\u00e9cifiquement sur les dispositifs r\u00e9seau.\n"
"      </li>\n"
"    </ul>\n"
"\n"
"    <h2 style=\"margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"      <span style=\"font-size:x-large; font-weight:700;\">Tendances Cybers\u00e9curit\u00e9 2025 selon MITRE ATTACK</span>\n"
"    </h2>\n"
"\n"
"    <p>Selon les pr\u00e9visions bas\u00e9es sur le framework MITRE ATTACK, plusieurs tendances cl\u00e9s se dessinent pour l'ann\u00e9e 2025 :</p>\n"
"    <ol style=\"margin: 0; -qt-list-indent: 1;\">\n"
"      <li style=\"margin:12px 0 0 0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\"font-weight:700;\">Attaques Aliment\u00e9es par l'Intelligence Artificielle</span><br />\n"
"        Les cybercriminels exploitent "
                        "l'IA pour automatiser des attaques telles que le phishing, l'obfuscation de malwares et l'exploitation de <br />\n"
"        vuln\u00e9rabilit\u00e9s zero-day.\n"
"      </li>\n"
"      <li style=\"margin:0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\"font-weight:700;\">Prolif\u00e9ration du Ransomware-as-a-Service (RaaS)</span><br />\n"
"        Les mod\u00e8les RaaS permettent \u00e0 des acteurs malveillants, m\u00eame peu exp\u00e9riment\u00e9s, de lancer des attaques sophistiqu\u00e9es, ciblant notamment les <br />\n"
"        environnements cloud mal configur\u00e9s.\n"
"      </li>\n"
"      <li style=\"margin:0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\"font-weight:700;\">Augmentation des Attaques sur la Cha\u00eene d'Approvisionnement</span><br />\n"
"        Les attaquants ciblent de plus en plus les fournisseurs tiers et les prestataires de services pour infiltrer les r\u00e9seaux d'entreprise, exploitant <br>les failles dans la cha\u00eene d'approvisionn"
                        "ement logicielle.\n"
"      </li>\n"
"    </ol>\n"
"    <p></p>\n"
"\n"
"    <h2 style=\"margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"      <span style=\"font-size:x-large; font-weight:700;\">\u00c9v\u00e9nements et Conf\u00e9rences</span>\n"
"    </h2>\n"
"\n"
"    <ul style=\"margin: 0; -qt-list-indent: 1;\">\n"
"      <li style=\"margin:12px 0 0 0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\"font-weight:700;\">ATTACKcon 6.0 \u2013 Octobre 2025</span><br />\n"
"        La conf\u00e9rence annuelle ATTACKcon se tiendra les 14 et 15 octobre 2025 \u00e0 McLean, Virginie. Cet \u00e9v\u00e9nement rassemblera des professionnels de la <br>cybers\u00e9curit\u00e9 pour discuter des derni\u00e8res avanc\u00e9es du framework ATTACK et partager des retours d'exp\u00e9rience.\n"
"      </li>\n"
"      <li style=\"margin:0 0 12px 0; -qt-block-indent:0; text-indent:0px;\">\n"
"        <span style=\"font-weight:700;\">Atelier Communa"
                        "utaire EU MITRE ATTACK</span><br />\n"
"        En mai 2025, un atelier communautaire a \u00e9t\u00e9 organis\u00e9 par EUROCONTROL, r\u00e9unissant des praticiens pour \u00e9changer sur l'utilisation du framework <br>ATTACK dans les domaines de la pr\u00e9vention, de la d\u00e9tection et de la r\u00e9ponse aux incidents.\n"
"      </li>\n"
"    </ul>\n"
"\n"
"    <h2 style=\"margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\n"
"      <span style=\"font-size:x-large; font-weight:700;\">Alignement avec le Cyber Resilience Act (CRA)</span>\n"
"    </h2>\n"
"\n"
"    <p>\n"
"      Une \u00e9tude r\u00e9cente a \u00e9valu\u00e9 l'alignement entre les exigences essentielles du CRA de l'Union europ\u00e9enne et les mitigations propos\u00e9es par le framework <br>ATTACK. Les r\u00e9sultats indiquent une bonne correspondance, bien que des \u00e9carts subsistent dans des domaines tels que la coordination des <br>vuln\u00e9rabilit\u00e9s.\n"
"    </p>\n"
"  <"
                        "/body>\n"
"</html>", None))
    # retranslateUi

