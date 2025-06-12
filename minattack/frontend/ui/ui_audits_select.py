# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audits_select.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_AuditsSelect(object):
    def setupUi(self, AuditsSelect):
        if not AuditsSelect.objectName():
            AuditsSelect.setObjectName(u"AuditsSelect")
        AuditsSelect.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AuditsSelect.sizePolicy().hasHeightForWidth())
        AuditsSelect.setSizePolicy(sizePolicy)
        AuditsSelect.setMinimumSize(QSize(1400, 900))
        AuditsSelect.setMaximumSize(QSize(1400, 900))
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(14)
        AuditsSelect.setFont(font)
        AuditsSelect.setStyleSheet(u"background-color: #300711;\n"
"color: white;\n"
"")
        self.gridLayout_4 = QGridLayout(AuditsSelect)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(10, 10, 10, 10)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.horizontalLayoutSelectionUrlAuditsSelect = QHBoxLayout()
        self.horizontalLayoutSelectionUrlAuditsSelect.setObjectName(u"horizontalLayoutSelectionUrlAuditsSelect")
        self.comboBoxSelectionUrlAuditsSelect = QComboBox(AuditsSelect)
        self.comboBoxSelectionUrlAuditsSelect.setObjectName(u"comboBoxSelectionUrlAuditsSelect")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxSelectionUrlAuditsSelect.sizePolicy().hasHeightForWidth())
        self.comboBoxSelectionUrlAuditsSelect.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(13)
        self.comboBoxSelectionUrlAuditsSelect.setFont(font1)
        self.comboBoxSelectionUrlAuditsSelect.setStyleSheet(u"QComboBox{\n"
"	border: 1px solid #ffffff;\n"
"}")

        self.horizontalLayoutSelectionUrlAuditsSelect.addWidget(self.comboBoxSelectionUrlAuditsSelect)

        self.pushButtonSelectionUrlAuditsSelect = QPushButton(AuditsSelect)
        self.pushButtonSelectionUrlAuditsSelect.setObjectName(u"pushButtonSelectionUrlAuditsSelect")
        self.pushButtonSelectionUrlAuditsSelect.setMinimumSize(QSize(180, 0))
        self.pushButtonSelectionUrlAuditsSelect.setMaximumSize(QSize(180, 16777215))
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMono Nerd Font"])
        font2.setPointSize(14)
        font2.setBold(True)
        self.pushButtonSelectionUrlAuditsSelect.setFont(font2)
        self.pushButtonSelectionUrlAuditsSelect.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.horizontalLayoutSelectionUrlAuditsSelect.addWidget(self.pushButtonSelectionUrlAuditsSelect)


        self.gridLayout.addLayout(self.horizontalLayoutSelectionUrlAuditsSelect, 6, 1, 1, 1)

        self.labelSelectionUrlAuditsSelect = QLabel(AuditsSelect)
        self.labelSelectionUrlAuditsSelect.setObjectName(u"labelSelectionUrlAuditsSelect")
        font3 = QFont()
        font3.setFamilies([u"JetBrainsMono Nerd Font"])
        font3.setPointSize(16)
        self.labelSelectionUrlAuditsSelect.setFont(font3)

        self.gridLayout.addWidget(self.labelSelectionUrlAuditsSelect, 5, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 7, 1, 1, 1)

        self.labelNomAuditsSelect = QLabel(AuditsSelect)
        self.labelNomAuditsSelect.setObjectName(u"labelNomAuditsSelect")
        font4 = QFont()
        font4.setFamilies([u"JetBrainsMono Nerd Font"])
        font4.setPointSize(16)
        font4.setBold(True)
        self.labelNomAuditsSelect.setFont(font4)
        self.labelNomAuditsSelect.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.labelNomAuditsSelect, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.gridLayoutMenuAuditsSelect = QGridLayout()
        self.gridLayoutMenuAuditsSelect.setObjectName(u"gridLayoutMenuAuditsSelect")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAuditsSelect.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.pushButtonActualiteAuditsSelect = QPushButton(AuditsSelect)
        self.pushButtonActualiteAuditsSelect.setObjectName(u"pushButtonActualiteAuditsSelect")
        font5 = QFont()
        font5.setFamilies([u"JetBrainsMono Nerd Font"])
        font5.setPointSize(12)
        font5.setBold(True)
        self.pushButtonActualiteAuditsSelect.setFont(font5)
        self.pushButtonActualiteAuditsSelect.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAuditsSelect.addWidget(self.pushButtonActualiteAuditsSelect, 0, 3, 1, 1)

        self.pushButtonAccueilAuditsSelect = QPushButton(AuditsSelect)
        self.pushButtonAccueilAuditsSelect.setObjectName(u"pushButtonAccueilAuditsSelect")
        self.pushButtonAccueilAuditsSelect.setFont(font5)
        self.pushButtonAccueilAuditsSelect.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAuditsSelect.addWidget(self.pushButtonAccueilAuditsSelect, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAuditsSelect.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.labelLogo = QLabel(AuditsSelect)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(65, 42))
        self.labelLogo.setMaximumSize(QSize(65, 42))
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.gridLayoutMenuAuditsSelect.addWidget(self.labelLogo, 0, 0, 1, 1)

        self.pushButtonDocumentationAuditsSelect = QPushButton(AuditsSelect)
        self.pushButtonDocumentationAuditsSelect.setObjectName(u"pushButtonDocumentationAuditsSelect")
        self.pushButtonDocumentationAuditsSelect.setFont(font5)
        self.pushButtonDocumentationAuditsSelect.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAuditsSelect.addWidget(self.pushButtonDocumentationAuditsSelect, 0, 4, 1, 1)

        self.pushButtonDeconnexionAuditsSelect = QPushButton(AuditsSelect)
        self.pushButtonDeconnexionAuditsSelect.setObjectName(u"pushButtonDeconnexionAuditsSelect")
        self.pushButtonDeconnexionAuditsSelect.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        icon = QIcon()
        icon.addFile(u"../resources/images/deconnexion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionAuditsSelect.setIcon(icon)
        self.pushButtonDeconnexionAuditsSelect.setIconSize(QSize(32, 32))

        self.gridLayoutMenuAuditsSelect.addWidget(self.pushButtonDeconnexionAuditsSelect, 0, 7, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutMenuAuditsSelect, 0, 0, 1, 1)


        self.retranslateUi(AuditsSelect)

        QMetaObject.connectSlotsByName(AuditsSelect)
    # setupUi

    def retranslateUi(self, AuditsSelect):
        AuditsSelect.setWindowTitle(QCoreApplication.translate("AuditsSelect", u"S\u00e9lection d'audit", None))
        self.pushButtonSelectionUrlAuditsSelect.setText(QCoreApplication.translate("AuditsSelect", u"S\u00e9lectionner", None))
        self.labelSelectionUrlAuditsSelect.setText(QCoreApplication.translate("AuditsSelect", u"S\u00e9lectionner un audit:", None))
        self.labelNomAuditsSelect.setText(QCoreApplication.translate("AuditsSelect", u"Audits", None))
        self.pushButtonActualiteAuditsSelect.setText(QCoreApplication.translate("AuditsSelect", u"Actualit\u00e9", None))
        self.pushButtonAccueilAuditsSelect.setText(QCoreApplication.translate("AuditsSelect", u"Accueil", None))
        self.labelLogo.setText("")
        self.pushButtonDocumentationAuditsSelect.setText(QCoreApplication.translate("AuditsSelect", u"Documentation", None))
        self.pushButtonDeconnexionAuditsSelect.setText("")
    # retranslateUi

