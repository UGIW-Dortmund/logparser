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

if __name__ == '__main__':
    # fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    data = pd.read_csv("AR_UEQS_Point.csv", delimiter=';')

    df = data.iloc[:, 1:6]

    x_vals = []
    y_vals = []
    j = len(df.index)


    print(len(df.index))

    for index, row in df.iterrows():
        ls = row
        valList = []

        i = 1
        for l in ls:

            if (l != 'nan'):
                l = str(l).replace(',', '.')
                l = float(l)
                l = l * i
                valList.append(l)

            i = i + 1


            # print(valList)

        print(sum(valList))

        x_vals.append(sum(valList))
        y_vals.append(j)
        j = j - 1

    # Row 1 - Colum 2 till 7

    # descrLeft = data.iloc[0:8, 0:1]
    descrLeft = data.iloc[:, 0]
    descrLeft = list(descrLeft)

    descrRight = data[data.columns[-1]]
    descrRight = list(descrRight)
    print(descrRight)

    # y_nums = [1, 2, 3, 4, 5, 6, 7, 8]
    y_nums = [8, 7, 6, 5, 4, 3, 2, 1]



    fig, ax1 = plt.subplots()
    plt.yticks(y_nums, descrLeft)

    plt.yticks(y_nums, descrLeft)
    # ax1.set_xlim(ratingMin - 0.5, ratingMax + 0.5)
    ax1.grid()
    ax1.set(xlabel='Wertung')
    ax1.set_box_aspect(2)
    ax1.set_xlim([0, 5])
    ax1.set_ylim([0.5, 8.5])

    ax2 = ax1.twinx()
    # ax2.sharey(ax1)
    ax2.set_ylim(ax1.get_ylim())
    # ax1.set_ylim(ax2.get_ylim())

    plt.yticks(y_nums, descrRight)
    #plt.yticks(y_nums, descrRight)
    ax2.set_box_aspect(2)



    plt.plot(x_vals, y_vals, '-o', color='green', label='AR Point')
    plt.title('AR Point', fontsize=15)
    plt.xlabel('Wertung', fontsize=12)
    plt.legend()
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    plt.show()



