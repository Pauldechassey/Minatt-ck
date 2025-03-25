# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'attacks.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Attacks(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1437, 694)
        Form.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButtonHomeAttaques = QPushButton(Form)
        self.pushButtonHomeAttaques.setObjectName(u"pushButtonHomeAttaques")

        self.horizontalLayout_2.addWidget(self.pushButtonHomeAttaques)

        self.pushButtonAttaquesAttaques = QPushButton(Form)
        self.pushButtonAttaquesAttaques.setObjectName(u"pushButtonAttaquesAttaques")

        self.horizontalLayout_2.addWidget(self.pushButtonAttaquesAttaques)

        self.pushButtonRapportsAttaques = QPushButton(Form)
        self.pushButtonRapportsAttaques.setObjectName(u"pushButtonRapportsAttaques")

        self.horizontalLayout_2.addWidget(self.pushButtonRapportsAttaques)

        self.pushButtonCartographieAttaques = QPushButton(Form)
        self.pushButtonCartographieAttaques.setObjectName(u"pushButtonCartographieAttaques")

        self.horizontalLayout_2.addWidget(self.pushButtonCartographieAttaques)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionAttaques = QPushButton(Form)
        self.pushButtonDeconnexionAttaques.setObjectName(u"pushButtonDeconnexionAttaques")
        icon = QIcon()
        icon.addFile(u"../../../../Downloads/image.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionAttaques.setIcon(icon)
        self.pushButtonDeconnexionAttaques.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.pushButtonDeconnexionAttaques)


        self.formLayout.setLayout(0, QFormLayout.SpanningRole, self.horizontalLayout_2)

        self.labelChoixAttaques = QLabel(Form)
        self.labelChoixAttaques.setObjectName(u"labelChoixAttaques")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.labelChoixAttaques)

        self.checkBoxSQLI = QCheckBox(Form)
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
        self.checkBoxSQLI.setTristate(False)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.checkBoxSQLI)

        self.labelURL = QLabel(Form)
        self.labelURL.setObjectName(u"labelURL")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.labelURL)

        self.lineEditURlAttaques = QLineEdit(Form)
        self.lineEditURlAttaques.setObjectName(u"lineEditURlAttaques")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lineEditURlAttaques)

        self.pushButtonLancerAttaques = QPushButton(Form)
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

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.pushButtonLancerAttaques)

        self.checkBoxCSRF = QCheckBox(Form)
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

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.checkBoxCSRF)

        self.checkBoxXSS = QCheckBox(Form)
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

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.checkBoxXSS)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButtonHomeAttaques.setText(QCoreApplication.translate("Form", u"Home", None))
        self.pushButtonAttaquesAttaques.setText(QCoreApplication.translate("Form", u"Attaques", None))
        self.pushButtonRapportsAttaques.setText(QCoreApplication.translate("Form", u"Rapports", None))
        self.pushButtonCartographieAttaques.setText(QCoreApplication.translate("Form", u"Cartographie", None))
        self.pushButtonDeconnexionAttaques.setText("")
        self.labelChoixAttaques.setText(QCoreApplication.translate("Form", u"Choisissez votre attaque:", None))
        self.checkBoxSQLI.setText(QCoreApplication.translate("Form", u"SQLI", None))
        self.labelURL.setText(QCoreApplication.translate("Form", u"Rentrer l'URL:", None))
        self.pushButtonLancerAttaques.setText(QCoreApplication.translate("Form", u"Lancer", None))
        self.checkBoxCSRF.setText(QCoreApplication.translate("Form", u"CSRF", None))
        self.checkBoxXSS.setText(QCoreApplication.translate("Form", u"XSS", None))
    # retranslateUi

