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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_Audits(object):
    def setupUi(self, Audits):
        if not Audits.objectName():
            Audits.setObjectName(u"Audits")
        Audits.resize(1000, 700)
        Audits.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_4 = QGridLayout(Audits)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayoutMenuAudits = QGridLayout()
        self.gridLayoutMenuAudits.setObjectName(u"gridLayoutMenuAudits")
        self.pushButtonAttaquesAudits = QPushButton(Audits)
        self.pushButtonAttaquesAudits.setObjectName(u"pushButtonAttaquesAudits")
        self.pushButtonAttaquesAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonAttaquesAudits, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAudits.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButtonHomeAudits = QPushButton(Audits)
        self.pushButtonHomeAudits.setObjectName(u"pushButtonHomeAudits")
        self.pushButtonHomeAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonHomeAudits, 0, 1, 1, 1)

        self.pushButtonCartographieAudits = QPushButton(Audits)
        self.pushButtonCartographieAudits.setObjectName(u"pushButtonCartographieAudits")
        self.pushButtonCartographieAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonCartographieAudits, 0, 6, 1, 1)

        self.pushButtonDeconnexionAudits = QPushButton(Audits)
        self.pushButtonDeconnexionAudits.setObjectName(u"pushButtonDeconnexionAudits")
        self.pushButtonDeconnexionAudits.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        icon = QIcon()
        icon.addFile(u"../../../../Downloads/image.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionAudits.setIcon(icon)
        self.pushButtonDeconnexionAudits.setIconSize(QSize(32, 32))

        self.gridLayoutMenuAudits.addWidget(self.pushButtonDeconnexionAudits, 0, 8, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutMenuAudits.addItem(self.horizontalSpacer_2, 0, 7, 1, 1)

        self.pushButtonRapportsAudits = QPushButton(Audits)
        self.pushButtonRapportsAudits.setObjectName(u"pushButtonRapportsAudits")
        self.pushButtonRapportsAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonRapportsAudits, 0, 5, 1, 1)

        self.pushButtonAuditsAudits = QPushButton(Audits)
        self.pushButtonAuditsAudits.setObjectName(u"pushButtonAuditsAudits")
        self.pushButtonAuditsAudits.setStyleSheet(u"QPushButton {\n"
"    background-color: #00C853; /* Vert */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #009624; / survol */\n"
"}")

        self.gridLayoutMenuAudits.addWidget(self.pushButtonAuditsAudits, 0, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutMenuAudits, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.labelNomAudits = QLabel(Audits)
        self.labelNomAudits.setObjectName(u"labelNomAudits")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.labelNomAudits.setFont(font)
        self.labelNomAudits.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.labelNomAudits, 4, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.retranslateUi(Audits)

        QMetaObject.connectSlotsByName(Audits)
    # setupUi

    def retranslateUi(self, Audits):
        Audits.setWindowTitle(QCoreApplication.translate("Audits", u"Audits", None))
        self.pushButtonAttaquesAudits.setText(QCoreApplication.translate("Audits", u"Attaques", None))
        self.pushButtonHomeAudits.setText(QCoreApplication.translate("Audits", u"Home", None))
        self.pushButtonCartographieAudits.setText(QCoreApplication.translate("Audits", u"Cartographie", None))
        self.pushButtonDeconnexionAudits.setText("")
        self.pushButtonRapportsAudits.setText(QCoreApplication.translate("Audits", u"Rapports", None))
        self.pushButtonAuditsAudits.setText(QCoreApplication.translate("Audits", u"Audits", None))
        self.labelNomAudits.setText(QCoreApplication.translate("Audits", u"Audits", None))
    # retranslateUi

