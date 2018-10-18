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
    for featVec in dataSet:
        if featVec[index] == value:
            reducedFeatVec = featVec[:index]
            reducedFeatVec.extend(featVec[index+1:])
            retData.append(reducedFeatVec)


    return retData


# 选择最好的数据集划分方法 计算 信息增益
# 对所有唯一的特征值得到的熵求和,
# 信息增益  是熵的减少或者数据无序度的减少            将信息增益数值最大的特征作为决策树的根节点
def chooseBestFeatureToSplit(dataSet):
    numberFreature = len(dataSet[0])-1  # 特征数2
    baseEntropy = calEntropy(dataSet)   # 计算整个数据集的原始香农熵
    bestInfoGain = 0.0;
    bestFeature = -1;
    for i in range(numberFreature):
        featureList = [example[i] for example in dataSet]
        uniqueVals = set(featureList)  # 特征去重
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

# 因为算法运行时并不是每次划分分组时都会消耗特征,(特征数并不是在每次互粉数据分组的时候都减少)
# 多数表决 法 决定叶子结点的分类
# me:返回出现频率最多的标签
def majorityCnt(labelList):
    classCount = {}
    for vote in labelList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote] +=1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True);
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    labelList = [ex[-1] for ex in dataSet]
    if labelList.count(labelList[0]) == len(labelList):   # 标签如果完全相同则停止继续划分
        return labelList[0]
    if len(dataSet[0]) == 1:                            # 遍历完所有特征时返回出现次数最多的
        return majorityCnt(labelList)
    bestFeatureIndex = chooseBestFeatureToSplit(dataSet)
    bestFeatureLabel = labels[bestFeatureIndex]
    myTree = {bestFeatureLabel:{}}
    del(labels[bestFeatureIndex])
    featureValues = [ex[bestFeatureIndex] for ex in dataSet]
    uniqueVals = set(featureValues)
    for va in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatureLabel][va] = createTree(splitDataSet(dataSet, bestFeatureIndex, va), subLabels)
    return myTree

# 为了绘制这个树,需要获取叶子结点的数目和树的层数
def getNumerLeafs(myTree):
    numerLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == "dict":
            numerLeafs += getNumerLeafs(secondDict[key])
        else:
            numerLeafs +=1
    return numerLeafs

# 获取树的深度
def getTreeDepth(myTree):
    numberDepth = 0
    firstKey = list(myTree.keys())[0]
    secondDict = myTree[firstKey]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numberDepth = 1 + getTreeDepth(secondDict[key])
        else:
            numberDepth = 1
    return numberDepth

# 决策树分类器,参数 :决策树 标签向量 测试向量
def classify(inputTree, featureLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featureIndex = featureLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featureIndex] == key:
            if type(secondDict[key]).__name__== 'dict':
                classLabel = classify(secondDict[key], featureLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

# pickle序列化决策树:
def storeTree(inputTree, fileName):
    import pickle
    fw = open(fileName)
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(fileName):
    import pickle
    fr = open(fileName)
    return pickle.load(fr)

if __name__ == "__main__":
    dataSet, labels = createDataSet()
    myTree = createTree(dataSet, labels)
    print(myTree)
    print(getTreeDepth(myTree))































