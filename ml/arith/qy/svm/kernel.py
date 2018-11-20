# coding:utf-8
# 核函数 将数据映射到高维空间
import numpy as np

from numpy import *
# （高斯）径向基函数核（英语：Radial basis function kernel），或称为RBF核。是一种常用的核函数。

def loadDataSet(fileName):
    DataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        DataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return mat(DataMat), mat(labelMat).transpose()

def kernelTrans(X,A,kTup):
    m,n = shape(X)
    K = mat(zeros((m,1)))
    if kTup[0]=='lin': K = X*A.T
    elif kTup[0]=='rbf':
        for j in range(m):
            deltaRow = X[j,:]-A
            K[j] = deltaRow*deltaRow.T
        K = exp(K/(-1*kTup[1]**2))
    else:raise NameError("Houston We have a Problem that Kernel is not recognized")
    return K

def testRbf(k1=1.3):
    from ml.arith.qy.svm.svmarith import SMO
    dataMat,labelMat = loadDataSet('../data/svm/testSetRBF.txt')
    smo = SMO()
    smo.C = 200
    smo.tol = 0.0001
    b, alphas =smo.smoP(10000,('rbf',k1))
    svInd = nonzero(alphas.A>0)[0]
    sVs = dataMat[svInd]
    labelSV = labelMat[svInd]
    print("there are %d Support Vectores "%shape(sVs)[0])
    m,n = shape(dataMat)
    errorCount = 0
    for i in range(m):
        kernelEval = kernelTrans(sVs,dataMat[i,:],('rbf',k1))
        predict = kernelEval.T * multiply(labelSV,alphas[svInd])+b
        if sign(predict)!= sign(labelMat[i]):errorCount +=1 ##difff
    print("the training error rate is :%f"%(float(errorCount/m)))

    dataMat,labelMat = loadDataSet("../data/svm/testSetRBF2.txt")
    errorCount= 0
    m,n = shape(dataMat)
    for i in range(m):
        kernelEval = kernelTrans(sVs, dataMat[i,:],('rbf',k1))
        predict = kernelEval.T * multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelMat[i]):
            errorCount +=1
    print("the test Error rate is %f "%float(errorCount/m))


if __name__=='__main__':
    testRbf()