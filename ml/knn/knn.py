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

# inX，待测试数据，DataSet，数据集，Labels 已知的标签，k
def classify(inX, dataSet, lables, k):
    dataSetSize = dataSet.shape[0]
    # print((dataSetSize, 1))
    # print(tile(inX, (dataSetSize, 1)))
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet   # tile 将数组inX 重复(x,1)次 变成x行一列的向量
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1) # 矩阵行向量相加  axis＝0表示按列相加
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()# 将矩阵按照axis排序，并返回排序后的下标
    classCount = {}
    for i in range(k):
        voteIlable = lables[sortedDistIndicies[i]]
        classCount[voteIlable] = classCount.get(voteIlable, 0)+1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

# 输入文件 返回数据向量和 标签向量
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


# 为了使数据归一化 newValue = (oldValue - min)/(max-min)
def autoNorm(dataSet):
    minValues  = dataSet.min(0)  # 获取每列最小的数字
    maxValues = dataSet.max(0)  # a.min(1)返回的是a的每行最小值
    ranges = maxValues - minValues
    normDataSet = zeros(shape(dataSet))
    dup = dataSet.shape[0]
    normDataSet = dataSet - tile(minValues, (dup, 1))
    normDataSet = normDataSet/tile(ranges, (dup, 1))
    return normDataSet, ranges, minValues

# 测试方法
def datingClassTest(fileName):
    hoRatio = 0.12 #测试集百分比
    datingDataMat, datingLabes = file2matrix(fileName)  # 数据和标签
    normMat, ranges, minValues = autoNorm(datingDataMat)  # 数据归一化
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)  # 测试数量
    errorCount  =0.0
    for i in range(numTestVecs):
        # 测试集  数据集 标签集 k
        classifierResult = classify(normMat[i, :], normMat[numTestVecs:m, :], datingLabes[numTestVecs:m], 3)
        if(classifierResult != datingLabes[i]):
            errorCount+=1.0
            print("分类器结果：%d实际结果:%d" % (classifierResult, datingLabes[i]))
    print("错误率:%f"%(errorCount/float(numTestVecs)))


# application of web
def classifyPerson(dataFileName):
    resultList = ['不喜欢', '有点喜欢', '很喜欢']
    percentTats = float(input("玩视频游戏的时间百分比"))
    ffMiles = float(input("每年飞行时间"))
    iceCream = float(input("冰激凌熟练每年"))
    datingDataMat ,dataLabels = file2matrix(dataFileName)
    normMat,ranges, minValues = autoNorm(datingDataMat)
    inputArray = array([ffMiles,percentTats,iceCream])
    classifierResult = classify((inputArray-minValues)/ranges, normMat, dataLabels, 3)
    print(resultList[classifierResult])

if __name__ == "__main__":
    filename = "./data/datingTestSet.txt"
    # datingClassTest(filename)
    classifyPerson(filename)