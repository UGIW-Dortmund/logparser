import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean

import sys
sys.path.append('/ILM_WS202223')
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

    Sn_Ad_1_T, Sn_Ad_1_P = scipy.stats.ttest_ind(Sn_Ad_1_G_M, Sn_Ad_1_G_F, equal_var=False)
    print(scipy.stats.ttest_ind(Sn_Ad_1_G_M, Sn_Ad_1_G_F, equal_var=False))

    Sn_Ad_2_T, Sn_Ad_2_P = scipy.stats.ttest_ind(Sn_Ad_2_G_M, Sn_Ad_2_G_F, equal_var=False)
    print(f'Sn-Ad-2 \t \t  {str(Sn_Ad_2_T)} \t \t {str(Sn_Ad_2_P)}')



    descArray = ["Sn-Ad-1-G-M", "Sn-Ad-2-G-M"]

    num, val, df1 = gf.setXTicks_param(Ad_Sn_M, descArray)

   # Sn_Ad_1_G_M = Sn_Ad_1_G_M[:79]

    print(len(Sn_Ad_1_G_F))
    print(len(Sn_Ad_1_G_M))

    fig, axs = plt.subplots(1, 2, figsize=(10, 8))

    axs[0].set_title('Male', fontsize=15)
    ttable = table(axs[0], df1, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    sns.violinplot(Ad_Sn_M, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(Ad_Sn_M, color="black", ax=axs[0])
    axs[0].set_xticks([])

    descArray = ["Sn-Ad-1-G-F", "Sn-Ad-2-G-F"]

    num, val, df2 = gf.setXTicks_param(Ad_Sn_F, descArray)
    sns.violinplot(Ad_Sn_F, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(Ad_Sn_F, color="black", ax=axs[1])
    df2 = df2.reset_index(drop=True)
    axs[1].set_title('Female', fontsize=15)
    ttable = table(axs[1], df2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[1].set_xticks([])

    #plt.scatter(Sn_Ad_2_G_M, Sn_Ad_2_G_F)

    plt.show()


