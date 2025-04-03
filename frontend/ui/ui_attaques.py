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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Attaques(object):
    def setupUi(self, Attaques):
        if not Attaques.objectName():
            Attaques.setObjectName(u"Attaques")
        Attaques.resize(1000, 700)
        Attaques.setStyleSheet(u"background-color: rgb(18, 18, 18);\n"
"color:white")
        self.gridLayout = QGridLayout(Attaques)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayoutMenuAttaques = QHBoxLayout()
        self.gridLayoutMenuAttaques.setObjectName(u"gridLayoutMenuAttaques")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAttaques.addItem(self.horizontalSpacer)

        self.pushButtonHomeAttaques = QPushButton(Attaques)
        self.pushButtonHomeAttaques.setObjectName(u"pushButtonHomeAttaques")
        self.pushButtonHomeAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonHomeAttaques)

        self.pushButtonAuditsAttaques = QPushButton(Attaques)
        self.pushButtonAuditsAttaques.setObjectName(u"pushButtonAuditsAttaques")
        self.pushButtonAuditsAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonAuditsAttaques)

        self.pushButtonAttaquesAttaques = QPushButton(Attaques)
        self.pushButtonAttaquesAttaques.setObjectName(u"pushButtonAttaquesAttaques")
        self.pushButtonAttaquesAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonAttaquesAttaques)

        self.pushButtonRapportsAttaques = QPushButton(Attaques)
        self.pushButtonRapportsAttaques.setObjectName(u"pushButtonRapportsAttaques")
        self.pushButtonRapportsAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonRapportsAttaques)

        self.pushButtonCartographieAttaques = QPushButton(Attaques)
        self.pushButtonCartographieAttaques.setObjectName(u"pushButtonCartographieAttaques")
        self.pushButtonCartographieAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonCartographieAttaques)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAttaques.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionAttaques = QPushButton(Attaques)
        self.pushButtonDeconnexionAttaques.setObjectName(u"pushButtonDeconnexionAttaques")

        self.gridLayoutMenuAttaques.addWidget(self.pushButtonDeconnexionAttaques)


        self.gridLayout.addLayout(self.gridLayoutMenuAttaques, 0, 0, 1, 1)

        self.gridLayoutContentAttaques = QGridLayout()
        self.gridLayoutContentAttaques.setObjectName(u"gridLayoutContentAttaques")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayoutContentAttaques.addItem(self.verticalSpacer_3, 11, 0, 1, 1)

        self.checkBoxSQLI = QCheckBox(Attaques)
        self.checkBoxSQLI.setObjectName(u"checkBoxSQLI")
        self.checkBoxSQLI.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00FF00; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00FF00; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxSQLI, 3, 0, 1, 1)

        self.checkBoxXSS = QCheckBox(Attaques)
        self.checkBoxXSS.setObjectName(u"checkBoxXSS")
        self.checkBoxXSS.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00FF00; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00FF00; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxXSS, 5, 0, 1, 1)

        self.checkBoxCSRF = QCheckBox(Attaques)
        self.checkBoxCSRF.setObjectName(u"checkBoxCSRF")
        self.checkBoxCSRF.setStyleSheet(u"QCheckBox {\n"
"    color: white;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #00FF00; \n"
"    background: black;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: #00FF00; \n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.checkBoxCSRF, 4, 0, 1, 1)

        self.pushButtonLancerAttaques = QPushButton(Attaques)
        self.pushButtonLancerAttaques.setObjectName(u"pushButtonLancerAttaques")
        self.pushButtonLancerAttaques.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 10px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutContentAttaques.addWidget(self.pushButtonLancerAttaques, 10, 0, 1, 1)

        self.lineEditUrlAttaques = QLineEdit(Attaques)
        self.lineEditUrlAttaques.setObjectName(u"lineEditUrlAttaques")

        self.gridLayoutContentAttaques.addWidget(self.lineEditUrlAttaques, 8, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayoutContentAttaques.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayoutContentAttaques.addItem(self.verticalSpacer_2, 6, 0, 1, 1)

        self.labelChoixAttaques = QLabel(Attaques)
        self.labelChoixAttaques.setObjectName(u"labelChoixAttaques")
        font = QFont()
        font.setPointSize(13)
        self.labelChoixAttaques.setFont(font)

        self.gridLayoutContentAttaques.addWidget(self.labelChoixAttaques, 2, 0, 1, 1)

        self.labelUrlAttaques = QLabel(Attaques)
        self.labelUrlAttaques.setObjectName(u"labelUrlAttaques")
        self.labelUrlAttaques.setFont(font)

        self.gridLayoutContentAttaques.addWidget(self.labelUrlAttaques, 7, 0, 1, 1)

        self.labelNomAttaques = QLabel(Attaques)
        self.labelNomAttaques.setObjectName(u"labelNomAttaques")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.labelNomAttaques.setFont(font1)
        self.labelNomAttaques.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayoutContentAttaques.addWidget(self.labelNomAttaques, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayoutContentAttaques, 1, 0, 1, 1)


        self.retranslateUi(Attaques)

        QMetaObject.connectSlotsByName(Attaques)
    # setupUi

    def retranslateUi(self, Attaques):
        Attaques.setWindowTitle(QCoreApplication.translate("Attaques", u"Attaques", None))
        self.pushButtonHomeAttaques.setText(QCoreApplication.translate("Attaques", u"Home", None))
        self.pushButtonAuditsAttaques.setText(QCoreApplication.translate("Attaques", u"Audits", None))
        self.pushButtonAttaquesAttaques.setText(QCoreApplication.translate("Attaques", u"Attaques", None))
        self.pushButtonRapportsAttaques.setText(QCoreApplication.translate("Attaques", u"Rapports", None))
        self.pushButtonCartographieAttaques.setText(QCoreApplication.translate("Attaques", u"Cartographie", None))
        self.pushButtonDeconnexionAttaques.setText("")
        self.checkBoxSQLI.setText(QCoreApplication.translate("Attaques", u"SQLI", None))
        self.checkBoxXSS.setText(QCoreApplication.translate("Attaques", u"CheckBoxXSS", None))
        self.checkBoxCSRF.setText(QCoreApplication.translate("Attaques", u"CSRF", None))
        self.pushButtonLancerAttaques.setText(QCoreApplication.translate("Attaques", u"PushButton", None))
        self.labelChoixAttaques.setText(QCoreApplication.translate("Attaques", u"Choisissez votre attaque:", None))
        self.labelUrlAttaques.setText(QCoreApplication.translate("Attaques", u"Rentrez l'URL:", None))
        self.labelNomAttaques.setText(QCoreApplication.translate("Attaques", u"Attaques", None))
    # retranslateUi

