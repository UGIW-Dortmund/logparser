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

    ### HPG2
    UWP_Sn1_HPG2 = gf.getDb('Sn-Wi-1-HPG2')
    UWP_Sn2_HPG2 = gf.getDb('Sn-Wi-2-HPG2')

    UWP_Sn1_HPG2 = gf.getDb('Sn-Wi-1-Np-HPG2')
    UWP_Sn2_HPG2 = gf.getDb('Sn-Wi-2-Np-HPG2')

    ### HL2
    UWP_Sn1_HL2 = gf.getDb('Sn-Wi-1-HL2')
    UWP_Sn2_HL2 = gf.getDb('Sn-Wi-2-HL2')

    UWP_Sn1_HL2 = gf.getDb('Sn-Wi-1-Np-HL2')
    UWP_Sn2_HL2 = gf.getDb('Sn-Wi-2-Np-HL2')

    UWP_Sn_HL2 = [UWP_Sn1_HL2, UWP_Sn2_HL2]
    UWP_Sn_HPG2 = [UWP_Sn1_HPG2, UWP_Sn2_HPG2]

    print("T-Test")
    print(scipy.stats.ttest_ind(UWP_Sn1_HPG2, UWP_Sn1_HL2, equal_var=False))
    print(scipy.stats.ttest_ind(UWP_Sn2_HPG2, UWP_Sn2_HL2, equal_var=False))

    print("Wilcox")
    print(scipy.stats.mannwhitneyu(UWP_Sn1_HPG2, UWP_Sn1_HL2))
    print(scipy.stats.mannwhitneyu(UWP_Sn2_HPG2, UWP_Sn2_HL2))




    plt.hist(UWP_Sn2_HPG2)

    plt.show()

    '''
    
    fig, axs = plt.subplots(1, 2, figsize=(10, 8))
    axs[0].set_ylabel('Sekunden', fontsize=12)
    axs[1].set_ylabel('Sekunden', fontsize=12)

    descArray = ["Sn-1-Wi", "Sn-2-Wi"]
    fig.suptitle('Korrelationsuntersuchung zwischen AR und VR', fontsize=15)

    num, val, df1 = gf.setXTicks_paramCorrelation(UWP_Sn_HL2, descArray, '14')

    axs[0].set_title('HoloLens 2 (AR)', fontsize=15)
    ttable = table(axs[0], df1, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    sns.violinplot(UWP_Sn_HL2, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(UWP_Sn_HL2, color="black", ax=axs[0])
    axs[0].set_xticks([])
    axs[1].sharey(axs[0])

    descArray = ["Sn-1-Wi", "Sn-2-Wi"]

    num, val, df2 = gf.setXTicks_paramCorrelation(UWP_Sn_HPG2, descArray, '13')
    sns.violinplot(UWP_Sn_HPG2, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(UWP_Sn_HPG2, color="black", ax=axs[1])
    df2 = df2.reset_index(drop=True)
    axs[1].set_title('Reverb G2 (VR)', fontsize=15)
    ttable = table(axs[1], df2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[1].set_xticks([])


    plt.show()


    '''


