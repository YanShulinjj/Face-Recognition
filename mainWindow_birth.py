# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\综合课设三\界面\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os
import sys
import numpy as np
import cv2
import time
import datetime
import random
import tensorflow as tf
from database import Database, Record
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from preprocessing import get_face, getPointsImg
#from facenet import Facenet, process_img
from birth import Mymodel, process_img
from confirmeWindow import Sign_window
from newWindow import New_person_window
from recordWindow import Record_window
from sucessWindow import Success_window
from bio_recgoniztion import eye, mouth
# 忽略警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings("ignore")

person_name = 'none'
data_path = 'mtcnn_face'

def add_class(imgs, person_name):
    '''
    添加新的人脸
    imgs 不少于10张
    '''
    for i, img in enumerate(imgs):
        fpath = os.path.join(data_path, person_name)
        if not os.path.exists(fpath):
            os.mkdir(fpath)
        fname = os.path.join(fpath, person_name + '-' + str(i) + '.bmp')

        cv2.imwrite(fname, img)
        print('Saving {}.. '.format(fname))



class Backend(QThread):
    '''
    子线程
    '''
    signal = pyqtSignal(str)  # 设置触发信号传递的参数数据类型,这里是字符串
    finished = pyqtSignal()
    stop =pyqtSignal()
    def __init__(self):
        super(Backend, self).__init__()

    def set_facenet(self, facenet):
        self.facenet = facenet


    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        '''
        添加 新用户的脸部信息
        添加包含20 张的脸部信息
        '''
        count = 0
        imgelist = []
        global person_name
        while count < 20:
            frames, boxs = get_face(camera.currentFrame)
            if len(boxs) > 0:
                for frame in frames:
                    if len(frame) > 0:
                        self.signal.emit('capture frame {}...  left {} frames !'.format(count + 1, 19 - count))
                        imgelist.append(frame)
                        count += 1
            time.sleep(0.5)
        self.signal.emit('Updating ues\'s faces !'.format(person_name))
        self.stop.emit()
        add_class(imgelist, person_name)
        self.stop.emit()
        self.finished.emit()

class Camera():
    '''
    摄像头类；
    打开摄像头获取帧
    '''
    def __init__(self, capture):
        '''
        param capture: cv2 捕获器
        '''
        self.cap = capture
        self.currentFrame = np.array([])

    def captureCurrentFrame(self):
        '''
        读取当前帧
        :return:
        '''
        ret, frame = self.cap.read()
        if ret:
            self.currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def transfer2QImage(self, faces, tags, tip = ''):
        '''
        使用cv2获取的图片转成Qimage
        '''
        curren_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        try:
            # self.currentFrame, _ = getPointsImg(self.currentFrame)
            frame = self.currentFrame
            for i, (x1, y1, x2, y2) in enumerate(faces):
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                frame = cv2.putText(frame, tags[i], (x1, y1),  cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            frame = cv2.putText(frame, tip, (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            frame = cv2.putText(frame, curren_time, (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            # 转化为pyqt里能显示的QPixmap
            heght, width = frame.shape[:2]
            img = QImage(frame, width, heght, QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            return img
        except:
            return None

## 定义一个全局camera
cap = cv2.VideoCapture(0) #  从摄像头捕获

camera = Camera(cap)


class Main_window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1008, 800)
        Form.setMaximumSize(QtCore.QSize(1200, 800))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(238, 250, 254))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(110, 123, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(147, 164, 169))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(238, 250, 254))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        # palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(238, 250, 254))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(110, 123, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(147, 164, 169))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(238, 250, 254))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        # palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(110, 123, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(238, 250, 254))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(110, 123, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(147, 164, 169))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(110, 123, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(110, 123, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(221, 246, 253))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        # palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        Form.setPalette(palette)
        Form.setMouseTracking(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.sign = QtWidgets.QPushButton(self.groupBox_2)
        self.sign.setGeometry(QtCore.QRect(40, 110, 93, 28))
        self.sign.setObjectName("sign")
        self.log = QtWidgets.QPushButton(self.groupBox_2)
        self.log.setGeometry(QtCore.QRect(40, 420, 93, 28))
        self.log.setObjectName("log")
        self.add_new_person = QtWidgets.QPushButton(self.groupBox_2)
        self.add_new_person.setGeometry(QtCore.QRect(40, 270, 93, 28))
        self.add_new_person.setObjectName("add_new_person")
        self.exit = QtWidgets.QPushButton(self.groupBox_2)
        self.exit.setGeometry(QtCore.QRect(40, 570, 93, 28))
        self.exit.setObjectName("exit")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(500, 500))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget = QtWidgets.QLabel(self.groupBox)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 234, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 202, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 113, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 212, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        # palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 234, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 202, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 113, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 212, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        # palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 234, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 202, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 113, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        # palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.widget.setPalette(palette)
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        self.widget.setObjectName("widget")
        self.widget.setAlignment(Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.widget)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.display = QtWidgets.QTextBrowser(self.groupBox_3)
        self.display.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.display.setObjectName("display")
        self.verticalLayout.addWidget(self.display)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.verticalLayout_2.setStretch(0, 3)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addWidget(self.splitter)

        #加载模型
        self.init()

        # 定义计时器
        self.timer = QTimer(Form)
        self.timer.timeout.connect(self.play)
        self.timer.start(27)

        #连接数据库
        self.peron_db = Database()
        self.record_db = Record()

        # 定义子线程
        self.backend = Backend()
        self.backend.set_facenet(self.facenet)
        self.backend.stop.connect(self.block)
        self.Form = Form
        self.triggered()
        self.retranslateUi(Form)
        self.colorful()
        self.add_windows()

        QtCore.QMetaObject.connectSlotsByName(Form)


    def colorful(self):
        '''
        修改控件风格
        :return:
        '''
        self.sign.setIcon(QIcon('icons/sign.png'))
        self.add_new_person.setIcon(QIcon('icons/new.png'))
        self.log.setIcon(QIcon('icons/record.png'))
        self.exit.setIcon(QIcon('icons/exit.png'))

        # 设置button 鼠标风格
        self.sign.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_new_person.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.log.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.Form.setStyleSheet('''
            QPushButton{border:none;color:black;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
        ''')
        self.Form.setWindowIcon(QIcon('icons/love.png'))

    def block(self):

        '''
        模型预测 和 重载再不同线程需要阻塞

        '''
        if self.model_block:
            self.facenet.init()
        self.model_block = not self.model_block

    def init(self):
        '''
        导入模型
        :return:
        '''
        self.eye_times = 0
        self.mouth_time = 0
        self.finished = 0
        self.tip = ''
        self.model_block = True
        self.sign_fg = False
        self.facenet = Mymodel()
        self.facenet.load()
        self.display.setText('-- Welcome to Face Recognition. v0.0 ' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    def add_windows(self):
        '''
        添加 子页面
        :return:
        '''
        # 签到界面
        self.sign_window = Sign_window()
        self.sign_widget = QtWidgets.QWidget()
        self.sign_window.setupUi(self.sign_widget)
        self.sign_window.confirm.clicked.connect(lambda: self.is_exits(which=0))
        self.sign_window.confirm2.clicked.connect(self.start_sign)
        self.sign_window.confirm2.clicked.connect(self.sign_widget.close)
        self.sign_window.cancel.clicked.connect(self.sign_widget.close)

        # 查询记录时
        self.sign_window1 = Sign_window()
        self.sign_widget1= QtWidgets.QWidget()
        self.sign_window1.setupUi(self.sign_widget1)
        self.sign_window1.confirm.clicked.connect(lambda: self.is_exits(which=1))
        self.sign_window1.confirm2.clicked.connect(self.show_table)
        self.sign_window1.confirm2.clicked.connect(self.sign_widget1.close)
        self.sign_window1.cancel.clicked.connect(self.sign_widget1.close)

        # 添加新脸界面
        self.new_window = New_person_window()
        self.new_widget = QtWidgets.QWidget()
        self.new_window.setupUi(self.new_widget)
        self.new_window.cancel.clicked.connect(self.new_widget.close)
        self.add_new_person.clicked.connect(self.new_widget.show)

        # person_name = new_window.name.text()
        self.new_window.confirm.clicked.connect(self.add)
        self.sign.clicked.connect(self.sign_widget.show)
        self.log.clicked.connect(self.sign_widget1.show)

    def is_exits(self, which = 0):
        # 判断用户输入的id是否在库中
        if which == 0:
            id = self.sign_window.input.toPlainText()
        else:
            id = self.sign_window1.input.toPlainText()

        if len(self.peron_db.search(id)) == 0:
            # 如果没有在库中，弹出警告
            qw = QWidget()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/love.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            QMessageBox.setWindowIcon(qw, icon)
            QMessageBox.information(qw, "提示", "找不到你的员工号 ！", QMessageBox.Ok)
            return True
        return False
    def start_sign(self):
        '''
        开始签到
        :return:
        '''

        if not self.is_exits():
            self.tip = 'Start to Sign'
            self.comman = [0, 1, 1, 0] # 0 为眨眼， 1为张嘴
            random.shuffle(self.comman)
            self.finished = 0
            self.sign_fg = True

    def isblank(self):
        '''
        判断信息是否全部都填写
        '''
        name = self.new_window.name.text()
        if not name:
            return True
        elif not self.new_window.male.isChecked() and not self.new_window.female.isChecked():
            return True
        telephone = self.new_window.telephone.text()
        if not telephone:
            return True
        address = self.new_window.address.text()
        if not address:
            return True

        return False


    def add(self):
        '''
        获取 new window里的名字 然后新加人脸
        :return:
        '''

        if self.isblank():
            # 弹窗警告
            qw = QWidget()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/love.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            QMessageBox.setWindowIcon(qw, icon)
            QMessageBox.information(qw, "提示", "请完整填写信息 ！", QMessageBox.Ok)
            return
        self.name = self.new_window.name.text()
        if self.new_window.male.isChecked():
            sex = '男'
        elif self.new_window.female.isChecked():
            sex = '女'


        telephone = self.new_window.telephone.text()
        address = self.new_window.address.text()
        headers = ['T', 'R', 'H']
        departments = ['技术部', '研发部', '人力资源部']
        idx = self.new_window.job.currentIndex()

        header = headers[idx]
        department = departments[idx]
        print('department: ', department)
        i = 0
        self.id = header + '0000' + str(i)
        while len(self.peron_db.search(self.id)) > 0:
            i += 1
            self.id = header + '0000' + str(i)
        self.peron_db.insert(self.id, self.name, sex, telephone, address, department)

        global person_name
        person_name = str(self.name)
        self.backend.start()
        self.new_widget.close()


    def triggered(self):
        '''
        绑定一些事件
        :return:
        '''
        # self.add_new_person.clicked.connect(self.backend.start)
        self.backend.signal.connect(self.display_info)

        self.backend.finished.connect(self.show_success)


    def show_success(self):
        '''
        显示录入成功界面
        :return:
        '''
        # 弹出一个窗口请牢记您的员工号
        self.success_window = Success_window()
        self.success_widget = QWidget()
        self.success_window.setupUi(self.success_widget)
        self.success_window.id.setText(self.id)
        self.success_window.label.setText('恭喜 {} 录入成功!'.format(self.name))
        self.success_widget.show()

    def display_info(self, info):
        '''
        :return:
        '''
        self.display.setText(info)

    def show_table(self):
        '''
        展示签到记录
        :return:
        '''
        id = self.sign_window1.input.toPlainText()
        if id:
            data = self.record_db.search(id)
        else:
            data = self.record_db.get_table_value()

        self.record_window = Record_window()
        self.record_widgt = QWidget()
        self.record_window.setupUi(self.record_widgt)
        self.record_window.insert_data(data)
        self.record_widgt.show()


    def exit(self):
        '''

        :return:
        '''
        self.peron_db.close()
        self.record_db.close()

    def play(self):

        camera.captureCurrentFrame()
        frames, boxs  = get_face(camera.currentFrame)
        tags = []
        if len(boxs) > 0:
            ### 预测人脸并画框显示

            if self.sign_fg:
                print(self.finished)
                if self.finished == len(self.comman) - 1:
                    print('完成！')
                    self.tip = 'Great'
                    self.sign_fg = False

                elif self.comman[self.finished] == 0:
                    self.tip = 'Move your eyes'
                else:
                    self.tip = 'Open your mouth'
            for f in frames:
                if len(f) > 0:
                    pots = getPointsImg(f)

                    if len(pots) > 0 and self.sign_fg:
                        # 如果开始签到
                        if self.comman[self.finished] == 0 and eye(pots):
                            self.finished += 1

                        elif self.comman[self.finished] == 1 and mouth(pots):
                            self.finished += 1

                    try:
                        f = process_img(f)
                    except:
                        return
                    if self.model_block:
                        tag = self.facenet.predict(f)
                        if tag.startswith('0'):
                            tag = 'unknown'
                    else:
                        return
                    if not self.sign_fg and self.finished != 0:
                        self.finished = 0
                        current_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                        id = self.sign_window.input.toPlainText()
                        # 判断 id 和 检测人名是否匹配
                        res = self.peron_db.search(id)
                        if tag == res[0][1]:
                            # 匹配成功
                            info = '-- {} {} 签到成功！'.format(id, tag) + current_time
                            self.record_db.insert(id, tag, current_time)
                        else:
                            info = '-- {} {} 签到失败！ 员工号和名字不匹配 ！'.format(id, tag) + current_time

                        self.display.append(info)
                    tags.append(tag)
            pass
        self.imge = camera.transfer2QImage(boxs, tags, self.tip)
        self.widget.setPixmap(self.imge)
        self.widget.setScaledContents(True)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "FaceWindow"))
        self.groupBox_2.setTitle(_translate("Form", "Menu"))
        self.sign.setText(_translate("Form", "签到"))
        self.log.setText(_translate("Form", "签到记录"))
        self.add_new_person.setText(_translate("Form", "新人录入"))
        self.exit.setText(_translate("Form", "退出系统"))
        self.groupBox.setTitle(_translate("Form", "camera"))
        self.groupBox_3.setTitle(_translate("Form", "Information"))



if __name__ == '__main__':

    app = QApplication(sys.argv)
    main_widget = QtWidgets.QWidget()
    main_window = Main_window()
    main_window.setupUi(main_widget)
    main_widget.show()
    main_window.exit.clicked.connect(main_widget.close)
    sys.exit(app.exec_())