# coding:utf-8
# AdaBoost(adaptive boosting)自适应
# 集成学习: meta-algorithm // ensembel method 元算法/对其他算法进行组合 对不同分类器进行聚合
# 优点：泛化错误率低，易编码。可以应用在大部分分类器上，无参数调整
# 缺点：对离群点敏感
# 适用数据类型：数值型和标称型数据
from numpy import *

def loadSimpData():
    datMat = matrix([[1., 2.1],
                     [2., 1.1],
                     [1.3, 1.],
                     [1., 1.],
                     [2., 1.]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat, classLabels

def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t'))
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():#
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat


# this is always the Fei G
# 用于测试是否有某个小鱼或大于我们正在测试的阈值,淘工作最大最小分类
def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):  # just classify the data
    retArray = ones((shape(dataMatrix)[0], 1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:, dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:, dimen] > threshVal] = -1.0
    return retArray

# 遍历stumpClassify()所有可能输入值,并找到具有最低错误率的单层决策树
def buildStump(dataArr, classLabels, D):
    dataMatrix = mat(dataArr)
    labelMat = mat(classLabels).transpose()
    m, n = shape(dataMatrix)
    numSteps = 10.0     # 在特征的所有可能只上进行遍历
    bestStump = {}
    bestClasEst = mat(zeros((m, 1)))
    minError = inf      # init error sum, to + infinity
    for i in range(n):  # loop over all dimensions
        rangeMin = dataMatrix[:, i].min()
        rangeMax = dataMatrix[:, i].max()
        stepSize = (rangeMax - rangeMin) / numSteps
        for j in range(-1, int(numSteps) + 1):  # loop over all range in current dimension
            for inequal in ['lt', 'gt']:        # go over less than and greater than
                threshVal = (rangeMin + float(j) * stepSize)
                predictedVals = stumpClassify(dataMatrix, i, threshVal, inequal)  # call stump classify with i, j, lessThan
                errArr = mat(ones((m, 1)))
                errArr[predictedVals == labelMat] = 0
                weightedError = D.T * errArr  # calc total error multiplied by D
                # print("split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError))
                if weightedError < minError:
                    minError = weightedError
                    bestClasEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump, minError, bestClasEst


# 基于单层决策树的AdaBoost训练过程
def adaBoostTrainDS(dataArr, classLabels, numIt= 40):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)# D数据点的权重,一开始,权重相等,算法会在增加错分数据的权重的同事,降低正确分类数据的权重
    aggClassEst = mat(zeros((m,1)))# aggClassEst 记录每个数据点的类别估计累计值
    for i in range(numIt):
        bestStump, error, classEst = buildStump(dataArr,classLablels,D)
        print("D:", D.T)
        alpha = float(0.5*log((1.0-error)/max(error, 1e-16)))# alpha: 表示总分类器本层决策树输出结果的权重
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print("classEst: ", classEst.T)
        expon = multiply(-1*alpha*mat(classLablels).T, classEst)
        D = multiply(D, exp(expon))
        D = D/D.sum()
        aggClassEst += alpha*classEst
        print("aggClassEst : ", aggClassEst.T)
        aggErrors = multiply(sign(aggClassEst) != mat(classLablels).T, ones((m ,1)))
        errorRate = aggErrors.sum()/m
        print("total error: ", errorRate, "\n")
        if errorRate == 0.0:break
    return weakClassArr

# 利用训练出的多个弱分类器进行分类
def adaClassify(datToclass,classifierArr):
    dataMatrix = mat(datToclass)
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst =stumpClassify(dataMatrix,classifierArr[i]['dim'],
                                classifierArr[i]['thresh'],classifierArr[i]['ineq'])
        aggClassEst += classifierArr[i]['alpha']*classEst
        print(aggClassEst)
    return sign(aggClassEst)

if __name__ == "__main__":
    D = mat(ones((5, 1))/5)
    dataMat, classLablels = loadSimpData()
    # bestStump, minError, bestClassEst = buildStump(dataMat, classLablels, D)
    classifierArray = adaBoostTrainDS(dataMat,classLablels, 30)
    adaClassify([[5,5],[0,0]],classifierArr=classifierArray)