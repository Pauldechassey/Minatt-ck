# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'documentation.ui'
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

class Ui_Documentation(object):
    def setupUi(self, Documentation):
        if not Documentation.objectName():
            Documentation.setObjectName(u"Documentation")
        Documentation.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Documentation.sizePolicy().hasHeightForWidth())
        Documentation.setSizePolicy(sizePolicy)
        Documentation.setMinimumSize(QSize(1400, 900))
        Documentation.setStyleSheet(u"background-color: #300711;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Documentation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelLogo = QLabel(Documentation)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(65, 42))
        self.labelLogo.setMaximumSize(QSize(65, 42))
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.gridLayout.addWidget(self.labelLogo, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.pushButtonDocumentationDocumentation = QPushButton(Documentation)
        self.pushButtonDocumentationDocumentation.setObjectName(u"pushButtonDocumentationDocumentation")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(12)
        font.setBold(True)
        self.pushButtonDocumentationDocumentation.setFont(font)
        self.pushButtonDocumentationDocumentation.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayout.addWidget(self.pushButtonDocumentationDocumentation, 0, 4, 1, 1)

        self.pushButtonActualiteDocumentation = QPushButton(Documentation)
        self.pushButtonActualiteDocumentation.setObjectName(u"pushButtonActualiteDocumentation")
        self.pushButtonActualiteDocumentation.setFont(font)
        self.pushButtonActualiteDocumentation.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayout.addWidget(self.pushButtonActualiteDocumentation, 0, 3, 1, 1)

        self.pushButtonAccueilDocumentation = QPushButton(Documentation)
        self.pushButtonAccueilDocumentation.setObjectName(u"pushButtonAccueilDocumentation")
        self.pushButtonAccueilDocumentation.setFont(font)
        self.pushButtonAccueilDocumentation.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayout.addWidget(self.pushButtonAccueilDocumentation, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 5, 1, 1)

        self.pushButtonDeconnexionDocumentation = QPushButton(Documentation)
        self.pushButtonDeconnexionDocumentation.setObjectName(u"pushButtonDeconnexionDocumentation")
        self.pushButtonDeconnexionDocumentation.setStyleSheet(u"QPushButton {\n"
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
        self.pushButtonDeconnexionDocumentation.setIcon(icon)
        self.pushButtonDeconnexionDocumentation.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.pushButtonDeconnexionDocumentation, 0, 6, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(Documentation)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1418, 1245))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(13)
        self.label_4.setFont(font1)

        self.verticalLayout.addWidget(self.label_4)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)


        self.retranslateUi(Documentation)

        QMetaObject.connectSlotsByName(Documentation)
    # setupUi

    def retranslateUi(self, Documentation):
        Documentation.setWindowTitle(QCoreApplication.translate("Documentation", u"Documentation", None))
        self.labelLogo.setText("")
        self.pushButtonDocumentationDocumentation.setText(QCoreApplication.translate("Documentation", u"Documentation", None))
        self.pushButtonActualiteDocumentation.setText(QCoreApplication.translate("Documentation", u"Actualit\u00e9", None))
        self.pushButtonAccueilDocumentation.setText(QCoreApplication.translate("Documentation", u"Accueil", None))
        self.pushButtonDeconnexionDocumentation.setText("")
        self.label_4.setText(QCoreApplication.translate("Documentation", u"<h2>Documentation \u2013 Workflow d\u2019Audit</h2>\n"
"\n"
"<p>Notre interface permet de r\u00e9aliser des audits de s\u00e9curit\u00e9 sur des sites web de mani\u00e8re guid\u00e9e et structur\u00e9e. Voici les grandes \u00e9tapes du <br>processus :</p>\n"
"\n"
"<h3>1. Cr\u00e9ation ou s\u00e9lection d\u2019un audit</h3>\n"
"<p>\n"
"  Lors de la premi\u00e8re utilisation, vous pouvez :\n"
"  <ul>\n"
"    <li><strong>Cr\u00e9er un nouvel audit</strong> en renseignant l\u2019URL cible.</li>\n"
"    <li><strong>Reprendre un audit existant</strong> d\u00e9j\u00e0 d\u00e9marr\u00e9, depuis l\u2019interface de s\u00e9lection.</li>\n"
"  </ul>\n"
"</p>\n"
"<p>\n"
"  Chaque audit conserve son avancement sous forme d\u2019un <strong>\u00e9tat num\u00e9rique</strong>, ce qui permet de reprendre le processus \u00e0 n\u2019importe quelle \u00e9tape <br>sans tout recommencer.\n"
"</p>\n"
"\n"
"<h3>2. Lancement de la cartographie</h3>\n"
"<p>\n"
"  Cette \u00e9tape effectue une analyse initiale du site, incluant :\n"
"  <"
                        "ul>\n"
"    <li>La <strong>d\u00e9couverte automatique de pages</strong> accessibles (publiques ou semi-cach\u00e9es).</li>\n"
"    <li>L\u2019identification de ressources ou endpoints utiles pour les phases suivantes.</li>\n"
"  </ul>\n"
"</p>\n"
"<p>Une fois cette \u00e9tape compl\u00e9t\u00e9e avec succ\u00e8s, l\u2019<strong>\u00e9tat de l\u2019audit passe \u00e0 1</strong>.</p>\n"
"\n"
"<h3>3. Lancement des attaques</h3>\n"
"<p>\n"
"  Apr\u00e8s la cartographie, vous pouvez lancer un ou plusieurs types d\u2019attaques automatis\u00e9es :\n"
"  <ul>\n"
"    <li><strong>SQL Injection (SQLi)</strong> : Injection de requ\u00eates malveillantes pour tester la robustesse des bases de donn\u00e9es.</li>\n"
"    <li><strong>Cross-Site Scripting (XSS)</strong> : Injection de scripts c\u00f4t\u00e9 client visant \u00e0 manipuler l'affichage ou voler des donn\u00e9es.</li>\n"
"    <li><strong>Cross-Site Request Forgery (CSRF)</strong> : Simulation de requ\u00eates non autoris\u00e9es pour tester la validation des ac"
                        "tions sensibles.</li>\n"
"    <li><strong>Analyse des headers et cookies</strong> : V\u00e9rification des en-t\u00eates HTTP, cookies et directives de s\u00e9curit\u00e9 (CSP, SameSite, etc.).</li>\n"
"  </ul>\n"
"</p>\n"
"<p>Une fois que les attaques sont ex\u00e9cut\u00e9es, l\u2019<strong>\u00e9tat de l\u2019audit passe \u00e0 2</strong>.</p>\n"
"\n"
"<h3>4. G\u00e9n\u00e9ration du rapport</h3>\n"
"<p>\n"
"  Un rapport est ensuite g\u00e9n\u00e9r\u00e9 automatiquement, synth\u00e9tisant :\n"
"  <ul>\n"
"    <li>Les vuln\u00e9rabilit\u00e9s identifi\u00e9es.</li>\n"
"    <li>Leur criticit\u00e9.</li>\n"
"    <li>Les recommandations associ\u00e9es.</li>\n"
"  </ul>\n"
"</p>\n"
"<p>Une fois cette phase termin\u00e9e, l\u2019<strong>\u00e9tat de l\u2019audit passe \u00e0 3</strong>.</p>\n"
"\n"
"<h3>Gestion de l\u2019\u00e9tat des audits</h3>\n"
"<p>Le syst\u00e8me repose sur une gestion d\u2019\u00e9tat pour permettre de reprendre un audit \u00e0 n\u2019importe quelle \u00e9tape :</p>\n"
"\n"
"<table border=\""
                        "1\" cellspacing=\"0\" cellpadding=\"6\">\n"
"  <thead>\n"
"    <tr>\n"
"      <th>\u00c9tat</th>\n"
"      <th>Signification</th>\n"
"    </tr>\n"
"  </thead>\n"
"  <tbody>\n"
"    <tr>\n"
"      <td>0</td>\n"
"      <td>Audit cr\u00e9\u00e9, aucune action lanc\u00e9e.</td>\n"
"    </tr>\n"
"    <tr>\n"
"      <td>1</td>\n"
"      <td>Cartographie r\u00e9alis\u00e9e.</td>\n"
"    </tr>\n"
"    <tr>\n"
"      <td>2</td>\n"
"      <td>Attaques effectu\u00e9es.</td>\n"
"    </tr>\n"
"    <tr>\n"
"      <td>3</td>\n"
"      <td>Rapport g\u00e9n\u00e9r\u00e9.</td>\n"
"    </tr>\n"
"  </tbody>\n"
"</table>\n"
"\n"
"<p>\n"
"  Il est possible de <strong>s\u2019arr\u00eater \u00e0 une \u00e9tape sans tout faire d\u2019un coup</strong>.<br>\n"
"  Par exemple, si vous vous arr\u00eatez apr\u00e8s la cartographie (<strong>\u00e9tat 1</strong>), vous pourrez <strong>reprendre plus tard l\u2019audit</strong> en allant dans la section <br><em>\u00ab S\u00e9lectionner un audit \u00bb</em>.<br>\n"
" Si l\u2019audit est \u00e0 "
                        "l\u2019\u00e9tat 1, vous serez automatiquement redirig\u00e9 vers la <strong>page de lancement des attaques</strong>, sans repasser par la cartographie.\n"
"</p>\n"
"", None))
    # retranslateUi

