# decision Tree
# 决策树 适合用于离散型数据 1,判定数据集的无序程度(信息熵) 2,划分数据集
# 信息熵 entropy : 信息的期望值       平均信息量, 度量集合无序程度的方法
# entropy越高,则混合的数据也就越多,
# 方法二: 基尼不纯度(Gini impurity)
from math import log

def createDataSet():
    dataSet = [[1, 1, 'maybe'], [1, 1, 'yes'], [1, 1, 'yes'], ['1', '0', 'no'], [0, 1, 'no'], [0, 1, 'no']]
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
def splitDataSet(dataSet, axis, value):
    retData = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retData.append(reducedFeatVec)
    print(retData)
    return retData

# 选择最好的数据集划分方法
def chooseBestFeatureToSplit(dataSet):
    numberFreature = len(dataSet[0])-1
    baseEntropy = calEntropy(dataSet)
    bestInfoGain = 0.0;
    bestFeature = -1;
    for i in range(numberFreature):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
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


if __name__ == "__main__":
    dataSet, labels = createDataSet()
    print(chooseBestFeatureToSplit(dataSet))