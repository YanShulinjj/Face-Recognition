# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\综合课设三\界面\confirme.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Sign_window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(651, 307)
        Form.setMaximumSize(QtCore.QSize(651, 307))
        Form.setWindowIcon(QIcon('icons/love.png'))
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(270, 280, 101, 20))
        self.label_3.setObjectName("label_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 120, 631, 131))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(460, 0, 171, 61))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.job = QtWidgets.QComboBox(self.groupBox_3)
        self.job.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.job.setObjectName("job")
        self.job.addItem("")
        self.job.addItem("")
        self.job.addItem("")
        self.horizontalLayout.addWidget(self.job)
        self.confirm2 = QtWidgets.QPushButton(self.groupBox_2)
        self.confirm2.setGeometry(QtCore.QRect(140, 90, 101, 31))
        self.confirm2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirm2.setObjectName("confirm2")
        self.cancel = QtWidgets.QPushButton(self.groupBox_2)
        self.cancel.setGeometry(QtCore.QRect(370, 90, 101, 31))
        self.cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel.setObjectName("cancel")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 631, 101))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.confirm = QtWidgets.QPushButton(self.groupBox)
        self.confirm.setGeometry(QtCore.QRect(540, 30, 71, 41))
        self.confirm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.confirm.setAutoDefault(False)
        self.confirm.setDefault(False)
        self.confirm.setFlat(False)
        self.confirm.setObjectName("confirm")
        self.input = QtWidgets.QTextEdit(self.groupBox)
        self.input.setGeometry(QtCore.QRect(100, 30, 401, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(18)
        font.setItalic(True)
        self.input.setFont(font)
        self.input.setStyleSheet("border:none;\n"
"backgraond-color:gray\n"
"")
        self.input.setObjectName("input")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 40, 81, 31))
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(14)
        font.setUnderline(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Verify"))
        self.label_3.setText(_translate("Form", "Copyright@ysl"))
        self.label_2.setText(_translate("Form", "所在部门"))
        self.job.setItemText(0, _translate("Form", "技术部"))
        self.job.setItemText(1, _translate("Form", "研发部"))
        self.job.setItemText(2, _translate("Form", "人力资源部"))
        self.confirm2.setText(_translate("Form", "确认"))
        self.cancel.setText(_translate("Form", "取消"))
        self.confirm.setText(_translate("Form", "确认"))
        self.input.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Century Gothic\'; font-size:18pt; font-weight:400; font-style:italic;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:9pt; font-style:normal;\"><br /></p></body></html>"))
        self.label_6.setText(_translate("Form", "员工号："))
