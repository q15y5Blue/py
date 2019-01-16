# coding:utf-8
# 当数据拥有众多特征并且特征之间的关系十分复杂时,构建全局模型的想法就不行
# 所以不能使用全局线性模型来拟合任何数据
# 解决: 1, 将数据集切分城很多份易建模数据,然后使用线性回归建模
#      2, 树结构:如果首次切分后仍然难以拟合线性模型,再次继续切分
from numpy import *
import numpy as np

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)    # 将每行映射成浮点数
        dataMat.append(fltLine)
    return dataMat


# CART(classification And Regression Trees 分类回归树)
def chooseBeatSplit(dataSet, leafType, errType, ops):
    pass

def regLeaf():
    pass

def regErr():
    pass

class TreeNode(object):
    def __init__(self,feat, val, right, left):
        self.featureToSplitOn = feat
        self.valueOfSplit = val
        self.rightBranch = right
        self.leftBranch = left

    def bindSplitDataSet(self,dataSet, feature, value):
        mat0 = dataSet[nonzero(dataSet[:, feature] > value)[0], :][0]
        mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :][0]
        return mat0, mat1

    def createTree(self, dataSet,leafType=regLeaf, errType=regErr, ops=(1, 4)):
        feat, val = chooseBeatSplit(dataSet, leafType, errType, ops)
        if feat == None: return val
        retTree = {}
        retTree['spInd'] = feat
        retTree['spVal'] = val
        lSet, rSet = self.bindSplitDataSet(dataSet,feat,val)
        retTree['left'] = self.createTree(lSet, leafType, errType, ops)
        retTree['right'] = self.createTree(rSet, leafType, errType, ops)
        return retTree