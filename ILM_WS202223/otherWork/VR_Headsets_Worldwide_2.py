from pandas.plotting import table
import csv
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import locale
locale.setlocale(locale.LC_NUMERIC, "de_DE")

if __name__ == '__main__':

    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    val = [42.04, 13.16, 9.59, 5.67, 3.82, 25.36]
    labels = ['Oculus Quest 2 - 42 %', 'Valve Index HMD - 13 %', 'Oculus Rift S - 10 %',
              'HTC Vive - 6 %', 'Windows Mixed Reality - 4 %', 'Andere - 25 %']


    wedges, texts = ax.pie(val, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(labels[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y), fontsize=15,
                    horizontalalignment=horizontalalignment, **kw)

    # 1.35
    # ax.set_title("Matplotlib bakery: A donut")



    #plt.pie(val, labels=labels, autopct='%.0f%%',  wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })

    #plt.legend(val, labels)

    plt.show()