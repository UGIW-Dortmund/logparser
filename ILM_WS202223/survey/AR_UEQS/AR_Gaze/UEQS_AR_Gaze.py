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


    data = pd.read_csv("UEQS_AR_Gaze.csv", delimiter=';')
    scale = ['Nein', 'Eher nein', 'Ich weiß nicht', 'Eher ja', 'Ja']

    print(data)

    print("Just partly")

    # Row 1 - Colum 2 till 7
    print(data.iloc[:1, 1:6])

    print("Print Column")
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

    ax2 = ax1.twinx()
    ax2.sharey(ax1)
    # ax2.set_ylim(ax1.get_ylim())
    ax2.set_yticks(y_nums, descrRight)
    #plt.yticks(y_nums, descrRight)
    ax2.set_box_aspect(2)


    ax1.set_yticks(y_nums, descrLeft)
    plt.plot(x_vals, y_vals, '-o', color='green', label='AR Gaze')
    #plt.grid()
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    plt.show()



