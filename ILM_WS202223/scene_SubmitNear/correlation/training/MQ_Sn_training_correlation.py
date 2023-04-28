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

    # MQP First
    Sn_Ad_Sn1_training_MQP_First = gf.getDb('Sn-Ad-1-Training-MQP-First')
    Sn_Ad_Sn2_training_MQP_First = gf.getDb('Sn-Ad-2-Training-MQP-First')

    Sn_Ad_Sn1_training_MQP_First = gf.getDb('Sn-Ad-1_Np_Training_MQP_First')
    Sn_Ad_Sn2_training_MQP_First = gf.getDb('Sn-Ad-2_Np_Training_MQP_First')

    # MQP Second
    Sn_Ad_Sn1_training_MQP_Second = gf.getDb('Sn-Ad-1-Training-MQP-Second')
    Sn_Ad_Sn2_training_MQP_Second = gf.getDb('Sn-Ad-2-Training-MQP-Second')

    Sn_Ad_Sn1_training_MQP_Second = gf.getDb('Sn-Ad-1_Np_Training_MQP_Second')
    Sn_Ad_Sn2_training_MQP_Second = gf.getDb('Sn-Ad-2_Np_Training_MQP_Second')

    # MQ2 First
    Sn_Ad_Sn1_training_MQ2_First = gf.getDb('Sn-Ad-1-Training-MQ2-First')
    Sn_Ad_Sn2_training_MQ2_First = gf.getDb('Sn-Ad-2-Training-MQ2-First')

    Sn_Ad_Sn1_training_MQ2_First = gf.getDb('Sn-Ad-1_Np_Training_MQ2_First')
    Sn_Ad_Sn2_training_MQ2_First = gf.getDb('Sn-Ad-2_Np_Training_MQ2_First')

    # MQ2 Second
    Sn_Ad_Sn1_training_MQ2_Second = gf.getDb('Sn-Ad-1-Training-MQ2-Second')
    Sn_Ad_Sn2_training_MQ2_Second = gf.getDb('Sn-Ad-2-Training-MQ2-Second')

    Sn_Ad_Sn1_training_MQ2_Second = gf.getDb('Sn-Ad-1_Np_Training_MQ2_Second')
    Sn_Ad_Sn2_training_MQ2_Second = gf.getDb('Sn-Ad-2_Np_Training_MQ2_Second')



    # Sn-1
    Sn_Ad_Sn1_training_First = [Sn_Ad_Sn1_training_MQP_First, Sn_Ad_Sn1_training_MQ2_First]
    Sn_Ad_Sn1_training_First = gf.aggregateData(Sn_Ad_Sn1_training_First)
    Sn_Ad_Sn1_training_Second = [Sn_Ad_Sn1_training_MQP_Second, Sn_Ad_Sn1_training_MQ2_Second]
    Sn_Ad_Sn1_training_Second = gf.aggregateData(Sn_Ad_Sn1_training_Second)




    # Sn-2
    Sn_Ad_2_training_First = [Sn_Ad_Sn2_training_MQP_First, Sn_Ad_Sn2_training_MQ2_First]
    Sn_Ad_2_training_First = gf.aggregateData(Sn_Ad_2_training_First)
    Sn_Ad_2_training_Second = [Sn_Ad_Sn2_training_MQP_Second, Sn_Ad_Sn2_training_MQ2_Second]
    Sn_Ad_2_training_Second = gf.aggregateData(Sn_Ad_2_training_Second)
    print(Sn_Ad_2_training_Second)

    # Macht der Proband OHNE Trainingseffekt - als Erstes
    Sn_Ad_Training_First = [Sn_Ad_Sn1_training_First, Sn_Ad_2_training_First]


    # Macht der Proband MIT Trainingseffekt - als Zweites
    Sn_Ad_Training_Second = [Sn_Ad_Sn1_training_Second, Sn_Ad_2_training_Second]

    print("T-Test")
    print(scipy.stats.ttest_ind(Sn_Ad_Sn1_training_First, Sn_Ad_Sn1_training_Second))
    print(scipy.stats.ttest_ind(Sn_Ad_2_training_First, Sn_Ad_2_training_Second))

    print("Man Whitney U")
    print(scipy.stats.mannwhitneyu(Sn_Ad_Sn1_training_First, Sn_Ad_Sn1_training_Second))
    print(scipy.stats.mannwhitneyu(Sn_Ad_2_training_First, Sn_Ad_2_training_Second))

    fig, axs = plt.subplots(1, 2, figsize=(10, 8))

    descArray = ["Sn-1-Ad", "Sn-2-Ad"]

    fig.suptitle('Korrelationsuntersuchung bei Sn auf einen Trainigseffekt', fontsize=15)

    num, val, df1 = gf.setXTicks_paramCorrelation(Sn_Ad_Training_First, descArray, '5')

    axs[0].set_title('Als Erstes - Ohne Trainingseffekt', fontsize=15)
    ttable = table(axs[0], df1, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    sns.violinplot(Sn_Ad_Training_First, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(Sn_Ad_Training_First, color="black", ax=axs[0])
    axs[0].set_xticks([])
    axs[1].sharey(axs[0])

    descArray = ["Sn-1-Ad", "Sn-2-Ad"]

    num, val, df2 = gf.setXTicks_paramCorrelation(Sn_Ad_Training_Second, descArray, '5')
    sns.violinplot(Sn_Ad_Training_Second, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(Sn_Ad_Training_Second, color="black", ax=axs[1])
    df2 = df2.reset_index(drop=True)
    axs[1].set_title('Als Zweites - Mit Trainingseffekt', fontsize=15)
    ttable = table(axs[1], df2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[1].set_xticks([])


    plt.show()





