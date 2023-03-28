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

from pymongo import MongoClient




if __name__ == "__main__":
    # Get the database


    Sn_Ad_1_dH_R = gf.getDb('Sn-Ad-1-dH_R')
    Sn_Ad_2_dH_R = gf.getDb('Sn-Ad-2-dH_R')
    Ad_Sn_dH_R = [Sn_Ad_1_dH_R, Sn_Ad_2_dH_R]


    Sn_Ad_1_dH_L = gf.getDb('Sn-Ad-1-dH_L')
    Sn_Ad_2_dH_L = gf.getDb('Sn-Ad-2-dH_L')
    Ad_Sn_dH_L = [Sn_Ad_1_dH_L, Sn_Ad_2_dH_L]

    print(scipy.stats.ttest_ind(Sn_Ad_1_dH_R, Sn_Ad_1_dH_L, equal_var=False))
    print(scipy.stats.ttest_ind(Sn_Ad_2_dH_R, Sn_Ad_2_dH_L, equal_var=False))



    fig, axs = plt.subplots(1, 2, figsize=(10, 8))


    fig.suptitle('Correlation @ Sn: Dominant Hand', fontsize=15)


    axs[1].sharey(axs[0])

    axs[0].set_ylabel('Sekunden', fontsize=12)
    axs[1].set_ylabel('Sekunden', fontsize=12)

    descArray = ["Sn-Ad-1-dH-R", "Sn-Ad-2-dH-R"]

    num, val, df1 = gf.setXTicks_param(Ad_Sn_dH_R, descArray)


    axs[0].set_title('Rechte Hand', fontsize=15)
    ttable = table(axs[0], df1, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    sns.violinplot(Ad_Sn_dH_R, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(Ad_Sn_dH_R, color="black", ax=axs[0])
    axs[0].set_xticks([])

    descArray = ["Sn-Ad-1-dH-L", "Sn-Ad-2-dH-L"]

    num, val, df2 = gf.setXTicks_param(Ad_Sn_dH_L, descArray)
    sns.violinplot(Ad_Sn_dH_L, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(Ad_Sn_dH_L, color="black", ax=axs[1])
    df2 = df2.reset_index(drop=True)
    axs[1].set_title('Linke Hand', fontsize=15)
    ttable = table(axs[1], df2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[1].set_xticks([])

    plt.show()


