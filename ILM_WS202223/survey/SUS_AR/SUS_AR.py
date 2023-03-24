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
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    data = pd.read_csv("20230324_ILM_SUS_AR_2.csv", delimiter=';')
    scale = ['Nein', 'Eher nein', 'Ich weiß nicht', 'Eher ja', 'Ja']

    print(data)

    plot_likert.plot_likert(data, scale, plot_percentage=True)

    plt.show()


