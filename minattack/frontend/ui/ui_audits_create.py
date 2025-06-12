# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audits_create.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_AuditsCreate(object):
    def setupUi(self, AuditsCreate):
        if not AuditsCreate.objectName():
            AuditsCreate.setObjectName(u"AuditsCreate")
        AuditsCreate.resize(1400, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AuditsCreate.sizePolicy().hasHeightForWidth())
        AuditsCreate.setSizePolicy(sizePolicy)
        AuditsCreate.setMinimumSize(QSize(1400, 900))
        AuditsCreate.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font"])
        font.setPointSize(14)
        AuditsCreate.setFont(font)
        AuditsCreate.setStyleSheet(u"background-color: #300711;\n"
"color: white;\n"
"")
        self.gridLayout_4 = QGridLayout(AuditsCreate)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayoutMenuAuditsCreate = QGridLayout()
        self.gridLayoutMenuAuditsCreate.setObjectName(u"gridLayoutMenuAuditsCreate")
        self.labelLogo = QLabel(AuditsCreate)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(65, 42))
        self.labelLogo.setMaximumSize(QSize(65, 42))
        self.labelLogo.setPixmap(QPixmap(u"../resources/images/logo.png"))
        self.labelLogo.setScaledContents(True)

        self.gridLayoutMenuAuditsCreate.addWidget(self.labelLogo, 0, 0, 1, 1)

        self.pushButtonDocumentationAuditsCreate = QPushButton(AuditsCreate)
        self.pushButtonDocumentationAuditsCreate.setObjectName(u"pushButtonDocumentationAuditsCreate")
        font1 = QFont()
        font1.setFamilies([u"JetBrainsMono Nerd Font"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.pushButtonDocumentationAuditsCreate.setFont(font1)
        self.pushButtonDocumentationAuditsCreate.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAuditsCreate.addWidget(self.pushButtonDocumentationAuditsCreate, 0, 4, 1, 1)

        self.pushButtonActualiteAuditsCreate = QPushButton(AuditsCreate)
        self.pushButtonActualiteAuditsCreate.setObjectName(u"pushButtonActualiteAuditsCreate")
        self.pushButtonActualiteAuditsCreate.setFont(font1)
        self.pushButtonActualiteAuditsCreate.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAuditsCreate.addWidget(self.pushButtonActualiteAuditsCreate, 0, 3, 1, 1)

        self.pushButtonDeconnexionAuditsCreate = QPushButton(AuditsCreate)
        self.pushButtonDeconnexionAuditsCreate.setObjectName(u"pushButtonDeconnexionAuditsCreate")
        self.pushButtonDeconnexionAuditsCreate.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        icon = QIcon()
        icon.addFile(u"../resources/images/deconnexion.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionAuditsCreate.setIcon(icon)
        self.pushButtonDeconnexionAuditsCreate.setIconSize(QSize(32, 32))

        self.gridLayoutMenuAuditsCreate.addWidget(self.pushButtonDeconnexionAuditsCreate, 0, 7, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAuditsCreate.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAuditsCreate.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.pushButtonAccueilAuditsCreate = QPushButton(AuditsCreate)
        self.pushButtonAccueilAuditsCreate.setObjectName(u"pushButtonAccueilAuditsCreate")
        self.pushButtonAccueilAuditsCreate.setFont(font1)
        self.pushButtonAccueilAuditsCreate.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.gridLayoutMenuAuditsCreate.addWidget(self.pushButtonAccueilAuditsCreate, 0, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutMenuAuditsCreate, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelUrlAuditsCreate = QLabel(AuditsCreate)
        self.labelUrlAuditsCreate.setObjectName(u"labelUrlAuditsCreate")
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMono Nerd Font"])
        font2.setPointSize(16)
        self.labelUrlAuditsCreate.setFont(font2)

        self.gridLayout.addWidget(self.labelUrlAuditsCreate, 5, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 8, 1, 1, 1)

        self.labelWarningUrlAuditsCreate = QLabel(AuditsCreate)
        self.labelWarningUrlAuditsCreate.setObjectName(u"labelWarningUrlAuditsCreate")
        self.labelWarningUrlAuditsCreate.setEnabled(False)
        font3 = QFont()
        font3.setFamilies([u"JetBrainsMono Nerd Font"])
        font3.setPointSize(13)
        font3.setBold(False)
        font3.setItalic(True)
        self.labelWarningUrlAuditsCreate.setFont(font3)
        self.labelWarningUrlAuditsCreate.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.gridLayout.addWidget(self.labelWarningUrlAuditsCreate, 7, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.horizontalLayoutUrlAuditsCreate = QHBoxLayout()
        self.horizontalLayoutUrlAuditsCreate.setObjectName(u"horizontalLayoutUrlAuditsCreate")
        self.horizontalLayoutUrlAuditsCreate.setContentsMargins(0, 6, -1, 0)
        self.lineEditUrlAuditsCreate = QLineEdit(AuditsCreate)
        self.lineEditUrlAuditsCreate.setObjectName(u"lineEditUrlAuditsCreate")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEditUrlAuditsCreate.sizePolicy().hasHeightForWidth())
        self.lineEditUrlAuditsCreate.setSizePolicy(sizePolicy1)
        self.lineEditUrlAuditsCreate.setFont(font)
        self.lineEditUrlAuditsCreate.setStyleSheet(u"QLineEdit {\n"
"	border: 1px solid #ffffff;\n"
"    border-radius: 5px;\n"
"}")

        self.horizontalLayoutUrlAuditsCreate.addWidget(self.lineEditUrlAuditsCreate)

        self.pushButtonCreerAuditsCreate = QPushButton(AuditsCreate)
        self.pushButtonCreerAuditsCreate.setObjectName(u"pushButtonCreerAuditsCreate")
        self.pushButtonCreerAuditsCreate.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonCreerAuditsCreate.sizePolicy().hasHeightForWidth())
        self.pushButtonCreerAuditsCreate.setSizePolicy(sizePolicy2)
        self.pushButtonCreerAuditsCreate.setMinimumSize(QSize(180, 0))
        self.pushButtonCreerAuditsCreate.setMaximumSize(QSize(180, 16777215))
        font4 = QFont()
        font4.setFamilies([u"JetBrainsMono Nerd Font"])
        font4.setPointSize(14)
        font4.setBold(True)
        self.pushButtonCreerAuditsCreate.setFont(font4)
        self.pushButtonCreerAuditsCreate.setStyleSheet(u"QPushButton {\n"
"    background-color: #94112b; \n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #76061c;\n"
"}")

        self.horizontalLayoutUrlAuditsCreate.addWidget(self.pushButtonCreerAuditsCreate)


        self.gridLayout.addLayout(self.horizontalLayoutUrlAuditsCreate, 6, 1, 1, 1)

        self.labelNomAuditsSelect = QLabel(AuditsCreate)
        self.labelNomAuditsSelect.setObjectName(u"labelNomAuditsSelect")
        font5 = QFont()
        font5.setFamilies([u"JetBrainsMonoNL Nerd Font"])
        font5.setPointSize(16)
        font5.setBold(True)
        self.labelNomAuditsSelect.setFont(font5)
        self.labelNomAuditsSelect.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.labelNomAuditsSelect, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 2, 0, 1, 1)


        self.retranslateUi(AuditsCreate)

        QMetaObject.connectSlotsByName(AuditsCreate)
    # setupUi

    def retranslateUi(self, AuditsCreate):
        AuditsCreate.setWindowTitle(QCoreApplication.translate("AuditsCreate", u"Cr\u00e9ation d'audits", None))
        self.labelLogo.setText("")
        self.pushButtonDocumentationAuditsCreate.setText(QCoreApplication.translate("AuditsCreate", u"Documentation", None))
        self.pushButtonActualiteAuditsCreate.setText(QCoreApplication.translate("AuditsCreate", u"Actualit\u00e9", None))
        self.pushButtonDeconnexionAuditsCreate.setText("")
        self.pushButtonAccueilAuditsCreate.setText(QCoreApplication.translate("AuditsCreate", u"Accueil", None))
        self.labelUrlAuditsCreate.setText(QCoreApplication.translate("AuditsCreate", u"Cr\u00e9er un audit:", None))
        self.labelWarningUrlAuditsCreate.setText("")
        self.lineEditUrlAuditsCreate.setText("")
        self.lineEditUrlAuditsCreate.setPlaceholderText(QCoreApplication.translate("AuditsCreate", u"Entrer une url", None))
        self.pushButtonCreerAuditsCreate.setText(QCoreApplication.translate("AuditsCreate", u"Cr\u00e9er", None))
        self.labelNomAuditsSelect.setText(QCoreApplication.translate("AuditsCreate", u"Audits", None))
    # retranslateUi

