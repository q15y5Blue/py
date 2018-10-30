# -*- coding: utf-8 -*-
#  词集模型：将每个词的出现与否当做一个特征，、词集模型
#  词袋模型：一个词在文本中出现的不止一次
#  词集模型中，每个词只能表现为出现一次，词袋模型每个词可以出现多次。
from ml.arith.qy import *

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

# 创建一个包含在所有文档中出现的不重复词的列表,
# 返回单词列表
def createVocabList(dataSet):
    vocabSet = set([])
    for doc in dataSet:
        vocabSet = vocabSet | set(doc)  # this |  按位或 用于求两个集合的并集,在数学符号表示上,按位或昱集合求并用相同记号
    return list(vocabSet)

# 返回Vec，one-hot方法
# 词集模型
def setOfWord2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            # vocabList.append(word)
            print("the word %s is not in my Vocabulary") % (word)
    return returnVec

# 词袋模型
def bagOfWord2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec

# 计算概率
# trainMaxtrix 文档矩阵,    trainCategory每篇文档标签所构成的向量.
def trainNB01(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix) # 文档矩阵长度
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    # p0Num = zeros(numWords)
    # p1Num = zeros(numWords)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    # p0Denom = 0.0
    # p1Denom = 0.0
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = np.log(p1Num/p1Denom)   #p1Num/p1Denom 之所以使用log函数是为了避免 多个小数相乘四舍五入为0
    p0Vect = np.log(p0Num/p0Denom)  #同上 np math log()冲突会出错
    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify*p1Vec) + log(pClass1)
    p0 = sum(vec2Classify*p0Vec) + log(1-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

def testingNB01():
    listOPosts ,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWord2Vec(myVocabList, postinDoc))
    trainMat = array(trainMat)
    listClasses = array(listClasses)
    # 已经迅雷好的模型
    p0V,p1V,pAb = trainNB01(trainMat, listClasses)
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWord2Vec(myVocabList, testEntry))
    print(classifyNB(thisDoc, p0V, p1V, pAb))

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\w*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]


def spamTest():
    docList = [];classList =[]; fullTest=[]
    for i in range(1,26):
        strByte = open("../data/bayes/email/spam/%d.txt" % i, encoding='mac_roman').read()
        wordList = textParse(strByte)
        docList.append(wordList)
        fullTest.extend(wordList)
        classList.append(1)# 垃圾信息
        wordList= textParse(open("../data/bayes/email/ham/%d.txt" %i, encoding='mac_roman').read())
        docList.append(wordList)
        fullTest.extend(wordList)
        classList.append(0)# 非垃圾信息
    vocabList = createVocabList(docList)
    trainingSet = list(range(50)); testSet=[]

    # 留存交叉验证
    # 随机删除list中的十个item
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(bagOfWord2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB01(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVec = bagOfWord2Vec(vocabList, docList[docIndex])
        if(classifyNB(array(wordVec), p0V, p1V, pSpam)) != classList[docIndex]:
            errorCount += 1
    print("errorCount:", float(errorCount)/len(testSet))

# there is a question that is called the name of Nick
if __name__=='__main__':
    # testingNB()
    spamTest()