# decision Tree
# 决策树 适合用于离散型数据 1,判定数据集的无序程度(信息熵) 2,划分数据集
# 信息熵 entropy : 信息的期望值       平均信息量, 度量集合无序程度的方法
# entropy越高,则混合的数据也就越多,
# 方法二: 基尼不纯度(Gini impurity)
from ml.arith.qy import *

def createDataSet():
    dataSet = [[1, 1, 'maybe'], [1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
    labels = ['no suerfacing', 'flippers']
    return dataSet, labels


# 计算entropy 标签的熵
def calEntropy(dataSet):
    sizeData = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]= 0
        labelCounts[currentLabel]+= 1
    entropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]/sizeData)
        entropy -= prob*log(prob, 2)  # 以2为底求对数
    return entropy


# 2 按照给定的特征划分数据集
# dataSet数据集  axis划分数据集的特征   value特征的返回值
def splitDataSet(dataSet, index, value):
    retData = []
    # [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']
    for featVec in dataSet:
        if featVec[index] == value:
            reducedFeatVec = featVec[:index]
            reducedFeatVec.extend(featVec[index+1:])
            retData.append(reducedFeatVec)
    return retData

# 选择最好的数据集划分方法
def chooseBestFeatureToSplit(dataSet):
    numberFreature = len(dataSet[0])-1  # 特征数2
    baseEntropy = calEntropy(dataSet)
    bestInfoGain = 0.0;
    bestFeature = -1;
    for i in range(numberFreature):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)# 特征去重
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calEntropy(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote] +=1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True);
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    labelList = [ex[-1] for ex in dataSet]
    if labelList.count(labelList[0]) == len(labelList):
        return labelList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(labelList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [ex[bestFeat] for ex in dataSet]
    uniqueVals = set(featValues)
    for va in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][va] = createTree(splitDataSet(dataSet,bestFeat,va),subLabels)
    return myTree


if __name__ == "__main__":
    dataSet, labels = createDataSet()