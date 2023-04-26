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
    fig, axs = plt.subplots(1, 3, figsize=(10, 8))

    data = pd.read_csv("20230324_ILM_survey.CSV", delimiter=';')

    numberItems = len(data.index)

    props = dict(boxstyle='round', facecolor='lightgray', alpha=1.0)
    cmap = plt.get_cmap("tab20c")
    outer_colors = cmap(np.arange(2))
    cmap = plt.get_cmap("Dark2")
    inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))
    cmap = plt.get_cmap("Set2")
    first_colors = cmap(np.arange(3))
    cmap = plt.get_cmap("Set1")
    second_colors = cmap(np.arange(4))

    # Gender
    df_Gender = data['gender'].value_counts()
    labels = 'männlich', 'weiblich'
    axs[0].set_title('Geschlecht', fontsize=15)
    axs[0].pie(df_Gender, labels=labels, colors=['#66CDAA', 'sandybrown'], autopct='%.0f%%', textprops={'fontsize': 14})
    # axs[0, 0].set_xlabel("n = " + str(len(data.index)), fontsize=12)
    axs[0].text(0.95, 0.95, 'n = ' + str(numberItems), transform=axs[0].transAxes, fontsize=15,
                   verticalalignment='top', bbox=props)

    # Age
    df_Age = data['Age'].value_counts()
    labels = df_Age.index
    #labels = '18 - 25 Jahre', '25 - 30 Jahre', '30 - 40 Jahre', '40 - 50 Jahre'
    axs[1].set_title('Alter (in Jahren)', fontsize=15)
    axs[1].pie(df_Age, labels=labels, colors=inner_colors, autopct='%.0f%%', textprops={'fontsize': 14})
    # axs[0, 1].set_xlabel("n = " + str(len(data.index)), fontsize=12)
    axs[1].text(0.95, 0.95, 'n = ' + str(numberItems), transform=axs[1].transAxes, fontsize=15,
                   verticalalignment='top', bbox=props)



    # Immersive Erfahrung
    df_dH = data['dominantHand'].value_counts()
    labels = df_dH.index
    axs[2].set_title('Dominante Hand', fontsize=15)
    axs[2].pie(df_dH, labels=labels, colors=['cornflowerblue', 'forestgreen'], autopct='%.0f%%', textprops={'fontsize': 14})
    # axs[1, 0].set_xlabel("n = " + str(len(data.index)), fontsize=12)
    axs[2].text(0.95, 0.95, 'n = ' + str(numberItems), transform=axs[2].transAxes, fontsize=15,
                   verticalalignment='top', bbox=props)


    plt.show()




