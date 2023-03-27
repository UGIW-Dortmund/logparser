import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean

import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf
import scipy
from scipy import stats
import seaborn as sns
from pandas.plotting import table
from scipy.stats import shapiro

from pymongo import MongoClient


if __name__ == "__main__":


    Sn_Ad_1_G_M = gf.getDb('Sn-Ad-1-G-M')
    Sn_Ad_2_G_M = gf.getDb('Sn-Ad-2-G-M')
    Ad_Sn_M = [Sn_Ad_1_G_M, Sn_Ad_2_G_M]

    Sn_Ad_1_G_F = gf.getDb('Sn-Ad-1-G-F')
    Sn_Ad_2_G_F = gf.getDb('Sn-Ad-2-G-F')
    Ad_Sn_F = [Sn_Ad_1_G_F, Sn_Ad_2_G_F]

    Sn_Ad_1_T, Sn_Ad_1_P = scipy.stats.ttest_ind(Sn_Ad_1_G_M, Sn_Ad_1_G_F)
    print(f'Sn-Ad-1 \t \t {str(Sn_Ad_1_T)} \t \t {str(Sn_Ad_1_P)}')

    Sn_Ad_2_T, Sn_Ad_2_P = scipy.stats.ttest_ind(Sn_Ad_2_G_M, Sn_Ad_2_G_F)
    print(f'Sn-Ad-2 \t \t  {str(Sn_Ad_2_T)} \t \t {str(Sn_Ad_2_P)}')



    descArray = ["Sn-1-Ad", "Sn-2-Ad"]

    num, val, df1 = gf.setXTicks_param(Ad_Sn_M, descArray)

    Sn_Ad_1_G_M = Sn_Ad_1_G_M[:79]

    print(len(Sn_Ad_1_G_F))
    print(len(Sn_Ad_1_G_M))


    plt.scatter(Sn_Ad_2_G_M, Sn_Ad_2_G_F)

    plt.show()


