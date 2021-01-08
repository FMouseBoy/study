#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 参考
# 1、 https://mrsuncodes.github.io/2020/03/19/%E6%9D%8E%E5%AE%8F%E6%AF%85%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0-%E7%AC%AC%E4%BA%8C%E8%AF%BE%E4%BD%9C%E4%B8%9A/#more
# 2、 https://www.cnblogs.com/HL-space/p/10785225.html

import numpy as np
import pandas as pd


def dataProcess(train_data):
  x = train_data[:, 1:-1]
  # 处理最后两列属于至0、1附近
  x[:,-1:] /= np.mean(x[:,-1:])
  x[:,-2:-1] /= np.mean(x[:,-2:-1])
  y = train_data[:, -1:]
  
  return x, y


def _sigmoid(z):
  # 为避免溢出，设置了最大最小值，即如果sigmoid函数的最小值比1e-8小，只会输出1e-8；而比1 - (1e-8)大，则只输出1 - (1e-8)
  return np.clip(1 / (1.0 + np.exp(-z)), 1e-8, 1 - (1e-8))


def _f(x, w, b):
  return _sigmoid(np.dot(w,x.T) + b)




# 更新参数，训练模型
def train(x_train, y_train, epoch):
  """
  x_train, y_train: 训练集数据
  epoch: 训练次数
  """
  num = x_train.shape[0]
  dim = x_train.shape[1]
  bias = 0 # 初始化偏置值b
  weights = np.ones((1,dim)) # 权重w初始化
  learning_rate = 1 # 初始化学习率
  reg_rate = 0.01  # 正则系数
  bg2_sum = 0  # 用于存放偏置值的梯度平方和
  wg2_sum = np.zeros((1,dim)) # 用于存放权重的梯度平方和

  for i in range(epoch):
    b_g = 0
    w_g = np.zeros((1,dim))
    # 在所有数据上计算梯度，梯度计算时针对损失函数求导
    for j in range(num):
      y_pred = _f(x_train[j:j+1, :], weights, bias)
      pred_error = y_train[j] - y_pred
      b_g += (-1) * pred_error
      
      w_g += (-1) * pred_error * x_train[j:j+1, :] + 2 * reg_rate * weights

    # 更新参数，自适应学习率
    b_g /= num
    w_g /= num

    # 学习率计算 adagrad
    bg2_sum += b_g ** 2
    wg2_sum += w_g ** 2  
    # 更新权重w和偏置值b
    bias -= learning_rate / bg2_sum**0.5 * b_g
    weights -= learning_rate / wg2_sum**0.5 * w_g
  
    # 输出预测效果
    if i % 1 == 0:
      correctNumber = 0
      forecastResult = np.zeros(num)
      for j in range(num):
        sig = _f(x_train[j:j+1, :], weights, bias)
        if sig >= 0.5:
          forecastResult[j] = 1
        else:
          forecastResult[j] = 0

        if forecastResult[j] == y_train[j]:
          correctNumber += 1  
      print('{}轮后准确率为:'.format(i),correctNumber/num)   
  
  return weights, bias



def main():
  x_train_data = pd.read_csv('./data/X_train')
  y_train_data = pd.read_csv('./data/Y_train')
  x = x_train_data.iloc[:,1:]
  y = y_train_data.iloc[:,1:]
  x_array = np.array(x)
  y_array = np.array(y)
  # print(x_array,y_array)
  # 划分训练集与验证集, 90%训练集，90%个验证集
  x_train, y_train = x_array[0:48830], y_array[0:48830]
  # print(x_train.shape, y_train.shape)
  # x_val, y_val = x[43404:54256], y[43404:54256]


  epoch = 300 #训练轮数

  # 开始训练
  w, b = train(x_train, y_train, epoch)

  # 保存结果
  np.save('./weight/weight.npy', w)
  np.save('./bias/bias.npy', b)

if __name__ == "__main__":
  main()