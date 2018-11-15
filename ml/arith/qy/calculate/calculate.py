# -*- coding: utf-8 -*-
# all of calculate
from numpy import *
import itertools
from itertools import permutations
from itertools import combinations
import numpy as np
def loadDataSet():
    alpha = np.array([[0.83,0.12,0.42,0.53,0.22],
                  [0.73,0.23,0.39,0.65,0.34],
                  [0.77,0.27,0.41,0.77,0.35],
                  [0.95,0.02,0.32,0.67,0.42],
                  [1.0,0.0,0.43,0.53,0.35],
                  [0.76,0.35,0.44,0.37,0.57],
                  [0.69,0.28,0.53,0.71,0.30],
                  [0.67,0.34,0.41,0.62,0.18]])
    beta = np.array([[0.70,0.86,0.44,0.30,0.70,0.61,0.63,0.38],
                 [0.89,0.80,0.22,0.12,0.81,0.55,0.67,0.70],
                 [0.61,0.92,0.54,0.19,1.0,0.51,0.68,0.43],
                 [0.82,0.63,0.27,0.49,0.59,0.87,0.69,0.61],
                 [0.86,0.76,0.30,0.0,0.46,0.70,0.66,0.20]])
    return alpha, beta  #  n8 m5

def subjectTo(alpha, beta):
    alphaOnes = zeros(alpha.shape)
    n, m = alphaOnes.shape
    rs = zeros((n, m))
    for i in range(0, n):
        for j in range (0, m):
            temp = zeros((n, m))
            temp[i][j]=1
            print(temp)

def getAllparam(arrayy):
    row, col = arrayy.shape
    vect = zeros((row,col))
    baseList = getChose(col)
    rowsList = []


def getChose(col):
    list = []
    for index in range(-1, col):
        arr = np.zeros((col))
        if index is not-1:
            arr[index] = 1
        list.append(arr)
    return list

if __name__=="__main__":
    # al, be = loadDataSet()
    # demo = np.zeros((1, 5))
    # getAllparam(demo)
    matrix = [[0, 0]] * 5
    print(matrix)