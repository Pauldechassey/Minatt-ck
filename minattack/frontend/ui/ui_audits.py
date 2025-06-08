# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audits.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Audits(object):
    def setupUi(self, Audits):
        if not Audits.objectName():
            Audits.setObjectName(u"Audits")
        Audits.resize(1400, 900)
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(14)
        Audits.setFont(font)
        Audits.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_4 = QGridLayout(Audits)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayoutMenuAudits = QGridLayout()
        self.gridLayoutMenuAudits.setObjectName(u"gridLayoutMenuAudits")
        self.pushButtonCartographieAudits = QPushButton(Audits)
        self.pushButtonCartographieAudits.setObjectName(u"pushButtonCartographieAudits")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.pushButtonCartographieAudits.setFont(font1)
        self.pushButtonCartographieAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonCartographieAudits, 0, 4, 1, 1)

        self.pushButtonHomeAudits = QPushButton(Audits)
        self.pushButtonHomeAudits.setObjectName(u"pushButtonHomeAudits")
        self.pushButtonHomeAudits.setFont(font1)
        self.pushButtonHomeAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonHomeAudits, 0, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAudits.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAudits.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.pushButtonDeconnexionAudits = QPushButton(Audits)
        self.pushButtonDeconnexionAudits.setObjectName(u"pushButtonDeconnexionAudits")
        self.pushButtonDeconnexionAudits.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        icon = QIcon()
        icon.addFile(u"../resources/images/deconnexion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionAudits.setIcon(icon)
        self.pushButtonDeconnexionAudits.setIconSize(QSize(32, 32))

        self.gridLayoutMenuAudits.addWidget(self.pushButtonDeconnexionAudits, 0, 7, 1, 1)

        self.pushButtonAuditsAudits = QPushButton(Audits)
        self.pushButtonAuditsAudits.setObjectName(u"pushButtonAuditsAudits")
        self.pushButtonAuditsAudits.setFont(font1)
        self.pushButtonAuditsAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonAuditsAudits, 0, 3, 1, 1)

        self.labelLogo = QLabel(Audits)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(65, 42))
        self.labelLogo.setMaximumSize(QSize(65, 42))
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.gridLayoutMenuAudits.addWidget(self.labelLogo, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutMenuAudits, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelNomAudits = QLabel(Audits)
        self.labelNomAudits.setObjectName(u"labelNomAudits")
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        self.labelNomAudits.setFont(font2)

        self.gridLayout.addWidget(self.labelNomAudits, 4, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.verticalLayoutContentAudits = QVBoxLayout()
        self.verticalLayoutContentAudits.setSpacing(10)
        self.verticalLayoutContentAudits.setObjectName(u"verticalLayoutContentAudits")
        self.labelUrlAudits = QLabel(Audits)
        self.labelUrlAudits.setObjectName(u"labelUrlAudits")
        font3 = QFont()
        font3.setPointSize(13)
        self.labelUrlAudits.setFont(font3)

        self.verticalLayoutContentAudits.addWidget(self.labelUrlAudits)

        self.gridLayoutUrlAudits = QGridLayout()
        self.gridLayoutUrlAudits.setObjectName(u"gridLayoutUrlAudits")
        self.gridLayoutUrlAudits.setVerticalSpacing(0)
        self.gridLayoutUrlAudits.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayoutUrlAudits = QHBoxLayout()
        self.horizontalLayoutUrlAudits.setObjectName(u"horizontalLayoutUrlAudits")
        self.horizontalLayoutUrlAudits.setContentsMargins(0, 6, -1, 0)
        self.lineEditUrlAudits = QLineEdit(Audits)
        self.lineEditUrlAudits.setObjectName(u"lineEditUrlAudits")
        self.lineEditUrlAudits.setStyleSheet(u"QLineEdit {\n"
"	border: 1px solid #ffffff;\n"
"}")

        self.horizontalLayoutUrlAudits.addWidget(self.lineEditUrlAudits)

        self.pushButtonCreerAudits = QPushButton(Audits)
        self.pushButtonCreerAudits.setObjectName(u"pushButtonCreerAudits")
        self.pushButtonCreerAudits.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCreerAudits.sizePolicy().hasHeightForWidth())
        self.pushButtonCreerAudits.setSizePolicy(sizePolicy)
        self.pushButtonCreerAudits.setMinimumSize(QSize(180, 0))
        self.pushButtonCreerAudits.setMaximumSize(QSize(180, 16777215))
        self.pushButtonCreerAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #2E2E2E;      \n"
"    color: white;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #4CAF50;      \n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #388E3C;      \n"
"}")

        self.horizontalLayoutUrlAudits.addWidget(self.pushButtonCreerAudits)


        self.gridLayoutUrlAudits.addLayout(self.horizontalLayoutUrlAudits, 0, 0, 1, 1)


        self.verticalLayoutContentAudits.addLayout(self.gridLayoutUrlAudits)

        self.labelWarningUrlAudits = QLabel(Audits)
        self.labelWarningUrlAudits.setObjectName(u"labelWarningUrlAudits")
        self.labelWarningUrlAudits.setEnabled(False)
        font4 = QFont()
        font4.setPointSize(11)
        font4.setBold(False)
        font4.setItalic(True)
        self.labelWarningUrlAudits.setFont(font4)
        self.labelWarningUrlAudits.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.verticalLayoutContentAudits.addWidget(self.labelWarningUrlAudits)

        self.labelSelectionUrlAudits = QLabel(Audits)
        self.labelSelectionUrlAudits.setObjectName(u"labelSelectionUrlAudits")
        self.labelSelectionUrlAudits.setFont(font3)

        self.verticalLayoutContentAudits.addWidget(self.labelSelectionUrlAudits)

        self.horizontalLayoutSelectionUrlAudits = QHBoxLayout()
        self.horizontalLayoutSelectionUrlAudits.setObjectName(u"horizontalLayoutSelectionUrlAudits")
        self.comboBoxSelectionUrlAudits = QComboBox(Audits)
        self.comboBoxSelectionUrlAudits.setObjectName(u"comboBoxSelectionUrlAudits")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxSelectionUrlAudits.sizePolicy().hasHeightForWidth())
        self.comboBoxSelectionUrlAudits.setSizePolicy(sizePolicy1)
        self.comboBoxSelectionUrlAudits.setStyleSheet(u"QComboBox{\n"
"	border: 1px solid #ffffff;\n"
"}")

        self.horizontalLayoutSelectionUrlAudits.addWidget(self.comboBoxSelectionUrlAudits)

        self.pushButtonSelectionUrlAudits = QPushButton(Audits)
        self.pushButtonSelectionUrlAudits.setObjectName(u"pushButtonSelectionUrlAudits")
        self.pushButtonSelectionUrlAudits.setMinimumSize(QSize(180, 0))
        self.pushButtonSelectionUrlAudits.setMaximumSize(QSize(180, 16777215))
        self.pushButtonSelectionUrlAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #2E2E2E;      \n"
"    color: white;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #4CAF50;      \n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #388E3C;      \n"
"}")

        self.horizontalLayoutSelectionUrlAudits.addWidget(self.pushButtonSelectionUrlAudits)


        self.verticalLayoutContentAudits.addLayout(self.horizontalLayoutSelectionUrlAudits)


        self.gridLayout.addLayout(self.verticalLayoutContentAudits, 6, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 8, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.retranslateUi(Audits)

        QMetaObject.connectSlotsByName(Audits)
    # setupUi

    def retranslateUi(self, Audits):
        Audits.setWindowTitle(QCoreApplication.translate("Audits", u"Audits", None))
        self.pushButtonCartographieAudits.setText(QCoreApplication.translate("Audits", u"Documentation", None))
        self.pushButtonHomeAudits.setText(QCoreApplication.translate("Audits", u"Accueil", None))
        self.pushButtonDeconnexionAudits.setText("")
        self.pushButtonAuditsAudits.setText(QCoreApplication.translate("Audits", u"Actualit\u00e9", None))
        self.labelLogo.setText("")
        self.labelNomAudits.setText(QCoreApplication.translate("Audits", u"Audits", None))
        self.labelUrlAudits.setText(QCoreApplication.translate("Audits", u"Cr\u00e9er un audit:", None))
        self.pushButtonCreerAudits.setText(QCoreApplication.translate("Audits", u"Cr\u00e9er", None))
        self.labelWarningUrlAudits.setText("")
        self.labelSelectionUrlAudits.setText(QCoreApplication.translate("Audits", u"S\u00e9lectionner un audit:", None))
        self.pushButtonSelectionUrlAudits.setText(QCoreApplication.translate("Audits", u"S\u00e9lectionner", None))
    # retranslateUi

