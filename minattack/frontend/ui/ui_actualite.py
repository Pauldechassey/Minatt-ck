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
        Actualite.resize(1416, 938)
        Actualite.setStyleSheet(u"background-color: #121212;\n"
"color: white;")
        self.gridLayout_2 = QGridLayout(Actualite)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButtonActualiteActualite = QPushButton(Actualite)
        self.pushButtonActualiteActualite.setObjectName(u"pushButtonActualiteActualite")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(12)
        font.setBold(True)
        self.pushButtonActualiteActualite.setFont(font)
        self.pushButtonActualiteActualite.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayout.addWidget(self.pushButtonActualiteActualite, 0, 3, 1, 1)

        self.pushButtonDocumentationActualite = QPushButton(Actualite)
        self.pushButtonDocumentationActualite.setObjectName(u"pushButtonDocumentationActualite")
        self.pushButtonDocumentationActualite.setFont(font)
        self.pushButtonDocumentationActualite.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayout.addWidget(self.pushButtonDocumentationActualite, 0, 4, 1, 1)

        self.pushButtonDeconnexionActualite = QPushButton(Actualite)
        self.pushButtonDeconnexionActualite.setObjectName(u"pushButtonDeconnexionActualite")

        self.gridLayout.addWidget(self.pushButtonDeconnexionActualite, 0, 6, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.pushButtonAccueilActualite = QPushButton(Actualite)
        self.pushButtonAccueilActualite.setObjectName(u"pushButtonAccueilActualite")
        self.pushButtonAccueilActualite.setFont(font)
        self.pushButtonAccueilActualite.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayout.addWidget(self.pushButtonAccueilActualite, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 5, 1, 1)

        self.labelLogo_2 = QLabel(Actualite)
        self.labelLogo_2.setObjectName(u"labelLogo_2")
        self.labelLogo_2.setMinimumSize(QSize(65, 42))
        self.labelLogo_2.setMaximumSize(QSize(65, 42))
        self.labelLogo_2.setScaledContents(True)

        self.gridLayout.addWidget(self.labelLogo_2, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(Actualite)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1396, 867))
        self.verticalLayoutWidget = QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 2040, 871))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.retranslateUi(Actualite)

        QMetaObject.connectSlotsByName(Actualite)
    # setupUi

    def retranslateUi(self, Actualite):
        Actualite.setWindowTitle(QCoreApplication.translate("Actualite", u"Form", None))
        self.pushButtonActualiteActualite.setText(QCoreApplication.translate("Actualite", u"Actualit\u00e9", None))
        self.pushButtonDocumentationActualite.setText(QCoreApplication.translate("Actualite", u"Documentation", None))
        self.pushButtonDeconnexionActualite.setText("")
        self.pushButtonAccueilActualite.setText(QCoreApplication.translate("Actualite", u"Accueil", None))
        self.labelLogo_2.setText("")
        self.label.setText(QCoreApplication.translate("Actualite", u"<h1>Actualit\u00e9s Cybers\u00e9curit\u00e9 et MITRE ATTACK \u2013 Juin 2025</h1>\n"
"\n"
"<p>Cette section pr\u00e9sente les derni\u00e8res \u00e9volutions en mati\u00e8re de s\u00e9curit\u00e9 offensive et d\u00e9fensive, en mettant l'accent sur les mises \u00e0 jour du framework MITRE ATTACK, les tendances \u00e9mergentes en mati\u00e8re d'attaques, et les \u00e9v\u00e9nements cl\u00e9s du secteur.</p>\n"
"\n"
"<h2>MITRE ATTACK v17 \u2013 Nouveaut\u00e9s (Avril 2025)</h2>\n"
"<p>En avril 2025, MITRE a publi\u00e9 la version 17.0 de son framework ATTACK, introduisant des changements significatifs :</p>\n"
"\n"
"<ul>\n"
"  <li>\n"
"    <strong>Ajout de la plateforme ESXi</strong> : Une nouvelle matrice d\u00e9di\u00e9e aux hyperviseurs VMware ESXi a \u00e9t\u00e9 int\u00e9gr\u00e9e, refl\u00e9tant l'augmentation des attaques ciblant ces environnements virtualis\u00e9s.\n"
"    <br>\n"
"  </li>\n"
"  <li>\n"
"    <strong>Renforcement des descriptions de mitigations</strong> : Les sections de mitigation ont \u00e9"
                        "t\u00e9 enrichies avec des conseils plus d\u00e9taill\u00e9s et des exemples pratiques pour faciliter leur mise en \u0153uvre.\n"
"    <br>\n"
"  </li>\n"
"  <li>\n"
"    <strong>Renommage de la plateforme \"Network\" en \"Network Devices\"</strong> : Ce changement vise \u00e0 clarifier la port\u00e9e de cette cat\u00e9gorie, en se concentrant sp\u00e9cifiquement sur les dispositifs r\u00e9seau.\n"
"    <br>\n"
"  </li>\n"
"</ul>\n"
"\n"
"<h2>Tendances Cybers\u00e9curit\u00e9 2025 selon MITRE ATTACK</h2>\n"
"<p>Selon les pr\u00e9visions bas\u00e9es sur le framework MITRE ATTACK, plusieurs tendances cl\u00e9s se dessinent pour l'ann\u00e9e 2025 :</p>\n"
"\n"
"<ol>\n"
"  <li>\n"
"    <strong>Attaques Aliment\u00e9es par l'Intelligence Artificielle</strong><br>\n"
"    Les cybercriminels exploitent l'IA pour automatiser des attaques telles que le phishing, l'obfuscation de malwares et l'exploitation de vuln\u00e9rabilit\u00e9s zero-day.\n"
"  </li>\n"
"  <li>\n"
"    <strong>Prolif\u00e9ration du Ransomware-as-a-"
                        "Service (RaaS)</strong><br>\n"
"    Les mod\u00e8les RaaS permettent \u00e0 des acteurs malveillants, m\u00eame peu exp\u00e9riment\u00e9s, de lancer des attaques sophistiqu\u00e9es, ciblant notamment les environnements cloud mal configur\u00e9s.\n"
"  </li>\n"
"  <li>\n"
"    <strong>Augmentation des Attaques sur la Cha\u00eene d'Approvisionnement</strong><br>\n"
"    Les attaquants ciblent de plus en plus les fournisseurs tiers et les prestataires de services pour infiltrer les r\u00e9seaux d'entreprise, exploitant les failles dans la cha\u00eene d'approvisionnement logicielle.\n"
"  </li>\n"
"</ol>\n"
"<h2>\u00c9v\u00e9nements et Conf\u00e9rences</h2>\n"
"<ul>\n"
"  <li>\n"
"    <strong>ATTACKcon 6.0 \u2013 Octobre 2025</strong><br>\n"
"    La conf\u00e9rence annuelle ATTACKcon se tiendra les 14 et 15 octobre 2025 \u00e0 McLean, Virginie. Cet \u00e9v\u00e9nement rassemblera des professionnels de la cybers\u00e9curit\u00e9 pour discuter des derni\u00e8res avanc\u00e9es du framework ATTACK et partager des ret"
                        "ours d'exp\u00e9rience.\n"
"    <br>\n"
"  </li>\n"
"  <li>\n"
"    <strong>Atelier Communautaire EU MITRE ATTACK</strong><br>\n"
"    En mai 2025, un atelier communautaire a \u00e9t\u00e9 organis\u00e9 par EUROCONTROL, r\u00e9unissant des praticiens pour \u00e9changer sur l'utilisation du framework ATTACK dans les domaines de la pr\u00e9vention, de la d\u00e9tection et de la r\u00e9ponse aux incidents.\n"
"    <br>\n"
"  </li>\n"
"</ul>\n"
"\n"
"<h2>Alignement avec le Cyber Resilience Act (CRA)</h2>\n"
"<p>Une \u00e9tude r\u00e9cente a \u00e9valu\u00e9 l'alignement entre les exigences essentielles du CRA de l'Union europ\u00e9enne et les mitigations propos\u00e9es par le framework ATTACK. Les r\u00e9sultats indiquent une bonne correspondance, bien que des \u00e9carts subsistent dans des domaines tels que la coordination des vuln\u00e9rabilit\u00e9s.</p>\n"
"\n"
"", None))
    # retranslateUi

