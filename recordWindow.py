# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\综合课设三\界面\record.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Record_window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(787, 683)
        Form.setWindowIcon(QIcon('icons/love.png'))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.display = QtWidgets.QTableWidget(self.groupBox)
        self.display.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.display.setObjectName("display")
        self.display.setColumnCount(0)
        self.display.setRowCount(0)
        self.verticalLayout.addWidget(self.display)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.init()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def init(self):
        self.display.setColumnWidth(0, 40)
        self.display.setColumnWidth(1, 200)
        self.display.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.display.horizontalHeader().setResizeContentsPrecision(0)
        self.display.resizeColumnToContents(0)
        self.display.setColumnCount(3)
        self.display.setHorizontalHeaderLabels(['员工号', '名字', '打卡时间'])

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Record"))
        self.groupBox.setTitle(_translate("Form", "签到记录"))
        self.label_3.setText(_translate("Form", "Copyright@ysl"))


    def insert_data(self, data):
        '''
        将data显示在表内
        :param data:
        :return:
        '''
        self.display.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(3):
                item = QTableWidgetItem(str(data[i][j]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if i % 2 == 0:
                    item.setBackground(QBrush(QColor(100, 149, 237)))  # 176,196,222
                else:
                    item.setBackground(QBrush(QColor(176, 196, 222)))
                self.display.setItem(i, j, item)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = QWidget()
    window = Record_window()
    window.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())