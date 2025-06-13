# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'attaques.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Attaques(object):
    def setupUi(self, Attaques):
        if not Attaques.objectName():
            Attaques.setObjectName(u"Attaques")
        Attaques.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Attaques.sizePolicy().hasHeightForWidth())
        Attaques.setSizePolicy(sizePolicy)
        Attaques.setMinimumSize(QSize(1400, 900))
        Attaques.setStyleSheet(u"background-color: #300711;\n"
"color: white;\n"
"")
        self.gridLayout = QGridLayout(Attaques)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayoutMenuAttaques = QHBoxLayout()
        self.gridLayoutMenuAttaques.setObjectName(u"gridLayoutMenuAttaques")
        self.labelLogo = QLabel(Attaques)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(65, 42))
        self.labelLogo.setMaximumSize(QSize(65, 42))
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.gridLayoutMenuAttaques.addWidget(self.labelLogo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAttaques.addItem(self.horizontalSpacer)

        self.pushButtonAccueilAttaques = QPushButton(Attaques)
        self.pushButtonAccueilAttaques.setObjectName(u"pushButtonAccueilAttaques")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(12)
        font.setBold(True)
        self.pushButtonAccueilAttaques.setFont(font)
        self.pushButtonAccueilAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonAccueilAttaques)

        self.pushButtonActualiteAttaques = QPushButton(Attaques)
        self.pushButtonActualiteAttaques.setObjectName(u"pushButtonActualiteAttaques")
        self.pushButtonActualiteAttaques.setFont(font)
        self.pushButtonActualiteAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonActualiteAttaques)

        self.pushButtonDocumentationAttaques = QPushButton(Attaques)
        self.pushButtonDocumentationAttaques.setObjectName(u"pushButtonDocumentationAttaques")
        self.pushButtonDocumentationAttaques.setFont(font)
        self.pushButtonDocumentationAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonDocumentationAttaques)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAttaques.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionAttaques = QPushButton(Attaques)
        self.pushButtonDeconnexionAttaques.setObjectName(u"pushButtonDeconnexionAttaques")
        self.pushButtonDeconnexionAttaques.setStyleSheet(u"QPushButton {\n"
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
        self.pushButtonDeconnexionAttaques.setIcon(icon)
        self.pushButtonDeconnexionAttaques.setIconSize(QSize(32, 32))

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonDeconnexionAttaques)


        self.gridLayout.addLayout(self.gridLayoutMenuAttaques, 0, 0, 1, 1)

        self.gridLayoutContentAttaques = QGridLayout()
        self.gridLayoutContentAttaques.setObjectName(u"gridLayoutContentAttaques")
        self.pushButtonLancerAttaques = QPushButton(Attaques)
        self.pushButtonLancerAttaques.setObjectName(u"pushButtonLancerAttaques")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.pushButtonLancerAttaques.setFont(font1)
        self.pushButtonLancerAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.pushButtonLancerAttaques, 9, 0, 1, 1)

        self.checkBoxSQLI = QCheckBox(Attaques)
        self.checkBoxSQLI.setObjectName(u"checkBoxSQLI")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBoxSQLI.sizePolicy().hasHeightForWidth())
        self.checkBoxSQLI.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMono Nerd Font"])
        font2.setPointSize(12)
        self.checkBoxSQLI.setFont(font2)
        self.checkBoxSQLI.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00E920; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00E920; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxSQLI, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayoutContentAttaques.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayoutContentAttaques.addItem(self.verticalSpacer_3, 11, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayoutContentAttaques.addItem(self.verticalSpacer_2, 7, 0, 1, 1)

        self.labelNomAttaques_2 = QLabel(Attaques)
        self.labelNomAttaques_2.setObjectName(u"labelNomAttaques_2")
        font3 = QFont()
        font3.setFamilies([u"JetBrainsMono Nerd Font"])
        font3.setPointSize(16)
        font3.setBold(True)
        self.labelNomAttaques_2.setFont(font3)
        self.labelNomAttaques_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayoutContentAttaques.addWidget(self.labelNomAttaques_2, 0, 0, 1, 1)

        self.checkBoxClusterAttaques = QCheckBox(Attaques)
        self.checkBoxClusterAttaques.setObjectName(u"checkBoxClusterAttaques")
        sizePolicy1.setHeightForWidth(self.checkBoxClusterAttaques.sizePolicy().hasHeightForWidth())
        self.checkBoxClusterAttaques.setSizePolicy(sizePolicy1)
        self.checkBoxClusterAttaques.setFont(font2)
        self.checkBoxClusterAttaques.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00E920; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00E920; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxClusterAttaques, 10, 0, 1, 1)

        self.checkBoxXSS = QCheckBox(Attaques)
        self.checkBoxXSS.setObjectName(u"checkBoxXSS")
        sizePolicy1.setHeightForWidth(self.checkBoxXSS.sizePolicy().hasHeightForWidth())
        self.checkBoxXSS.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setFamilies([u"JetBrainsMonoNL Nerd Font"])
        font4.setPointSize(12)
        self.checkBoxXSS.setFont(font4)
        self.checkBoxXSS.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00E920; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00E920; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxXSS, 5, 0, 1, 1)

        self.pushButtonVisualiserAttaques = QPushButton(Attaques)
        self.pushButtonVisualiserAttaques.setObjectName(u"pushButtonVisualiserAttaques")
        self.pushButtonVisualiserAttaques.setFont(font1)
        self.pushButtonVisualiserAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.pushButtonVisualiserAttaques, 12, 0, 1, 1)

        self.checkBoxCSRF = QCheckBox(Attaques)
        self.checkBoxCSRF.setObjectName(u"checkBoxCSRF")
        sizePolicy1.setHeightForWidth(self.checkBoxCSRF.sizePolicy().hasHeightForWidth())
        self.checkBoxCSRF.setSizePolicy(sizePolicy1)
        self.checkBoxCSRF.setFont(font2)
        self.checkBoxCSRF.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00E920; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00E920; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxCSRF, 4, 0, 1, 1)

        self.labelChoixAttaques = QLabel(Attaques)
        self.labelChoixAttaques.setObjectName(u"labelChoixAttaques")
        font5 = QFont()
        font5.setFamilies([u"JetBrainsMono Nerd Font"])
        font5.setPointSize(14)
        self.labelChoixAttaques.setFont(font5)

        self.gridLayoutContentAttaques.addWidget(self.labelChoixAttaques, 2, 0, 1, 1)

        self.checkBoxHEADERSCOOKIES = QCheckBox(Attaques)
        self.checkBoxHEADERSCOOKIES.setObjectName(u"checkBoxHEADERSCOOKIES")
        sizePolicy1.setHeightForWidth(self.checkBoxHEADERSCOOKIES.sizePolicy().hasHeightForWidth())
        self.checkBoxHEADERSCOOKIES.setSizePolicy(sizePolicy1)
        self.checkBoxHEADERSCOOKIES.setFont(font2)
        self.checkBoxHEADERSCOOKIES.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00E920; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00E920; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxHEADERSCOOKIES, 6, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayoutContentAttaques, 1, 0, 1, 1)


        self.retranslateUi(Attaques)

        QMetaObject.connectSlotsByName(Attaques)
    # setupUi

    def retranslateUi(self, Attaques):
        Attaques.setWindowTitle(QCoreApplication.translate("Attaques", u"Attaques", None))
        self.labelLogo.setText("")
        self.pushButtonAccueilAttaques.setText(QCoreApplication.translate("Attaques", u"Accueil", None))
        self.pushButtonActualiteAttaques.setText(QCoreApplication.translate("Attaques", u"Actualit\u00e9", None))
        self.pushButtonDocumentationAttaques.setText(QCoreApplication.translate("Attaques", u"Documentation", None))
        self.pushButtonDeconnexionAttaques.setText("")
        self.pushButtonLancerAttaques.setText(QCoreApplication.translate("Attaques", u"Lancer ", None))
        self.checkBoxSQLI.setText(QCoreApplication.translate("Attaques", u"SQLI", None))
        self.labelNomAttaques_2.setText(QCoreApplication.translate("Attaques", u"Attaques", None))
        self.checkBoxClusterAttaques.setText(QCoreApplication.translate("Attaques", u"Attaque par cluster", None))
        self.checkBoxXSS.setText(QCoreApplication.translate("Attaques", u"XSS", None))
        self.pushButtonVisualiserAttaques.setText(QCoreApplication.translate("Attaques", u"Visualiser la cartographie", None))
        self.checkBoxCSRF.setText(QCoreApplication.translate("Attaques", u"CSRF", None))
        self.labelChoixAttaques.setText(QCoreApplication.translate("Attaques", u"Choisissez votre attaque:", None))
        self.checkBoxHEADERSCOOKIES.setText(QCoreApplication.translate("Attaques", u"Headers & Cookies", None))
    # retranslateUi

