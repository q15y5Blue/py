# -*- coding: utf-8 -*-
# k-NN手写体项目
from ml.arith.qy import *
from ml.arith.qy.knn.knn import classify
from ml.arith.qy.svm.svmarith import SMO
from ml.arith.qy.svm.kernel import kernelTrans

# reshape改变维度
# ravel 多维变一维
# flatten 同revel不过flatten函数会请求分配内存来保存结果，而ravel函数只是返回数组的一个视图(view)
def img2Vec(filename):
    fileVec = img.imread(filename)
    reVec = fileVec.reshape((1, 784))
    return reVec

def getVecsLabels(path):
    labelList = []
    imgVecs = zeros((1, 784))
    pathList = listdir(path)
    for li in pathList: # type
        filePath = listdir(path+li)
        for label in filePath:
            pa = path+str(li)+'/'+label
            if (imgVecs == zeros((1, 784))).all():
                imgVecs = img2Vec(pa)
                labelList.append(int(li))
            else:
                vec = img2Vec(pa)
                imgVecs = np.vstack((imgVecs, vec))
                labelList.append(int(li))
    return imgVecs, labelList

def testVecs(dataPath, testPath):
    fileNames = listdir(testPath)
    dataSet,labelList = getVecsLabels(dataPath)
    for fileName in fileNames:
        filePath = testPath + fileName
        vec = img2Vec(filePath)
        result = classify(vec, dataSet, labelList, 3)
        print(result, "文件目录" +filePath)

# SVM是二分类算法，但是如果需要做多分类需要参考别的
# svm算法
def svmTest(kTup = ('rbf',10)):
    dataArr,labelArr = getVecsLabels("../data/training/")
    smo = SMO(C=200,toler=0.0001,kTup=('rbf',10))
    smo.smoP(10000)
    dataMat = mat(dataArr)
    labelMat = mat(labelArr).transpose()
    svInd = nonzero(smo.alphas.A>0)[0]
    sVs = dataMat[svInd]
    labelSV = labelMat[svInd]
    print("there are %d Support Vectors "% shape(sVs)[0])
    m,n = shape(dataMat)
    errorCount = 0
    for i in range(m):
        kernelEval = kernelTrans(sVs, dataMat[i,:],kTup)
        predic =kernelEval.T * multiply(labelSV,smo.alphas[svInd])+smo.b
        if sign(predic)!= sign(labelArr[i]):errorCount+=1
    print("the training error rate is :%f "%(float(errorCount/m)))

    dataMat,labelMat = getVecsLabels("../data/training/")
    errorCount = 0
    m,n = shape(dataMat)
    for i in range(m):
        kernelEval = kernelTrans(sVs, dataMat[i, :], kTup)
        predic = kernelEval.T * multiply(labelSV, smo.alphas[svInd]) + smo.b
        if sign(predic) != sign(labelArr[i]): errorCount += 1
    print("the test error rate is :%f " % (float(errorCount / m)))



if __name__=="__main__":
    #    testVecs("../data/training/", "../data/test/")
    svmTest()
