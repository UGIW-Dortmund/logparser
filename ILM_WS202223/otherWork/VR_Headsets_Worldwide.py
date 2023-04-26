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

    val = [42.04, 13.16, 9.59, 5.67, 3.82, 25.36]
    labels = ['Oculus Quest 2', 'Valve Index HMD', 'Oculus Rift S', 'HTC Vive', 'Windows Mixed Reality', 'Andere']


    plt.pie(val, labels=labels, autopct='%.0f%%',  wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })

    plt.legend()


    plt.show()