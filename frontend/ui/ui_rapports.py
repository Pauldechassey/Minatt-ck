# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rapports.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(818, 474)
        Form.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonHomeRapports = QPushButton(Form)
        self.pushButtonHomeRapports.setObjectName(u"pushButtonHomeRapports")

        self.horizontalLayout.addWidget(self.pushButtonHomeRapports)

        self.pushButtonAttaquesRapports = QPushButton(Form)
        self.pushButtonAttaquesRapports.setObjectName(u"pushButtonAttaquesRapports")

        self.horizontalLayout.addWidget(self.pushButtonAttaquesRapports)

        self.pushButtonRapportsRapports = QPushButton(Form)
        self.pushButtonRapportsRapports.setObjectName(u"pushButtonRapportsRapports")

        self.horizontalLayout.addWidget(self.pushButtonRapportsRapports)

        self.pushButtonCartographieRapports = QPushButton(Form)
        self.pushButtonCartographieRapports.setObjectName(u"pushButtonCartographieRapports")

        self.horizontalLayout.addWidget(self.pushButtonCartographieRapports)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionRapports = QPushButton(Form)
        self.pushButtonDeconnexionRapports.setObjectName(u"pushButtonDeconnexionRapports")
        icon = QIcon()
        icon.addFile(u"../../../../Downloads/image.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionRapports.setIcon(icon)
        self.pushButtonDeconnexionRapports.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.pushButtonDeconnexionRapports)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.labelRapports = QLabel(self.frame)
        self.labelRapports.setObjectName(u"labelRapports")
        self.labelRapports.setGeometry(QRect(430, 110, 91, 31))

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButtonHomeRapports.setText(QCoreApplication.translate("Form", u"Home", None))
        self.pushButtonAttaquesRapports.setText(QCoreApplication.translate("Form", u"Attaques", None))
        self.pushButtonRapportsRapports.setText(QCoreApplication.translate("Form", u"Rapports", None))
        self.pushButtonCartographieRapports.setText(QCoreApplication.translate("Form", u"Cartographie", None))
        self.pushButtonDeconnexionRapports.setText("")
        self.labelRapports.setText(QCoreApplication.translate("Form", u"Rapports", None))
    # retranslateUi

