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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Cartographie(object):
    def setupUi(self, Cartographie):
        if not Cartographie.objectName():
            Cartographie.setObjectName(u"Cartographie")
        Cartographie.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Cartographie.sizePolicy().hasHeightForWidth())
        Cartographie.setSizePolicy(sizePolicy)
        Cartographie.setMinimumSize(QSize(1400, 900))
        Cartographie.setStyleSheet(u"background-color: #300711;\n"
"color: white;\n"
"")
        self.gridLayout_4 = QGridLayout(Cartographie)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(10, 10, 10, 10)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButtonLancerCartographie = QPushButton(Cartographie)
        self.pushButtonLancerCartographie.setObjectName(u"pushButtonLancerCartographie")
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(14)
        font.setBold(True)
        self.pushButtonLancerCartographie.setFont(font)
        self.pushButtonLancerCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayout.addWidget(self.pushButtonLancerCartographie, 10, 1, 1, 1)

        self.labelNomCartographie = QLabel(Cartographie)
        self.labelNomCartographie.setObjectName(u"labelNomCartographie")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.labelNomCartographie.setFont(font1)
        self.labelNomCartographie.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.labelNomCartographie, 4, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 5, 1, 1, 1)

        self.label = QLabel(Cartographie)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMono Nerd Font"])
        font2.setPointSize(14)
        self.label.setFont(font2)

        self.gridLayout.addWidget(self.label, 6, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.checkBoxFuzzingCartographie = QCheckBox(Cartographie)
        self.checkBoxFuzzingCartographie.setObjectName(u"checkBoxFuzzingCartographie")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBoxFuzzingCartographie.sizePolicy().hasHeightForWidth())
        self.checkBoxFuzzingCartographie.setSizePolicy(sizePolicy1)
        self.checkBoxFuzzingCartographie.setMinimumSize(QSize(0, 30))
        self.checkBoxFuzzingCartographie.setFont(font2)
        self.checkBoxFuzzingCartographie.setStyleSheet(u"QCheckBox {\n"
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
        self.checkBoxFuzzingCartographie.setChecked(False)
        self.checkBoxFuzzingCartographie.setAutoRepeat(False)

        self.horizontalLayout.addWidget(self.checkBoxFuzzingCartographie)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.lineEditWordlistPathCartographie = QLineEdit(Cartographie)
        self.lineEditWordlistPathCartographie.setObjectName(u"lineEditWordlistPathCartographie")
        self.lineEditWordlistPathCartographie.setEnabled(False)
        self.lineEditWordlistPathCartographie.setMinimumSize(QSize(0, 46))
        self.lineEditWordlistPathCartographie.setFont(font2)
        self.lineEditWordlistPathCartographie.setStyleSheet(u"QLineEdit {\n"
"	border: 1px solid #ffffff;\n"
"    border-radius: 5px;\n"
"}")

        self.horizontalLayout.addWidget(self.lineEditWordlistPathCartographie)


        self.gridLayout.addLayout(self.horizontalLayout, 9, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.verticalSpacer_2, 7, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 11, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.gridLayoutMenuCartographie = QGridLayout()
        self.gridLayoutMenuCartographie.setObjectName(u"gridLayoutMenuCartographie")
        self.pushButtonDeconnexionCartographie = QPushButton(Cartographie)
        self.pushButtonDeconnexionCartographie.setObjectName(u"pushButtonDeconnexionCartographie")
        self.pushButtonDeconnexionCartographie.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        icon = QIcon()
        icon.addFile(u"../resources/images/deconnexion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionCartographie.setIcon(icon)
        self.pushButtonDeconnexionCartographie.setIconSize(QSize(32, 32))

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonDeconnexionCartographie, 0, 7, 1, 1)

        self.pushButtonDocumentationCartographie = QPushButton(Cartographie)
        self.pushButtonDocumentationCartographie.setObjectName(u"pushButtonDocumentationCartographie")
        font3 = QFont()
        font3.setFamilies([u"JetBrainsMonoNL Nerd Font"])
        font3.setPointSize(12)
        font3.setBold(True)
        self.pushButtonDocumentationCartographie.setFont(font3)
        self.pushButtonDocumentationCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonDocumentationCartographie, 0, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuCartographie.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.pushButtonActualiteCartographie = QPushButton(Cartographie)
        self.pushButtonActualiteCartographie.setObjectName(u"pushButtonActualiteCartographie")
        font4 = QFont()
        font4.setFamilies([u"JetBrainsMono Nerd Font"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.pushButtonActualiteCartographie.setFont(font4)
        self.pushButtonActualiteCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonActualiteCartographie, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuCartographie.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.labelLogo = QLabel(Cartographie)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(65, 42))
        self.labelLogo.setMaximumSize(QSize(65, 42))
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.gridLayoutMenuCartographie.addWidget(self.labelLogo, 0, 0, 1, 1)

        self.pushButtonAccueilCartographie = QPushButton(Cartographie)
        self.pushButtonAccueilCartographie.setObjectName(u"pushButtonAccueilCartographie")
        self.pushButtonAccueilCartographie.setFont(font4)
        self.pushButtonAccueilCartographie.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuCartographie.addWidget(self.pushButtonAccueilCartographie, 0, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutMenuCartographie, 0, 0, 1, 1)


        self.retranslateUi(Cartographie)

        QMetaObject.connectSlotsByName(Cartographie)
    # setupUi

    def retranslateUi(self, Cartographie):
        Cartographie.setWindowTitle(QCoreApplication.translate("Cartographie", u"Cartographie", None))
        self.pushButtonLancerCartographie.setText(QCoreApplication.translate("Cartographie", u"Lancer", None))
        self.labelNomCartographie.setText(QCoreApplication.translate("Cartographie", u"Cartographie", None))
        self.label.setText(QCoreApplication.translate("Cartographie", u"Cette page vous permet de g\u00e9n\u00e9rer une cartographie dynamique \u00e0 partir des donn\u00e9es collect\u00e9es lors des audits.\n"
"Apr\u00e8s avoir selectionn\u00e9 vos attaques, cliquez sur Lancer pour visualiser la carte.", None))
        self.checkBoxFuzzingCartographie.setText(QCoreApplication.translate("Cartographie", u"Fuzzing", None))
        self.lineEditWordlistPathCartographie.setPlaceholderText(QCoreApplication.translate("Cartographie", u"(optionnel) chemin absolu de votre propre wordlist", None))
        self.pushButtonDeconnexionCartographie.setText("")
        self.pushButtonDocumentationCartographie.setText(QCoreApplication.translate("Cartographie", u"Documentation", None))
        self.pushButtonActualiteCartographie.setText(QCoreApplication.translate("Cartographie", u"Actualit\u00e9", None))
        self.labelLogo.setText("")
        self.pushButtonAccueilCartographie.setText(QCoreApplication.translate("Cartographie", u"Accueil", None))
    # retranslateUi

