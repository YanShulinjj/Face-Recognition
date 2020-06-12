# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:24:31 2020

@author: ysl
"""


'''
调用facenet
'''
import os
import cv2
import numpy as np
import joblib
from tqdm import tqdm
from keras.models import load_model
from keras.utils import plot_model
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
from mtcnn import MTCNN
from preprocessing import  get_face
from sklearn.model_selection import train_test_split

# 忽略警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
MARGIN = 0.5
IMAGE_SHAPE = (128, 128)

def process_img(img):

    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.equalizeHist(img)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if len(img) > 0:
        img = cv2.resize(img, IMAGE_SHAPE, interpolation=cv2.INTER_CUBIC)
        # 标准化
        mean, std = img.mean(), img.std()
        img = (img - mean) / std
        return img
    
class Mymodel():
    '''
    基于facenet的人脸识别
    '''
    
    def __init__(self):
        
        self.data_path = 'mtcnn_face'
        self.test_path = 'test_img'
            
        print('Loading the model...')
        self.model = load_model('model/model_encoder.h5')
        self.facenet2 = load_model('model/model_target.h5')

        # mtcnn 检测脸部
#        self.detector = MTCNN()

    def get_all_imgs(self, path):
        '''
        从文件读取图片
        :param dir:
        :return:
        '''

        print('\nLoading data....')
        # 循环读取本地图片
        data_1 = []
        labels = []
        dirs = os.listdir(self.data_path)
        for i,dir_ in tqdm(enumerate(dirs)):
            dir = os.path.join(path, dir_)
            if os.path.isdir(dir):
                fnames = os.listdir(dir)
                for fname in (fnames):
                    if fname.endswith('.bmp'):

                        fname = os.path.join(dir, fname)
        #                image1 = extract_face(fname)
                        image1 = cv2.imread(fname)
                        image1 = process_img(image1)

                        data_1.append(image1)
                        labels.append(dir_)
        return np.array(data_1), labels

    def split_data(self, data, labels, split_rate = 0.8):
        '''
        分0.8 在库里
        0.2 来测试
        '''
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=(1-split_rate), random_state=42)

        return X_train, X_test, y_train, y_test
    
    def save_mode_vector(self):

        data, labels = self.get_all_imgs(self.data_path)
        # 标准化
#        mean, std = data.mean(), data.std()
#        data = (data - mean) / std
        X_train, X_test, y_train, y_test = self.split_data(data, labels)
        X_train = np.array(X_train)
        vec = self.model.predict(X_train)

        print('Found {} modes !'.format(vec.shape[0]))

        return vec, np.array(y_train), np.array(X_test), np.array(y_test)



    def init(self):
        self.mode_v, self.labels, self.test_imgs, self.test_tags = self.save_mode_vector()

        print('Saving the mode...')
        joblib.dump((self.mode_v, self.labels, self.test_imgs, self.test_tags), open('data/mode_data.pkl', 'wb'))
        print('Successfully')
    def load(self):
        print('Loading the mode...')
        self.mode_v, self.labels, self.test_imgs, self.test_tags =joblib.load(open('data/mode_data.pkl', 'rb'))
        print('Successfully')
    
    def predict(self, img):
    #    img = process_img(img)
        img = np.expand_dims(img, axis=0)
        pre = self.facenet2.predict(img)
        res = cosine_similarity(self.mode_v, pre)
        idx = np.argmax(res, axis=0)

        return self.labels[idx[0]]  

    def add_class(self, imgs, person_name):
        '''
        添加新的人脸
        imgs 不少于10张
        '''
        for i, img in enumerate(imgs):
            fpath = os.path.join(self.data_path, person_name)
            if not os.path.exists(fpath):
                os.mkdir(fpath)
            fname = os.path.join(fpath, person_name+'-'+str(i)+'.bmp')
            
            cv2.imwrite(fname, img)
            print('Saving {}.. '.format(fname))
        
        print('Reloading the mode vector...')
        self.init()

    def acc(self):
        '''
        测试正确率
        '''
        count = 0
        for i, img in enumerate(tqdm(self.test_imgs)):
#            print(img, img.shape, i)
            pre = self.predict(img)
#            print(i, pre)
            if pre == self.test_tags[i]:

                count += 1

        print('Acc: {}'.format(count/len(self.test_imgs)))
        
    



# facenet = Mymodel()
# facenet.init()
##facenet.load()
#facenet.acc()

#test_imgs, tags = load_test_imgs(test_path)
#
#print('Saving the test_imgs...')
#joblib.dump((test_imgs, tags), open('data/test_imgs_data.pkl', 'wb'))
#print('Successfully')
#
#acc(test_imgs, tags)

