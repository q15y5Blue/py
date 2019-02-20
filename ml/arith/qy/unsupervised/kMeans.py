# coding:utf-8
from numpy import *
import random

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine))
        dataMat.append(fltLine)
    return dataMat

# 计算两个向量的欧氏距离 //距离函数
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


# 为给定数据集构建一个包含k个随机质心的集合. K要在数据集边界之内
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids


if __name__ == '__main__' :
    dataMat = mat(loadDataSet("./data/kmeans/testSet.txt"))
    # print(min(dataMat[:, 0]))
    randCent(dataMat, 2)
