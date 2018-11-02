# -*- coding: utf-8 -*-
from ml.arith.qy.dtree.tree import *
from ml.arith.qy import *

# 绘图
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
def createPlotTest():
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    ax1 = plt.subplot(111, frameon=False)
    ax1.annotate("sdasdasd", xy=(0.1,0.5), xycoords='axes fraction', xytext=(0.5,0.5),
                            textcoords='axes fraction', va="center", ha="center", bbox=decisionNode,
                            arrowprops=arrow_args)
    plt.show()

def plotNode(nodeTxt, starNode, textNode, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=starNode, xycoords='axes fraction', xytext=textNode,
                            textcoords='axes fraction', va="center", ha="center", bbox=nodeType,
                            arrowprops=arrow_args)

# 创建树 同createTree
def retrieveTree(i):
    listOfTree=[{'no suerfacing':{0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                {'no suerfacing':{0:'no', 1:{'flippers':{
                    0:{'head':{0:'no', 1:'yes'}}, 1:'no'}}}}]
    return listOfTree[i]

# 绘制线上的标记 比如 0,1
def plotMidText(cntrPt, parentPt, txtString):
    xMid= (parentPt[0]-cntrPt[0])/2.0 +cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 +cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

# 绘制树形图
def plotTree(myTree, parentPt, nodeTxt):
    numberLeafs = getNumerLeafs(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0+float(numberLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, parentPt, cntrPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], cntrPt, (plotTree.xOff, plotTree.yOff), leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)#  **axprops
    plotTree.totalW = float(getNumerLeafs(inTree))   # 树的宽度    用于计算放置判断结点的位置
    plotTree.totalD = float(getTreeDepth(inTree))    # 树的深度
    plotTree.xOff = -0.5/plotTree.totalW       # 追踪已经绘制的结点位置
    plotTree.yOff = 1.0                        # 放置下一个结点的位置
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

if __name__ == "__main__":
    dataSet, labels = createDataSet()
    myTree = retrieveTree(1)
    createPlot(myTree)
