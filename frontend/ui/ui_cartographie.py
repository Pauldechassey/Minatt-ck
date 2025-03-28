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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1479, 754)
        Form.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.labelRapports = QLabel(self.frame)
        self.labelRapports.setObjectName(u"labelRapports")
        self.labelRapports.setGeometry(QRect(440, 260, 91, 31))

        self.gridLayout_3.addWidget(self.frame, 3, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButtonHomeCartographie = QPushButton(Form)
        self.pushButtonHomeCartographie.setObjectName(u"pushButtonHomeCartographie")

        self.horizontalLayout_2.addWidget(self.pushButtonHomeCartographie)

        self.pushButtonAttaquesCartographie = QPushButton(Form)
        self.pushButtonAttaquesCartographie.setObjectName(u"pushButtonAttaquesCartographie")

        self.horizontalLayout_2.addWidget(self.pushButtonAttaquesCartographie)

        self.pushButtonRapportsCartographie = QPushButton(Form)
        self.pushButtonRapportsCartographie.setObjectName(u"pushButtonRapportsCartographie")

        self.horizontalLayout_2.addWidget(self.pushButtonRapportsCartographie)

        self.pushButtonCartographieCartographie = QPushButton(Form)
        self.pushButtonCartographieCartographie.setObjectName(u"pushButtonCartographieCartographie")

        self.horizontalLayout_2.addWidget(self.pushButtonCartographieCartographie)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButtonDeconnexionCartographie = QPushButton(Form)
        self.pushButtonDeconnexionCartographie.setObjectName(u"pushButtonDeconnexionCartographie")
        self.pushButtonDeconnexionCartographie.setStyleSheet(u"background-color: #121212;\n"
"color: white;\n"
"")
        icon = QIcon()
        icon.addFile(u"../../../../Downloads/image.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonDeconnexionCartographie.setIcon(icon)
        self.pushButtonDeconnexionCartographie.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.pushButtonDeconnexionCartographie)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 1, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.labelRapports.setText(QCoreApplication.translate("Form", u"Cartographie", None))
        self.pushButtonHomeCartographie.setText(QCoreApplication.translate("Form", u"Home", None))
        self.pushButtonAttaquesCartographie.setText(QCoreApplication.translate("Form", u"Attaques", None))
        self.pushButtonRapportsCartographie.setText(QCoreApplication.translate("Form", u"Rapports", None))
        self.pushButtonCartographieCartographie.setText(QCoreApplication.translate("Form", u"Cartographie", None))
        self.pushButtonDeconnexionCartographie.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"Cartographie", None))
    # retranslateUi

