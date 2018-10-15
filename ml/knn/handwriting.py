# -*- coding: utf-8 -*-
# k-NN手写体项目
from ml.knn import *
from ml.knn.knn import classify

# reshape改变维度
# ravel 多维变一维
# flatten 同revel 不过flatten函数会请求分配内存来保存结果，而ravel函数只是返回数组的一个视图(view)
def img2Vec(filename):
    fileVec = img.imread(filename)
    reVec = fileVec.reshape(1, 784)
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
                continue
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
        print(result, "文件目录"+filePath)

if __name__=="__main__":
    print(testVecs("./data/training/", "./data/test/"))

