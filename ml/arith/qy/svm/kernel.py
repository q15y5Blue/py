# coding:utf-8
# 核函数 将数据映射到高维空间
import numpy as np
from numpy import *

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
