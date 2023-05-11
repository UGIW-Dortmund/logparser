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
import matplotlib.pyplot as plt

import seaborn as sns
from pandas.plotting import table

from pymongo import MongoClient


if __name__ == "__main__":
    # Get the database


    SF_UWP_R_HPG2 = gf.getDb('SF_UWP_R_HPG2')
    SF_UWP_L_HPG2 = gf.getDb('SF_UWP_L_HPG2')

    SF_UWP_R_HL2 = gf.getDb('SF_UWP_R_HL2')
    SF_UWP_L_HL2 = gf.getDb('SF_UWP_L_HL2')

    SF_UWP_L = [SF_UWP_L_HPG2, SF_UWP_L_HL2]
    SF_UWP_L = gf.aggregateData(SF_UWP_L)
    SF_UWP_R = [SF_UWP_R_HPG2, SF_UWP_R_HL2]
    SF_UWP_R = gf.aggregateData(SF_UWP_R)

    print(SF_UWP_R)
    print(SF_UWP_L)
    descArray = ['Rechts', 'Links']
    data = [SF_UWP_R, SF_UWP_L]

    print(scipy.stats.ttest_ind(SF_UWP_R_HL2, SF_UWP_L_HL2, equal_var = False))
    print(scipy.stats.ttest_ind(SF_UWP_R_HPG2, SF_UWP_L_HPG2, equal_var=False))
    print(scipy.stats.ttest_ind(SF_UWP_R, SF_UWP_L, equal_var=False))

    (num, val, df) = gf.setXTicks_param(data, descArray)

    ttable = table(plt.gca(), df, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
    ttable.set_fontsize(10)
    ttable.auto_set_font_size(False)
    plt.grid(axis='y', linestyle='-', which='major', color='lightgrey', alpha=0.5)

    # plt.xticks(num, val)
    plt.ylabel('Sekunden')



    plt.boxplot(data)


    plt.show()




