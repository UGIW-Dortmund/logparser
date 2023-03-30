import statistics

from pandas.plotting import table
import csv
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plot_likert
from pandas import DataFrame
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf


if __name__ == '__main__':

    dataDresden = open('20230202_Ping-Server_Dresden.txt')
    dataRenningen = open('20230209_Ping-Server_Renningen.txt')

    pingListDresden = []
    pintListRenningen = []


    s = dataDresden.read()
    dataRenningen = dataRenningen.read()

    answersDresden = s.split('\n')
    answersRenningen = dataRenningen.split('\n')

    # print(answers[1])

    for answer in answersDresden:
        time = answer[40:42]
        time = float(time)

        pingListDresden.append(time)


    for answer in answersRenningen:
        time = answer[40:42]
        time = float(time)
        pintListRenningen.append(time)


    pingList = [pingListDresden, pintListRenningen]

    descArray = ['Dresden', 'Renningen']
    plt.title('Ping-Antwortzeiten von den Studienstandorten', fontsize=15)
    num, val, df = gf.setXTicks_paramPing(pingList, descArray)
    plt.ylabel('Millisekunden', fontsize=12)
    plt.boxplot(pingList)
    ttable = table(plt.gca(), df, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)

    plt.xticks([])
    plt.show()
