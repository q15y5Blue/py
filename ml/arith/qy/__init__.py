# -*- coding: utf-8 -*-
from numpy import *
import numpy as np
import operator
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as img
from os import listdir
from math import log
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False


#  矩阵除法 ：linalg.solve(matA,matB)