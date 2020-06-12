# -*- coding: utf-8 -*-
# @Time    : 2020 2020/6/2 18:10
# @Author  : Lagrange
# @Email   : 1935971904@163.com
# @File    : preprocessing.py
# @Software: PyCharm

'''
对image的一些预处理函数
'''

import cv2
import dlib
import numpy as np
import copy

# 人脸分类器
detector = dlib.get_frontal_face_detector()

# 获取人脸分类检测器
predictor = dlib.shape_predictor(
    "data/shape_predictor_68_face_landmarks.dat"
)


def getPointsImg(img):
    '''
    使用dlib 提取脸部特征点
    :param img:
    :return:
    '''
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(img, 0)
    pos = []
    for face in dets:
        shape = predictor(img, face)
        # 遍历所有点，打印出坐标，并圈出来
        for pt in shape.parts():
            pt_pos = (pt.x, pt.y)
            # cv2.circle(img, pt_pos, 2, (255, 0, 0), 1)
            pos.append(pt_pos)
    return pos


# cv2 自带 分类器
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
detector = dlib.get_frontal_face_detector()


def get_face(image):
    """
    dlib detector返回值是<class 'dlib.dlib.rectangle'>，就是一个矩形
    坐标为[(x1, y1) (x2, y2)]
    可以通过函数的left,right,top,bottom方法分别获取对应的x1, x2, y1, y2值:
    """
    dstIndex = detector(image, 0)
    new_images = []
    pots = []
    min_size = (80, 80)
    for i, index in enumerate(dstIndex):
        x1 = index.left()
        y1 = index.top()
        x2 = index.right()
        y2 = index.bottom()
        if (x2 - x1) > min_size[0] and (y2 - y1) > min_size[1]:
            pots.append((x1, y1, x2, y2))
    #        srcImg = cv2.rectangle(srcImg, (x1, y1), (x2, y2), (0, 255, 0), 1)
            new_images.append(image[y1: y2, x1:x2])
    

    return  new_images, pots


#def get_face(image):
#    '''
#    在image里提取人脸部分
#    :param image:
#    :return: 被裁剪的图片， 裁剪框坐标
#    '''
#    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    faces = faceCascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5, minSize=(150, 150))
#    new_image = image
#    for (x, y, width, height) in faces:
##        cv2.rectangle(image, (x, y), (x+width, y+height), (0,0,0), 0)
##        cv2.putText(image, 'heheh', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
#        new_image = image[y: y+width, x:x+height]
#    
#    return np.array(new_image), faces


def equalization(img):
	'''
	三通道分别均衡化
	:return:
	'''
	(b, g, r) = cv2.split(img)
	equal_b = cv2.equalizeHist(b)
	equal_g = cv2.equalizeHist(g)
	equal_r = cv2.equalizeHist(r)
	dst = cv2.merge((equal_b, equal_g, equal_r))
	# cv2.imshow('img', img)
	# cv2.imshow('dst', dst)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	return dst