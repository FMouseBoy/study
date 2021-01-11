#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 手写数字辨识,卷积神经网络 Keras 2.4.3 tensorflow 2.4.0

import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Flatten
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam
from keras.utils import np_utils
from keras import backend as K

def load_data():
  path = './mnist.npz'
  f = np.load(path)
  x_data, y_data = f['x_train'], f['y_train']
  x_test, y_test = f['x_test'], f['y_test']
  x_data = x_data.reshape(x_data.shape[0], 28*28)
  x_data = x_data.astype('float32')
  x_test = x_test.reshape(x_test.shape[0], 28*28)
  x_test = x_test.astype('float32')
  # y_train之前可以理解为60000x1的数组，每个单元素数组的值就是样本所表示的数字
  y_data = np_utils.to_categorical(y_data,10)
  y_test = np_utils.to_categorical(y_test,10)
  x_data = x_data / 255 # 归一
  x_test = x_test / 255
  return (x_data, y_data), (x_test, y_test)



if __name__ == "__main__":
  (x_train, y_train), (x_test, y_test) = load_data()
  x_train = x_train.reshape(x_train.shape[0],28,28,1)
  x_test = x_test.reshape(x_test.shape[0],28,28,1)
  model = Sequential()
  # 如果是RGB的话，1就要改成3
  model.add(Conv2D(input_shape=(28,28,1), filters=25, kernel_size=(3,3)))
  model.add(MaxPooling2D(pool_size = (2,2)))
  model.add(Conv2D(filters=50, kernel_size=(3,3)))
  model.add(MaxPooling2D(pool_size = (2,2)))
  model.add(Flatten())   #比较关键的一层，将卷积结果“压平”，即将多维结果一维化，好过渡到全连接层
  model.add(Dense(units = 100,activation = 'relu'))
  model.add(Dense(units = 10, activation = 'softmax'))
  # model.summary()  # 输出每一层网络的参数
  model.compile(loss='categorical_crossentropy',optimizer='Adam', metrics=['accuracy'])
  model.fit(x_train, y_train, batch_size=100, epochs=20, )

  result_train = model.evaluate(x_train, y_train)
  result_test = model.evaluate(x_test, y_test)

  print('训练集准确度:', result_train[1])
  print('测试集准确度:', result_test[1])
  #保存模型
  model.save("modelCNNRecognition.h5")
  # 导入模型
  # model=keras.models.load_model('./modelCNNRecognition.h5')