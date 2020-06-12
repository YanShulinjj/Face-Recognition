# -*- coding: utf-8 -*-
# @Time    : 2020 2020/6/10 15:53
# @Author  : Lagrange
# @Email   : 1935971904@163.com
# @File    : bio_recgoniztion.py
# @Software: PyCharm
# Reference https://blog.csdn.net/Lee_01/article/details/89151044

'''
活体检测
'''
import numpy as np
from preprocessing import  getPointsImg

EAR_THRESH = 0.2
MAR_THRESH = 0.5
def get_eye_rate(eye):
    '''

    :param eye:  一只眼睛的六个点
    :return:  眼长宽比方程结果
    '''

    A = np.linalg.norm(eye[1]-eye[5])
    B = np.linalg.norm(eye[2]-eye[4])
    C = 2.*np.linalg.norm(eye[0]-eye[3])
    return (A+B)/C

def get_mouth_rate(mouth):

    A = np.linalg.norm(mouth[2] - mouth[9])  # 51, 59
    B = np.linalg.norm(mouth[4] - mouth[7])  # 53, 57
    C = np.linalg.norm(mouth[0] - mouth[6])  # 49, 55

    return (A+B)/(2.0*C)

def eye(pots1):
    '''
    当长宽比小于阈值时，认为闭眼
    :param pots1:
    :return:
    '''
    leye, reye = np.array(pots1[36: 42]), np.array(pots1[42: 48])

    e1 = get_eye_rate(leye)
    e2 = get_eye_rate(reye)

    return e2 < EAR_THRESH or e1 < EAR_THRESH

def mouth(pots1):
    '''
    当长宽比大于某阈值时， 认为张开嘴巴
    :param pots1:
    :return:
    '''

    mou = np.array(pots1[48: 60])  # 嘴唇内圈
    return get_mouth_rate(mou) > MAR_THRESH
