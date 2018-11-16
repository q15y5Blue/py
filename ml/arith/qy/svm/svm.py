# coding:utf-8
# SVM泛华错误率低，计算开销小，结果易解释
# 缺点：对于参数调节和核函数的选择敏感，原始分类器不加修改仅适用于二分类问题。
# 数据类型：数值、 标称型数据
# separating隔 hyperplane超平面 margin间隔
# 希望找到离分割超平面最近的点，确保他们离分割面的距离尽可能远（margin :点到分割面距离）
# argmax(min(lable*(W^T+b))/|W|)
import time
import random
import numpy as np
from numpy import *
from .kernel import kernelTrans
fileName = '../data/svm/testSet.txt'
# Sequential Minimal Optimization 序列最小优化
class SMO(object):
    # 修改后的Platt SMO
    def __init__(self, C=None, toler=None,kTup=None):
        self.X, self.labelMat = self.loadDataSet()
        self.C = C if C is not None else 0.6
        self.tol = toler if toler is not None else 0.001
        self.m = self.X.shape[0]
        self.alphas = mat(zeros((self.m, 1)))
        self.b = 0
        self.eChache = mat(zeros((self.m, 2)))  # 误差缓存
        self.K = mat(zeros((self.m,self.m)))
        self.kTup = ('lin',0) if kTup is None else kTup
        for i in range(self.m):
            self.K[:,i] =kernelTrans(self.X,self.X[i,:], self.kTup)

    def calcEk(self, k):
        fXk = float(multiply(self.alphas,self.labelMat).T*(self.X*self.X[k,:].T))+self.b
        Ek = fXk - float(self.labelMat[k])
        return Ek

    def selectJ(self,i,Ei):
        maxK = -1; maxDeltaE = 0; Ej = 0
        self.eChache[i] = [1,Ei]
        validEcacheList = nonzero(self.eChache[:, 0].A)[0]
        if(len(validEcacheList))>1:
            for k in validEcacheList:
                if k== i:continue
                Ek = self.calcEk(k)
                deltaE = abs(Ei-Ek)
                if (deltaE>maxDeltaE):
                    maxK = k
                    maxDeltaE= deltaE
                    Ej = Ek
            return maxK,Ej
        else:
            j = selectJrand(i, self.m)
            Ej = self.calcEk(j)
        return j,Ej

    def updateEk(self, k):
        Ek = self.calcEk(k)
        self.eChache[k] = [1, Ek]

    # 内循环
    def innerL(self,i):
        Ei = self.calcEk(i)
        if (self.labelMat[i]*Ei<-self.tol and self.alphas[i]<self.C) or (self.labelMat[i]*Ei>self.tol and self.alphas[i]>0):
            j,Ej = self.selectJ(i,Ei)
            alphaIold = self.alphas[i].copy()
            alphaJold = self.alphas[j].copy()
            if (self.labelMat[i]!= self.labelMat[j]):
                L = max(0,self.alphas[j]-self.alphas[i])
                H = min(self.C,self.C+self.alphas[j]-self.alphas[i])
            else:
                L = max(0,self.alphas[j]+self.alphas[i]-self.C)
                H = min(self.C, self.alphas[j]+self.alphas[i])
            if L==H:
                # print("L==H")
                return 0
            eta = 2.0*self.X[i,:]*self.X[j,:].T-self.X[i,:]*self.X[i,:].T-self.X[j,:]*self.X[j,:].T
            if eta>=0:
                # print("eta<=0")
                return 0
            self.alphas[j] -= self.labelMat[j]*(Ei-Ej)/eta
            self.alphas[j]  = clipAlpha(self.alphas[j],H,L)
            self.updateEk(j)
            if (abs(self.alphas[j])-alphaJold<0.00001):
                # print("j not moving enough")
                return 0
            self.alphas[i] += self.labelMat[j]*self.labelMat[i]*(alphaJold-self.alphas[j])
            self.updateEk(i)
            b1 = self.b - Ei - self.labelMat[i]*(self.alphas[i]-alphaIold)*self.X[i,:]*self.X[i,:].T -\
                 self.labelMat[j]*(self.alphas[j]-alphaJold)*self.X[i,:]*self.X[j,:].T
            b2 = self.b - Ej- self.labelMat[i]*(self.alphas[i]-alphaIold)*self.X[i,:]*self.X[j,:].T -\
                 self.labelMat[j]*(self.alphas[j]-alphaJold)*self.X[j,:]*self.X[j,:].T
            if (0<self.alphas[i]) and (self.C>self.alphas[i]):
                self.b = b1
            elif (0<self.alphas[j]) and self.C>self.alphas[j]:
                self.b = b2
            else:
                self.b = (b1+b2)/2.0
            return 1
        else:
            return 0

    def smoP(self,maxIter, kTup=('lin',0)):
        iter = 0
        entireSet =True; alphaPairsChanged = 0
        while(iter<maxIter) and (alphaPairsChanged>0 or entireSet):
            alphaPairsChanged = 0
            if entireSet:
                for i in range(self.m):
                    alphaPairsChanged += self.innerL(i)
                print("fullSet ,iter :%d i:%d , pairs changed %d"%(iter,i,alphaPairsChanged))
                iter +=1
            else:
                nonBoundIs = nonzero((self.alphas.A>0)*(self.alphas.A<self.C))[0]
                for i in nonBoundIs:
                    alphaPairsChanged += self.innerL(i)
                    print("non-bound , iter : %d i: %d, pairs changed %d"%(iter,i,alphaPairsChanged))
                iter +=1
            if entireSet:entireSet=False
            elif(alphaPairsChanged==0):entireSet=True
            print("iteration number:%d"%iter)
        return self.b,self.alphas

    # Common
    def loadDataSet(self):
        DataMat = []; labelMat= []
        fr = open(fileName)
        for line in fr.readlines():
            lineArr = line.strip().split('\t')
            DataMat.append([float(lineArr[0]),float(lineArr[1])])
            labelMat.append(float(lineArr[2]))
        return mat(DataMat), mat(labelMat).transpose()

    # b, alphas = smo.smoSimple(dataMat, labelMat, 0.6, 0.001, 40)
    # for i in range(100):
    #     if alphas[i] > 0.0:
    #         print(dataMat[i], labelMat[i])
    # 简化版的SMO算法  数据集，标签集，常数C,容错率，取消前最大的循环次数 test function upstairs
    def smoSimple(self,dataMatIn,classLabels,maxIter):
        dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
        b = 0; m, n=shape(dataMatrix)
        alphas = mat(zeros((m,1)))  # 创建一个alpha向量并将其初始化为0向量
        iter = 0
        while(iter<maxIter):  # 迭代循环
            alphaPairsChanged = 0  # 用来记录alpha是否已经进行了优化
            for i in range(m):  # 选择数据集中的每个数据向量
                fXi  =float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T))+b
                Ei = fXi - float(labelMat[i])
                if ((labelMat[i]*Ei< -self.tol) and (alphas[i]<self.C)) or ((labelMat[i]*Ei>self.tol) and (alphas[i]>0)): # 如果此向量可以被优化
                    j = selectJrand(i,m)  # 随机选取另一个数据向量
                    fXj = float(multiply(alphas, labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                    Ej = fXj - float(labelMat[j])
                    alphaIold = alphas[i].copy()
                    alphaJold = alphas[j].copy()
                    if (labelMat[i]!=labelMat[j]):
                        L = max(0,alphas[j]-alphas[i])
                        H = min(self.C, self.C + alphas[j] - alphas[i])
                    else:
                        L = max(0, alphas[j]+ alphas[i] - self.C)
                        H = min(self.C, alphas[j]+ alphas[i])
                    if L == H:
                        # print("L==H")
                        continue;
                    eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T-dataMatrix[j,:]*dataMatrix[j,:].T
                    if eta >=0:
                        # print("rta>=0")
                        continue
                    alphas[j] -= labelMat[j]*(Ei-Ej)/eta
                    alphas[j]  = clipAlpha(alphas[j],H,L)
                    if (abs(alphas[j])-alphaJold)<0.00001:
                        # print("j not moving enough")
                        continue
                    alphas[i] += labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                    b1 = b - Ei - labelMat[i]*(alphas[i]-alphaJold)*dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                    b2 = b - Ej - labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                    if (0<alphas[i]) and (self.C>alphas[i]):
                        b = b1
                    elif (0<alphas[i]) and (self.C>alphas[i]):
                        b=b1
                    else:
                        b = (b1+b2)/2.0
                    alphaPairsChanged +=1
                    # print("iter:%d i :%d ,pairs changed %d"%(iter,i,alphaPairsChanged))
            if (alphaPairsChanged==0):iter+=1
            else: iter=0
            print("iteration number :%d"%iter)
        return b,alphas


    # 辅助函数：用于在某个区间内随机选择一个非i整数
def selectJrand(i,m):
    j = i
    while (j==i):
        j = int(random.uniform(0,m))
    return j

# 用于数值过大的时候的调整
def clipAlpha(aj,H,L):
    if aj>H:
        aj =H
    if L>aj:
        aj =L
    return aj

if __name__=='__main__':
    # dataMat,labelMat = smo.loadDataSet(fileName)
    smo =SMO()
    smo.smoP(40)
    # print(smo.X)
