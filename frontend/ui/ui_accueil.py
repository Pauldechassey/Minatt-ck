# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'accueil.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_Accueil(object):
    def setupUi(self, Accueil):
        if not Accueil.objectName():
            Accueil.setObjectName(u"Accueil")
        Accueil.resize(1000, 700)
        self.label = QLabel(Accueil)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(440, 20, 81, 41))

        self.retranslateUi(Accueil)

        QMetaObject.connectSlotsByName(Accueil)
    # setupUi

    def retranslateUi(self, Accueil):
        Accueil.setWindowTitle(QCoreApplication.translate("Accueil", u"Accueil", None))
        self.label.setText(QCoreApplication.translate("Accueil", u"MinAtt&ck", None))
    # retranslateUi

