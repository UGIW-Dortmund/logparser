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

    # Age: 18-25
    #Sn_Ad_1_age_18_25 = gf.getDb('Sn-Ad-1-age-18-25')
    #Sn_Ad_2_age_18_25 = gf.getDb('Sn-Ad-2-age-18-25')

    Sn_Ad_1_age_18_25 = gf.getDb('Sn-Ad-1-age-18-25-np')
    Sn_Ad_2_age_18_25 = gf.getDb('Sn-Ad-2-age-18-25-np')
    Ad_Sn_age_18_25 = [Sn_Ad_1_age_18_25, Sn_Ad_2_age_18_25]

    # Age: 25-30
    #Sn_Ad_1_age_25_30 = gf.getDb('Sn-Ad-1-age-25-30')
    #Sn_Ad_2_age_25_30 = gf.getDb('Sn-Ad-2-age-25-30')

    Sn_Ad_1_age_25_30 = gf.getDb('Sn-Ad-1-age-25-30-np')
    Sn_Ad_2_age_25_30 = gf.getDb('Sn-Ad-2-age-25-30-np')

    Ad_Sn_age_25_30 = [Sn_Ad_1_age_25_30, Sn_Ad_2_age_25_30]

    # Age: 30-40
    #Sn_Ad_1_age_30_40 = gf.getDb('Sn-Ad-1-age-30-40')
    Sn_Ad_2_age_30_40 = gf.getDb('Sn-Ad-2-age-30-40')

    Sn_Ad_1_age_30_40 = gf.getDb('Sn-Ad-1-age-30-40-np')
    Sn_Ad_2_age_30_40 = gf.getDb('Sn-Ad-2-age-30-40-np')

    Ad_Sn_age_30_40 = [Sn_Ad_1_age_30_40, Sn_Ad_2_age_30_40]

    # Age: 40-50
    # Sn_Ad_1_age_40_50 = gf.getDb('Sn-Ad-1-age-40-50')
    # Sn_Ad_2_age_40_50 = gf.getDb('Sn-Ad-2-age-40-50')

    Sn_Ad_1_age_40_50 = gf.getDb('Sn-Ad-1-age-40-50-np')
    Sn_Ad_2_age_40_50 = gf.getDb('Sn-Ad-2-age-40-50-np')

    Ad_Sn_age_40_50 = [Sn_Ad_1_age_40_50, Sn_Ad_2_age_40_50]

    #print(scipy.stats.ttest_ind(Sn_Ad_1_dH_R, Sn_Ad_1_dH_L, equal_var=False))
    #print(scipy.stats.ttest_ind(Sn_Ad_2_dH_R, Sn_Ad_2_dH_L, equal_var=False))


    print(stats.f_oneway(Sn_Ad_1_age_18_25, Sn_Ad_1_age_25_30, Sn_Ad_1_age_30_40, Sn_Ad_1_age_40_50))
    print(stats.f_oneway(Sn_Ad_2_age_18_25, Sn_Ad_2_age_25_30, Sn_Ad_2_age_30_40, Sn_Ad_2_age_40_50))

    fig, axs = plt.subplots(1, 4, figsize=(10, 8))

    descArray = ['Sn-Ad-1', 'Sn-Ad-2']
    # descArray = ['Sn-Ad-1-age-18-25', 'Sn-Ad-2-age-18-25']

    axs[0].set(ylabel='Sekunden')
    axs[1].set(ylabel='Sekunden')
    axs[2].set(ylabel='Sekunden')
    axs[3].set(ylabel='Sekunden')

    fig.suptitle('Korrelationsuntersuchung auf Altersgruppen', fontsize=16)

    axs[0].set_title('18 - 25 Jahre', fontsize=15)
    num, val, df1 = gf.setXTicks_paramCorrelation(Ad_Sn_age_18_25, descArray, '7')
    ttable = table(axs[0], df1, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    sns.violinplot(Ad_Sn_age_18_25, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(Ad_Sn_age_18_25, color="black", ax=axs[0])
    axs[0].set_xticks([])
    axs[0].sharey(axs[3])

    # descArray = ['Sn-Ad-1-age-25-30', 'Sn-Ad-2-age-25-30']
    # descArray = ["Sn-Ad-1-dH-L", "Sn-Ad-2-dH-L"]
    axs[1].set_title('25 - 30 Jahre', fontsize=15)
    num, val, df2 = gf.setXTicks_paramCorrelation(Ad_Sn_age_25_30, descArray, '4')
    sns.violinplot(Ad_Sn_age_25_30, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(Ad_Sn_age_25_30, color="black", ax=axs[1])
    df2 = df2.reset_index(drop=True)
    ttable = table(axs[1], df2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[1].set_xticks([])
    axs[1].sharey(axs[3])

    # descArray = ['Sn-Ad-1-age-30-40', 'Sn-Ad-2-age-30-40']
    axs[2].set_title('30 - 40 Jahre', fontsize=15)
    num, val, df3 = gf.setXTicks_paramCorrelation(Ad_Sn_age_30_40, descArray, '9')
    sns.violinplot(Ad_Sn_age_30_40, showmeans=True, color="skyblue", ax=axs[2])
    sns.swarmplot(Ad_Sn_age_30_40, color="black", ax=axs[2])
    df3 = df3.reset_index(drop=True)
    ttable = table(axs[2], df3, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[2].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[2].set_xticks([])
    axs[2].sharey(axs[3])

    # descArray = ['Sn-Ad-1-age-30-40', 'Sn-Ad-2-age-30-40']
    axs[3].set_title('40 - 50 Jahre', fontsize=15)
    num, val, df4 = gf.setXTicks_paramCorrelation(Ad_Sn_age_40_50, descArray, '4')
    sns.violinplot(Ad_Sn_age_40_50, showmeans=True, color="skyblue", ax=axs[3])
    sns.swarmplot(Ad_Sn_age_40_50, color="black", ax=axs[3])
    df4 = df4.reset_index(drop=True)
    ttable = table(axs[3], df4, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[3].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[3].set_xticks([])
    # axs[3].sharey(axs[0])

    plt.show()






