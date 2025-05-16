# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'audits.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_Audits(object):
    def setupUi(self, Audits):
        if not Audits.objectName():
            Audits.setObjectName("Audits")
        Audits.resize(1000, 700)
        Audits.setStyleSheet("background-color: #121212;\n" "color: white;\n" "")
        self.gridLayout_4 = QGridLayout(Audits)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayoutMenuAudits = QGridLayout()
        self.gridLayoutMenuAudits.setObjectName("gridLayoutMenuAudits")
        self.pushButtonAttaquesAudits = QPushButton(Audits)
        self.pushButtonAttaquesAudits.setObjectName("pushButtonAttaquesAudits")
        self.pushButtonAttaquesAudits.setStyleSheet(
            "QPushButton {\n"
            "    background-color: #00C853; /* Vert */\n"
            "    color: white;\n"
            "    font-weight: bold;\n"
            "    border-radius: 5px;\n"
            "    padding: 8px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: #009624; / survol */\n"
            "}"
        )

        self.gridLayoutMenuAudits.addWidget(self.pushButtonAttaquesAudits, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayoutMenuAudits.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.pushButtonHomeAudits = QPushButton(Audits)
        self.pushButtonHomeAudits.setObjectName("pushButtonHomeAudits")
        self.pushButtonHomeAudits.setStyleSheet(
            "QPushButton {\n"
            "    background-color: #00C853; /* Vert */\n"
            "    color: white;\n"
            "    font-weight: bold;\n"
            "    border-radius: 5px;\n"
            "    padding: 8px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: #009624; / survol */\n"
            "}"
        )

        self.gridLayoutMenuAudits.addWidget(self.pushButtonHomeAudits, 0, 1, 1, 1)

        self.pushButtonCartographieAudits = QPushButton(Audits)
        self.pushButtonCartographieAudits.setObjectName("pushButtonCartographieAudits")
        self.pushButtonCartographieAudits.setStyleSheet(
            "QPushButton {\n"
            "    background-color: #00C853; /* Vert */\n"
            "    color: white;\n"
            "    font-weight: bold;\n"
            "    border-radius: 5px;\n"
            "    padding: 8px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: #009624; / survol */\n"
            "}"
        )

        self.gridLayoutMenuAudits.addWidget(
            self.pushButtonCartographieAudits, 0, 6, 1, 1
        )

        self.pushButtonDeconnexionAudits = QPushButton(Audits)
        self.pushButtonDeconnexionAudits.setObjectName("pushButtonDeconnexionAudits")
        self.pushButtonDeconnexionAudits.setStyleSheet(
            "background-color: #121212;\n" "color: white;\n" ""
        )
        icon = QIcon()
        icon.addFile(
            "../../../../Downloads/image.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.pushButtonDeconnexionAudits.setIcon(icon)
        self.pushButtonDeconnexionAudits.setIconSize(QSize(32, 32))

        self.gridLayoutMenuAudits.addWidget(
            self.pushButtonDeconnexionAudits, 0, 8, 1, 1
        )

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.gridLayoutMenuAudits.addItem(self.horizontalSpacer_2, 0, 7, 1, 1)

        self.pushButtonRapportsAudits = QPushButton(Audits)
        self.pushButtonRapportsAudits.setObjectName("pushButtonRapportsAudits")
        self.pushButtonRapportsAudits.setStyleSheet(
            "QPushButton {\n"
            "    background-color: #00C853; /* Vert */\n"
            "    color: white;\n"
            "    font-weight: bold;\n"
            "    border-radius: 5px;\n"
            "    padding: 8px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: #009624; / survol */\n"
            "}"
        )

        self.gridLayoutMenuAudits.addWidget(self.pushButtonRapportsAudits, 0, 5, 1, 1)

        self.pushButtonAuditsAudits = QPushButton(Audits)
        self.pushButtonAuditsAudits.setObjectName("pushButtonAuditsAudits")
        self.pushButtonAuditsAudits.setStyleSheet(
            "QPushButton {\n"
            "    background-color: #00C853; /* Vert */\n"
            "    color: white;\n"
            "    font-weight: bold;\n"
            "    border-radius: 5px;\n"
            "    padding: 8px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: #009624; / survol */\n"
            "}"
        )

        self.gridLayoutMenuAudits.addWidget(self.pushButtonAuditsAudits, 0, 2, 1, 1)

        self.gridLayout_4.addLayout(self.gridLayoutMenuAudits, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayoutContentAudits = QVBoxLayout()
        self.verticalLayoutContentAudits.setObjectName("verticalLayoutContentAudits")
        self.labelUrlAudits = QLabel(Audits)
        self.labelUrlAudits.setObjectName("labelUrlAudits")
        font = QFont()
        font.setPointSize(13)
        self.labelUrlAudits.setFont(font)

        self.verticalLayoutContentAudits.addWidget(self.labelUrlAudits)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEditUrlAudits = QLineEdit(Audits)
        self.lineEditUrlAudits.setObjectName("lineEditUrlAudits")

        self.gridLayout_2.addWidget(self.lineEditUrlAudits, 0, 0, 1, 1)

        self.pushButtonCreerAudits = QPushButton(Audits)
        self.pushButtonCreerAudits.setObjectName("pushButtonCreerAudits")

        self.gridLayout_2.addWidget(self.pushButtonCreerAudits, 0, 1, 1, 1)

        self.verticalLayoutContentAudits.addLayout(self.gridLayout_2)

        self.labelSelectionUrlAudits = QLabel(Audits)
        self.labelSelectionUrlAudits.setObjectName("labelSelectionUrlAudits")
        self.labelSelectionUrlAudits.setFont(font)

        self.verticalLayoutContentAudits.addWidget(self.labelSelectionUrlAudits)

        self.gridLayout.addLayout(self.verticalLayoutContentAudits, 6, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.labelNomAudits = QLabel(Audits)
        self.labelNomAudits.setObjectName("labelNomAudits")
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.labelNomAudits.setFont(font1)
        self.labelNomAudits.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.labelNomAudits, 4, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer_2, 7, 1, 1, 1)

        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Audits)

        QMetaObject.connectSlotsByName(Audits)

    # setupUi

    def retranslateUi(self, Audits):
        Audits.setWindowTitle(QCoreApplication.translate("Audits", "Audits", None))
        self.pushButtonAttaquesAudits.setText(
            QCoreApplication.translate("Audits", "Attaques", None)
        )
        self.pushButtonHomeAudits.setText(
            QCoreApplication.translate("Audits", "Home", None)
        )
        self.pushButtonCartographieAudits.setText(
            QCoreApplication.translate("Audits", "Cartographie", None)
        )
        self.pushButtonDeconnexionAudits.setText("")
        self.pushButtonRapportsAudits.setText(
            QCoreApplication.translate("Audits", "Rapports", None)
        )
        self.pushButtonAuditsAudits.setText(
            QCoreApplication.translate("Audits", "Audits", None)
        )
        self.labelUrlAudits.setText(
            QCoreApplication.translate("Audits", "Cr\u00e9er un audit:", None)
        )
        self.pushButtonCreerAudits.setText(
            QCoreApplication.translate("Audits", "Cr\u00e9er un audit", None)
        )
        self.labelSelectionUrlAudits.setText(
            QCoreApplication.translate("Audits", "S\u00e9lectionner un audit:", None)
        )
        self.labelNomAudits.setText(
            QCoreApplication.translate("Audits", "Audits", None)
        )

    # retranslateUi
