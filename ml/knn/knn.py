# -*- coding: utf-8 -*-
# 精度高 对异常值不敏感 无数据输入假定 缺点计算复杂度、空间复杂度高 数值型,标称型
from numpy import *
import operator


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify(inX, dataSet, lables, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet   # tile 将数组inX 重复N次
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1) # 矩阵行向量相加  axis＝0表示按列相加
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()# 将矩阵按照axis排序，并返回排序后的下标
    classCount = {}
    for i in range(k):
        voteIlable = lables[sortedDistIndicies[i]]
        classCount[voteIlable] = classCount.get(voteIlable, 0)+1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    file = open(filename)
    dataList = file.readlines()
    lineNumber = len(dataList)
    returnMat = zeros((lineNumber, 3))
    print(returnMat)
    classLabelVector = []
    index = 0
    for line in dataList:
        line = line.strip()
        listFromLine = line.strip("\t")
        returnMat[index,:] = listFromLine[0:3]
        print(returnMat)
        classLabelVector.append(int(listFromLine[-1]))
        index =index + 1
    return returnMat, classLabelVector


if __name__ == "__main__":
    filename = "./data/datingTestSet.txt"
    # group, lables= createDataSet()
    # result = classify([0.0, 0.0],group, lables, 3)
    # print(result)
    print(file2matrix(filename))