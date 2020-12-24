#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 清华源https://pypi.tuna.tsinghua.edu.cn/simple
# 参考：URL:https://www.cnblogs.com/HL-space/p/10676637.html
import numpy as np
import pandas as pd

def dataProcess(train_data):
  data = train_data.copy()
  x_list, y_list = [], []
  # 去除多余数据，只取有效数据
  data = data.iloc[:, 3:]
  # 特殊字符补零
  data[data == 'NR'] = 0
  # 转化为数组，等同于data.to_numpy()
  array = np.array(data).astype(float)
  # 将每一天数据差分成数据帧（18，9）,一天24小时能分成15份,(0-8,9)(1-9,10)....(14-22,23)
  for i in range(0, 4320, 18):
    for j in range(15):
      mat = array[i:i+18, j:j+9]
      # print(mat.shape)
      label = array[i+9,j+9]   # 第10行为PM2.5的数值
      x_list.append(mat)
      y_list.append(label)
  x = np.array(x_list)   # x.shape -- (3600, 18, 9)  3600 = 15 * 240
  y = np.array(y_list)   # x.shape -- (3600, )

  return x, y, array

# 更新参数，训练模型
def train(x_train, y_train, epoch):
  """
  x_train, y_train: 训练集数据
  epoch: 训练次数
  """
  bias = 0 # 初始化偏置值b
  weights = np.ones(9) # 权重w初始化
  learnint_rate = 1 # 初始化学习率
  reg_rate = 0.01  # 正则系数
  bg2_sum = 0  # 用于存放偏置值的梯度平方和
  wg2_sum = np.zeros(9) # 用于存放权重的梯度平方和
  
  for i in range(epoch):
    b_g = 0  # b的偏微分
    w_g = 0  # w的偏微分
    for j in range(3200):
      b_g += (y_train[j] - weights.dot(x_train[j,9, :]) - bias )*(-1)
      w_g += (y_train[j] - weights.dot(x_train[j, 9, :])- bias ) * (-x_train[j, 9, :])
    b_g /= 3200
    w_g /= 3200

    # 加上正则系项
    for m in range(9):
      w_g[m] += reg_rate * weights[m]
    

    # 学习率计算 adagrad
    bg2_sum += b_g**2
    wg2_sum += w_g**2

    # 更新权重w和偏置值b
    bias -= learnint_rate / bg2_sum**0.5 * b_g
    weights -= learnint_rate / wg2_sum**0.5 * w_g

    # 每200轮输出一次训练集上的损失函数值
    if i % 200 == 0:
      loss = 0
      for j in range(3200):
        loss += (y_train[j] - weights.dot(x_train[j, 9, :]) - bias)**2 
      # print('损失函数值为:',loss/3200)
  return weights, bias


# 验证模型效果
def validate(x_val, y_val, weights, bias):
  """
  在验证集上验证模型的损失效果
  """
  loss = 0
  for i in range(400):
    loss += (y_val[i] - weights.dot(x_val[i, 9, :]) - bias)**2
  return loss / 400

def main():
  # “文件路径”和“文件编码格式”,‘big5’指的是繁体中文编码
  train_data = pd.read_csv('./data/train.csv', encoding = 'big5')
  x, y, _ = dataProcess(train_data)
  
  # 划分训练集与验证集, 3200个训练集，400个验证集
  x_train, y_train = x[0:3200], y[0:3200]
  x_val, y_val = x[3200:3600], y[3200:3600]

  epoch = 2000 #训练轮数

  weights, bias = train(x_train, y_train, epoch)

  # 在验证集上验证
  loss = validate(x_val, y_val, weights, bias)
  print('验证集的loss为:', loss)

if __name__ == "__main__":
    main()