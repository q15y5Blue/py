# -*- coding: utf-8 -*-
# 优点 计算代价不高，容易理解和实现
# 缺点： 容易欠拟合 分类精度可能不高
# 数值型 标称型数据都能用
from numpy import *
import matplotlib.pyplot as plt

def loadDataSet():
    dataMat =[];labelMat=[]
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

# 梯度上升
# 每次更新回归系数的时候都需要遍历整个数据集
def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)   # numpy矩阵
    labelMat = mat(classLabels).transpose()   # 转换为numpy矩阵数据类型
    m,n = shape(dataMatIn)
    alpha = 0.001 # 步长
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat-h)
        weights = weights +alpha * dataMatrix.transpose()*error
    return weights

# 随机梯度上升算法
def randGradAscent(dataMatrix, classLabels,numerIter=150):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for j in range(numerIter):   #添加迭代
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.01
            randIndex = int(random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            # del(dataIndex[randIndex])
    return weights


def plotBestFit(wei):
    # weights = wei.getA() # return self as an ndarray obj
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 =[]; ycord1 = []
    xcord2 =[]; ycord2 = []
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else :
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

if __name__=='__main__':
    dataArr, labelMat = loadDataSet()
    # weights= gradAscent(dataArr, labelMat)
    # 迭代后的随机梯度上升
    weights = randGradAscent(array(dataArr), labelMat, 100)
    plotBestFit(weights)