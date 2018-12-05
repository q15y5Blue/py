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
    if kTup[0] =='lin': K = X*A.T
    elif kTup[0]=='rbf':
        for j in range(m):
            deltaRow = X[j, :] - A
            K[j] = deltaRow*deltaRow.T
        K = exp(K/(-1*kTup[1]**2))
    else:
        raise NameError("Houston We have a Problem that Kernel is not recognized")
    return K
# 但是

def testRbf(k1=0.1):
    from ml.arith.qy.svm.svmarith import SMO
    X, labelMat = loadDataSet('../data/svm/testSetRBF.txt')
    smo = SMO(C=200, toler=0.0001, X=X,labelMat=labelMat)
    smo.smoP(10000, ('rbf',k1))# get b and alphas
    svInd = nonzero(smo.alphas.A >0)[0]
    sVs = smo.X[svInd]
    labelSV = smo.labelMat[svInd]
    print("there are %d Support Vectores "%shape(sVs)[0])
    errorCount = 0
    for i in range(smo.m):
        kernelEval = kernelTrans(sVs,smo.X[i, :],('rbf',k1))
        predict = kernelEval.T * multiply(labelSV,smo.alphas[svInd])+smo.b
        if sign(predict)!= sign(smo.labelMat[i]):errorCount += 1 ##difff
    print("the training error rate is :%f" %(float(errorCount/smo.m)))

    smo.X, smo.labelMat = loadDataSet("../data/svm/testSetRBF2.txt")
    errorCount= 0
    for i in range(smo.m):
        kernelEval = kernelTrans(sVs, smo.X[i, :],('rbf',k1))
        predict = kernelEval.T * multiply(labelSV, smo.alphas[svInd])+smo.b
        if sign(predict)!=sign(smo.labelMat[i]):
            errorCount +=1
    print("the test Error rate is %f "%float(errorCount/smo.m))


if __name__=='__main__':
    testRbf()