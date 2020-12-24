import pandas as pd
import numpy as np
import csv
# Linear Regression
# 此方案在 index.py下改进
# 参考 https://mrsuncodes.github.io/2020/03/15/%E6%9D%8E%E5%AE%8F%E6%AF%85%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0-%E7%AC%AC%E4%B8%80%E8%AF%BE%E4%BD%9C%E4%B8%9A/#more


# 数据预处理,处理成（18，5760）shape的数据，18为18个特征，5760为数列
def dataProcess(raw_data):
    x_list, y_list = [], []
    month_data = np.zeros((18, 480*12))
    array = np.array(raw_data).astype(float)

    for month in range(12):  # month 从0-11 共12个月
      for day in range(20):  # day从0-19 共20天
          month_data[: , (month * 20 + day) * 24: (month * 20 + day+1)*24 ] = array[18 * (month * 20 + day): 18*(month * 20 + day + 1), :]

    # print(month_data.shape) # shape:(18,5760)

    # 继续处理
    for i in range(0, 5760):
      if i <= 5750:
        mat = month_data[:,i:i+9]
        label = month_data[9,i+9]
        x_list.append(mat)
        y_list.append(label)
    x = np.array(x_list)
    y = np.array(y_list)
    return x, y, month_data

# 更新参数，训练模型, 模型选择回归模型
def train(x_train, y_train, epoch):
  #初始化数据
  bias = 0
  weights = np.ones(9)
  learning_rate = 1 # 学习率
  reg_rate = 0.01 # 正则系数
  bg2_sum = 0  # 用于存放偏置值的梯度平方和
  wg2_sum = np.zeros(9)  # 用于存放权重的梯度平方和

  for i in range(epoch):
    b_g = 0  # b的偏微分
    w_g = 0  # w的偏微分
    for j in range(4600):
      b_g += (y_train[j] - weights.dot(x_train[j,9, :]) - bias )*(-1)
      w_g += (y_train[j] - weights.dot(x_train[j, 9, :])- bias ) * (-x_train[j, 9, :])
    b_g /= 4600
    w_g /= 4600

    # 加上正则系项
    for m in range(9):
      w_g[m] += reg_rate * weights[m]
    

    # 学习率计算 adagrad
    bg2_sum += b_g**2
    wg2_sum += w_g**2

    # 更新权重w和偏置值b
    bias -= learning_rate / bg2_sum**0.5 * b_g
    weights -= learning_rate / wg2_sum**0.5 * w_g


    # 每200轮输出一次训练集上的损失函数值
    if i % 200 == 0:
      loss = 0
      loss_reg = 0  # 正则项
      for j in range(4600):
        loss += (y_train[j] - weights.dot(x_train[j, 9, :]) - bias)**2 
      for w in range(9):
        loss_reg += weights[w]**2
      loss = (loss/4600 + reg_rate * loss_reg) / 2
      print('损失函数值为:',loss)
  return weights, bias


# 验证模型效果
def validate(x_val, y_val):
  w = np.load('./weight/weight2.npy')
  b = np.load('./bias/bias2.npy')
  print(w,b)
  loss = 0
  loss_reg = 0  # 正则项
  reg_rate = 0.01
  for i in range(1151):
    loss += (y_val[i] - w.dot(x_val[i, 9, :]) - b)**2 
  for j in range(9):
    loss_reg += w[j]**2
  loss = (loss/1151 + reg_rate * loss_reg) / 2

  return loss

# 预测test.csv
def forecast():
    x_test = []
    y_forecast = []
    w = np.load('./weight/weight2.npy')
    b = np.load('./bias/bias2.npy')
   # 读取数据
    test_data = pd.read_csv('./data/test.csv',header=None, encoding='big5')
    
    # 获取想要的数据
    test_data = test_data.iloc[:, 2:]
    # 无效数据清0
    test_data[test_data == 'NR'] = 0
    # 转化为二维数组
    array = np.array(test_data).astype(float)

    for i in range(0, 4320, 18):
      mat = array[i:i+18, :]
      x_test.append(mat)
    x = np.array(x_test)
    for i in range(240):
      label = w.dot(x[i, 9, :]) + b
      y_forecast.append(label)
    y = np.array(y_forecast)
    return y


# 写入 sample_submission.csv文件
def write_csv(resule_label):
  with open('./result/submit.csv', mode='w', newline='') as submit_file:
    csv_writer = csv.writer(submit_file)
    header = ['id', 'value']
    csv_writer.writerow(header)
    for i in range(240):
      row = ['id_' + str(i), resule_label[i]]
      csv_writer.writerow(row)

# 主函数
def main():
    
    # # 读取数据
    # data = pd.read_csv('./data/train.csv', encoding='big5')
    
    # # 获取想要的数据
    # data = data.iloc[:, 3:]

    # # 无效数据清0
    # data[data == 'NR'] = 0

    # # 转化为二维数组
    # raw_data = data.to_numpy()

    # # 数据预处理
    # x, y, _ = dataProcess(raw_data)

    # 将训练数据拆成训练数据：验证数据=8:2，这样用来验证
    # x_train, y_train = x[0:4600],y[0:4600]
    # x_val, y_val = x[4600:5751], y[4600:5751]
    # epoch = 10000 # 训练次数

    # weights, bias = train(x_train, y_train, epoch)

    # np.save("./weight/weight2.npy", weights)  # 将参数保存下来
    # np.save("./bias/bias2.npy", bias)

    # 验证数据集
    # loss = validate(x_val, y_val)
    # print('验证集的loss为:', loss)

    # 测试集test.csv 测试数据
    forecast_y = forecast()
    # 写入文件
    write_csv(forecast_y)

if __name__ == "__main__":
    main()