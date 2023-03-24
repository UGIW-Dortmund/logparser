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

    data = pd.read_csv("20230324_ILM_SUS_AR_7.csv", delimiter=';')
    scale = ['Nein', 'Eher nein', 'Ich weiß nicht', 'Eher ja', 'Ja']

    scaleWeight = [['Nein', 1],
                   ['Eher nein', 2],
                   ['Ich weiß nicht', 3],
                   ['Eher ja', 4],
                   ['Ja', 5]]

    # print(data)

    df = data.iloc[:, 1:]
    # del df[df.columns[-1]]

    x_vals = []
    y_vals = []
    x_vals_median = []
    i = len(df.columns)
    boxplotVals = []


    # ls = df1 = df.iloc[0].tolist()

    j = 0
    # df1 = df.iloc[1:]
    for column in df:
        # print(df.iloc[:, j])
        ls = df.iloc[:, j]
        ls = list(ls)
        # print(ls)
        j = j + 1
        newrow = []
        for l in ls:
            if l == scale[0]:
                newrow.append(1)
            elif l == scale[1]:
                newrow.append(2)
            elif l == scale[2]:
                newrow.append(3)
            elif l == scale[3]:
                newrow.append(4)
            elif l == scale[4]:
                newrow.append(5)


        x_vals.append(statistics.mean(newrow))
        x_vals_median.append(statistics.median(newrow))
        y_vals.append(i)
        print(f'Y: {str(i)} \t \t '
              f'Mi. = {str(round(statistics.mean(newrow), 2))} \t \t'
              f' Me. = {str(round(statistics.median(newrow), 2))}')
        newrow = list(newrow)
        # box = [i, newrow]
        boxplotVals.append(newrow)
        i = i - 1


    print(boxplotVals)

    descr = df.iloc[:0]
    descr = list(descr)

    print(len(descr))


    #plt.plot(x_vals, y_vals, '-o', color='green')
    #plt.plot(x_vals_median, y_vals, '-o', color='blue')
    plt.boxplot(boxplotVals, vert=False, showmeans=True)
    plt.grid()
    plt.title("AR SUS", fontsize=15)
    plt.xticks([1, 2, 3, 4, 5], scale)
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], descr)

    plt.show()


