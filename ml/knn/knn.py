# -*- coding: utf-8 -*-
# 精度高 对异常值不敏感 无数据输入假定 缺点计算复杂度、空间复杂度高 数值型,标称型
from ml.knn import *


# FirstStep
# group, lables= createDataSet()
# result = classify([0.0, 0.0],group, lables, 3)
# print(result)
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
    returnMat = zeros((lineNumber, 3))  # 创建以0填充的矩阵
    classLabelVector = []
    index = 0
    for line in dataList:
        line = line.strip()
        listFromLine = line.split("\t")
        returnMat[index, :] = listFromLine[0:3]  # 前三个数据
        classLabelVector.append(defineLike(listFromLine[-1]))
        index+= 1
    return returnMat, classLabelVector

def defineLike(like):
    if like == 'smallDoses':
        return 1
    elif like =='largeDoses':
        return 2
    elif like == 'didntLike':
        return 0

# matplotlib
def showFigure1(datingDataMat, datingLables):
    figure = plt.figure()
    ax1 = figure.add_subplot(211)
    ax2 = figure.add_subplot(212)
    ax1.set(ylabel="冰激凌公斤数", xlabel="玩游戏所耗时间占总时间百分比", title="关系图1")
    ax2.set(ylabel="玩视频游戏占时间百分比", xlabel="飞行里程数", title="关系图2")
    ax1.scatter(datingDataMat[:, 1],datingDataMat[:, 2],
                15.0 * array(datingLables), 15.0 * array(datingLables) )
    ax2.scatter(datingDataMat[:, 0], datingDataMat[:, 1],
               15.0 * array(datingLables), 15.0 * array(datingLables))
    plt.show()


if __name__ == "__main__":
    filename = "./data/datingTestSet.txt"
    datingDataMat, datingLables = file2matrix(filename)
    showFigure1(datingDataMat, datingLables)
