# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 20:29:35 2020

@author: ysl
"""

'''
参考 https://www.sohu.com/a/214143960_465975
    https://kexue.fm/archives/4493
'''



'''
孪生神经网络
'''
import os

import cv2
import keras
from keras.layers import Input,Dense,Conv2D
from keras.layers import MaxPooling2D,Flatten,Convolution2D, Concatenate
from keras.models import Model

import numpy as np
from PIL import Image
from tqdm import tqdm
from keras.optimizers import SGD
from preprocessing import equalization
from keras.callbacks import EarlyStopping
import random
from keras.layers import Input,Embedding,LSTM,Dense,Lambda
from keras.layers.merge import dot
from keras.models import Model, load_model
from keras import backend as K
from keras.applications.vgg16 import VGG16
 

data_path = 'face'
IMAGE_SHAPE = (128,128)
INPUT_SHAPE = (128,128,3)
MARGIN = 0.5    # 效果最佳
 



def process_img(img):
    
    img = cv2.resize(img, IMAGE_SHAPE, interpolation=cv2.INTER_CUBIC)
    #彩色均衡化
#    img = equalization(img)
    return img




def get_data(path, split_rate = 0.2):
    '''
    从文件读取图片作为正样本
    再从另外的文件夹提取图片作为负样本
    :param dir:
    :return:
    '''

    print('\nLoading data....')
    # 读取正样本
    dirs = os.listdir(path)
    # 循环读取本地图片
    data_1 = []     #固定image
    data_2 = []     #正例image
    for dir_ in tqdm(dirs):
        dir = os.path.join(path, dir_)
        fnames = os.listdir(dir)
        for fname in (fnames):
            if fname.endswith('.bmp'):
                # 这是固定影像
                image1 = cv2.imread(os.path.join(dir, fname))
                image1 = cv2.resize(image1, IMAGE_SHAPE, interpolation=cv2.INTER_CUBIC)
                #彩色均衡化
#                image1 = equalization(image1)
                
                # 这是正例子
                random_fname = random.choice(fnames)
                image2 = cv2.imread(os.path.join(dir, random_fname))
                image2 = cv2.resize(image2, IMAGE_SHAPE, interpolation=cv2.INTER_CUBIC)
                #彩色均衡化
#                image2 = equalization(image2)
                # 
                data_1.append(image1)
                data_2.append(image2)
          
        #反例        
        data_3 = []
        list_dir = dirs[:]
        n_images = len(data_1)
        for i in (range(n_images)):
            random_dir = random.choice(list_dir)
            while random_dir == dir_:
                random_dir = random.choice(list_dir)
            fnames = os.listdir(os.path.join(data_path, random_dir))
            fname = random.choice(fnames)
            if fname.endswith('.bmp'):
                image3 = cv2.imread(os.path.join(data_path, random_dir, fname))
                image3 = cv2.resize(image3, IMAGE_SHAPE, interpolation=cv2.INTER_CUBIC)
                # 彩色均衡化
#                image3 = equalization(image3)
                data_3.append(image3)

    data_1 = np.array(data_1)
    data_2 = np.array(data_2)
    data_3 = np.array(data_3)
    #组合数据
    print(data_1.shape)
    print(data_2.shape)
    print(data_3.shape)
#    data = np.stack([data_1, data_2, data_3], axis=1)


    labels = np.ones(shape=(len(data_1),))
    print('Labels \'s shape is {}'.format(labels.shape))

    # 数据标准化
#    x = data / 255.
    mean1, std1 = data_1.mean(), data_1.std()
    data_1 = (data_1 - mean1) / std1
    
    mean2, std2 = data_2.mean(), data_2.std()
    data_2 = (data_2 - mean2) / std2
    
    mean3, std3 = data_3.mean(), data_3.std()
    data_3 = (data_3 - mean3) / std3
     
    # label 转 one_hot
    y = labels
    # y = to_categorical(labels)

    # 首先打乱数据集
    index = list(range(len(y)))
    np.random.shuffle(index)
#    x = x[index, :]
    x1 = data_1[index, :]
    x2 = data_2[index, :]
    x3 = data_3[index, :]
    y = y[index]

    # 划分数据集
#    boundary = int(len(y) * (1 - split_rate))
#    train_x1, valid = x1[:boundary]
#    train_x2 = x2[:boundary]
#    train_x3 = x3[:boundary]
#    
#    train_x, train_y, valid_x, valid_y = x[:boundary], y[:boundary], x[boundary:], y[boundary:]

#    return train_x, train_y, valid_x, valid_y
    return x1, x2, x3, y
    
    
 
 
def vgg_16_base(input_tensor):
   
    net = Conv2D(64,(3,3),activation='relu',padding='same',input_shape=INPUT_SHAPE)(input_tensor)
    net = Conv2D(64,(3,3),activation='relu',padding='same')(net)
    net = MaxPooling2D((2,2),strides=(2,2))(net)
 
    net = Conv2D(128,(3,3),activation='relu',padding='same')(net)
    net = Conv2D(128,(3,3),activation='relu',padding='same')(net)
    net= MaxPooling2D((2,2),strides=(2,2))(net)
 
    net = Conv2D(256,(3,3),activation='relu',padding='same')(net)
    net = Conv2D(256,(3,3),activation='relu',padding='same')(net)
    net = Conv2D(256,(3,3),activation='relu',padding='same')(net)
    net = MaxPooling2D((2,2),strides=(2,2))(net)
 
    net = Conv2D(512,(3,3),activation='relu',padding='same')(net)
    net = Conv2D(512,(3,3),activation='relu',padding='same')(net)
    net = Conv2D(512,(3,3),activation='relu',padding='same')(net)
    net = MaxPooling2D((2,2),strides=(2,2))(net)
 
    net = Conv2D(512,(3,3),activation='relu',padding='same')(net)
    net = Conv2D(512,(3,3),activation='relu',padding='same')(net)
    net = Conv2D(512,(3,3),activation='relu',padding='same')(net)
    net = MaxPooling2D((2,2),strides=(2,2))(net)
    net = Flatten()(net)
    net = Dense(128)(net)
    

    return net
 
    

from keras.optimizers import Adam

 
def siamese():
    input_tensor = Input(shape=INPUT_SHAPE)
    vgg_model1 = Model(input_tensor,vgg_16_base(input_tensor))
#    vgg_model2 = Model(input_tensor,vgg_16_base(input_tensor))
#    vgg_model3 = Model(input_tensor,vgg_16_base(input_tensor))

    input_im1 = Input(shape=INPUT_SHAPE, name = 'Anchor')  # 固定图像
    input_im2 = Input(shape=INPUT_SHAPE, name = 'Positive')  # 正例图像
    input_im3 = Input(shape=INPUT_SHAPE, name = 'Negtive')  # 反例图像
    out_im1 = vgg_model1(input_im1)
    out_im2 = vgg_model1(input_im2)
    out_im3 = vgg_model1(input_im3)
    
#    out_im1 = Dense(128)(out_im1)
#    out_im2 = Dense(128)(out_im2)
#    out_im3 = Dense(128)(out_im3)
    


    right_cos = dot([out_im1, out_im2], -1, normalize=True)
    wrong_cos = dot([out_im1, out_im3], -1, normalize=True)

    Triple_loss = Lambda(lambda x: K.relu(MARGIN + x[0] - x[1]))([wrong_cos, right_cos])
    
    
    train_model = Model(inputs=[input_im1, input_im2, input_im3], outputs=Triple_loss)
    model_encoder = Model(inputs=input_im1, outputs=out_im1)
    model_right_encoder = Model(inputs=input_im2, outputs=out_im2)
   
    
    train_model.compile(optimizer=SGD(lr=1e-4, decay = 1e-6), loss=lambda y_true, y_pred: y_pred)   # 忽视y_ture
    model_encoder.compile(optimizer='adam', loss='mse')
    model_right_encoder.compile(optimizer='adam', loss='mse')
    
    return train_model, model_encoder, model_right_encoder





def generate(x1, x2, x3, y, batch_size = 32):
    '''
    转成迭代器运行
    '''
    if batch_size > len(x1):
        batch_size = len(x1)
    while True:
        cnt = 0  
        X1, X2, X3 =[],[],[]
        Y =[]
        for i in range(len(x1)):  
            # create Numpy arrays of input data  
            # and labels, from each line in the file
            xx1, xx2, xx3, yy = x1[i], x2[i], x3[i], y[i]
#            print('hhhh', i)
            X1.append(xx1)  
            X2.append(xx2)
            X3.append(xx3)
            Y.append(yy)
            cnt += 1  
            if cnt == batch_size:
                cnt = 0  
                yield ([np.array(X1), np.array(X2), np.array(X3)], np.array(Y))  
                X1, X2, X3 = [], [], []
                Y = []  


from keras.callbacks import EarlyStopping

def train():
    x1, x2, x3, y = get_data(os.path.join(data_path))
#    gen_data = []
#    gen_valid_data = [[valid_x[i], valid_y[i]]for i in range(len(valid_y))]
    
    
    train_model, model_encoder, model_right_encoder = siamese()
    train_model.summary()
    
    #sgd = SGD(lr=1e-6,momentum=0.9,decay=1e-6,nesterov=True)
    #model.compile(optimizer=sgd,loss='mse',metrics=['accuracy'])
    
    
    
    gen = generate(x1, x2, x3, y)

    train_model.fit_generator(gen, 
                        steps_per_epoch=len(x1)/200, 
                        epochs=200, 
                        callbacks = [EarlyStopping(monitor='loss', patience = 4)]
                        )
    train_model.save('model/train_mdoel.h5')
    model_encoder.save('model/model_encoder.h5')
    model_right_encoder.save('model/model_target.h5')
    print('Models Saved !')



train()
##
#model_scr = load_model('model/model_encoder.h5')
#model_target = load_model('model/model_target.h5')
#
#mode_v = save_mode_vector()  
#img1 = cv2.imread('face/001/001-001.bmp')
#img2 = cv2.imread('face/002/002-001.bmp')
#img3 = cv2.imread('face/003/003-001.bmp')
#print(predict(img1))
#print(predict(img2))
#print(predict(img3))

