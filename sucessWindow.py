# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\综合课设三\界面\sucess.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Success_window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(350, 170)
        Form.setMaximumSize(350, 170)
        Form.setWindowIcon(QIcon('icons/love.png'))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(120, 30, 161, 31))
        font = QtGui.QFont()
        font.setFamily("华文仿宋")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 171, 31))
        font = QtGui.QFont()
        font.setFamily("华文仿宋")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.id = QtWidgets.QLabel(Form)
        self.id.setGeometry(QtCore.QRect(230, 110, 131, 31))
        font = QtGui.QFont()
        font.setFamily("华文仿宋")
        font.setPointSize(20)
        font.setUnderline(True)
        self.id.setFont(font)
        self.id.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.id.setObjectName("id")
        self.img = QtWidgets.QLabel(Form)
        self.img.setGeometry(QtCore.QRect(66, 20, 106, 60))
        self.img.setObjectName("img")

        self.init()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def init(self):
        pix = QPixmap('icons/ss.png')
        # self.img.setGeometry(0, 0, 50, 50)
        # self.img.setStyleSheet("border: 2px solid red")
        self.img.setPixmap(pix)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Congratulations"))
        self.label.setText(_translate("Form", "恭喜你 录入你成功"))
        self.label_2.setText(_translate("Form", "请牢记你的员工号："))
        self.id.setText(_translate("Form", "U000001"))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = QWidget()
    window = Success_window()
    window.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())