# coding:utf-8
# SVM泛华错误率低，计算开销小，结果易解释
# 缺点：对于参数调节和核函数的选择敏感，原始分类器不加修改仅适用于二分类问题。
# 数据类型：数值、 标称型数据
# separating隔 hyperplane超平面 margin间隔
# 希望找到离分割超平面最近的点，确保他们离分割面的距离尽可能远（margin :点到分割面距离）
# argmax(min(lable*(W^T+b))/|W|)

import random
import numpy as np
from numpy import *
fileName = '../data/svm/testSet.txt'
# Sequential Minimal Optimization 序列最小优化
class SMO(object):
    def loadDataSet(self, file):
        DataMat = []; labelMat= []
        fr = open(fileName)
        for line in fr.readlines():
            lineArr = line.strip().split('\t')
            DataMat.append([float(lineArr[0]),float(lineArr[1])])
            labelMat.append(float(lineArr[2]))
        return DataMat, labelMat

    # 辅助函数：用于在某个区间内随机选择一个非i整数
    def selectJrand(self,i,m):
        j = i
        while (j==i):
            j = int(random.uniform(0,m))
        return j

    # 用于数值过大的时候的调整
    def clipAlpha(self,aj,H,L):
        if aj>H:
            aj =H
        if L>aj:
            aj =L
        return aj

    # 简化版的SMO算法  数据集，标签集，常数C,容错率，取消前最大的循环次数
    def smoSimple(self,dataMatIn,classLabels,C,toler,maxIter):
        dataMatrix = mat(dataMatIn); labelMat =mat (classLabels).transpose()
        b = 0; m, n=shape(dataMatrix)
        alphas = mat(zeros((m,1)))
        iter = 0
        while(iter<maxIter):
            alphaPairsChanged = 0
            for i in range(m):
                fXi  =float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T))+b
                Ei = fXi - float(labelMat[i])
                if ((labelMat[i]*Ei< -toler) and (alphas[i]<C)) or ((labelMat[i]*Ei>toler) and (alphas[i]>0)):
                    j = self.selectJrand(i,m)
                    fXj =  float(multiply(alphas, labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                    Ej = fXj - float(labelMat[j])
                    alphaIold = alphas[i].copy()
                    alphaJold = alphas[j].copy()
                    if (labelMat[i]!=labelMat[j]):
                        L = max(0,alphas[j]-alphas[i])
                        H = min(C, C + alphas[j] - alphas[i])
                    else:
                        L = max(0, alphas[j]+ alphas[i] - C)
                        H = min(C, alphas[j]+ alphas[i])
                    if L == H:
                        # print("L==H")
                        continue;
                    eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                    if eta >=0:
                        # print("rta>=0")
                        continue
                    alphas[j] -= labelMat[j]*(Ei-Ej)/eta
                    alphas[j]  = self.clipAlpha(alphas[j],H,L)
                    if (abs(alphas[j])-alphaJold)<0.00001:
                        # print("j not moving enough")
                        continue
                    alphas[i] += labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                    b1 = b - Ei - labelMat[i]*(alphas[i]-alphaJold)*dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                    b2 = b - Ej - labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                    if (0<alphas[i]) and (C>alphas[i]):
                        b = b1
                    elif (0<alphas[i]) and (C>alphas[i]):
                        b=b1
                    else:
                        b = (b1+b2)/2.0
                    alphaPairsChanged +=1
                    # print("iter:%d i :%d ,pairs changed %d"%(iter,i,alphaPairsChanged))
            if (alphaPairsChanged==0):iter+=1
            else:iter=0
            print("iteration number :%d"%iter)
        return b,alphas

if __name__=='__main__':
    smo = SMO()
    dataMat,labelMat = smo.loadDataSet(fileName)
    b,alphas = smo.smoSimple(dataMat,labelMat,0.6,0.001,40)
    # print(b)
    # print(alphas[alphas>0])
    for i in range(100):
        if alphas[i]>0.0:
            print(dataMat[i], labelMat[i])