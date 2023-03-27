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
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

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
    axs[0, 0].set_title('Geschlecht', fontsize=15)
    axs[0, 0].pie(df_Gender, labels=labels, colors=['teal', 'sandybrown'], autopct='%.0f%%')
    # axs[0, 0].set_xlabel("n = " + str(len(data.index)), fontsize=12)
    axs[0, 0].text(0.95, 0.95, 'n = ' + str(numberItems), transform=axs[0, 0].transAxes, fontsize=12,
                   verticalalignment='top', bbox=props)

    # Age
    df_Age = data['Age'].value_counts()
    labels = df_Age.index
    axs[0, 1].set_title('Alter', fontsize=15)
    axs[0, 1].pie(df_Age, labels=labels, colors=inner_colors, autopct='%.0f%%')
    # axs[0, 1].set_xlabel("n = " + str(len(data.index)), fontsize=12)
    axs[0, 1].text(0.95, 0.95, 'n = ' + str(numberItems), transform=axs[0, 1].transAxes, fontsize=12,
                   verticalalignment='top', bbox=props)



    # Immersive Erfahrung
    df_Age = data['immersiveExperience'].value_counts()
    labels = df_Age.index
    axs[1, 0].set_title('Immersive Erfahrung', fontsize=15)
    axs[1, 0].pie(df_Age, labels=labels, colors=['plum', 'lightblue', 'limegreen'], autopct='%.0f%%')
    # axs[1, 0].set_xlabel("n = " + str(len(data.index)), fontsize=12)
    axs[1, 0].text(0.95, 0.75, 'n = ' + str(numberItems), transform=axs[1, 0].transAxes, fontsize=12,
                   verticalalignment='top', bbox=props)

    # Gaming Erfahrung
    df_Age = data['gamingExperience'].value_counts()
    labels = df_Age.index
    axs[1, 1].set_title('Erfahrung mit Controllern', fontsize=15)
    axs[1, 1].pie(df_Age, labels=labels, colors=['limegreen', 'plum', 'lightblue'], autopct='%.0f%%')
    # axs[1, 1].set_xlabel("n = " + str(len(data.index)), fontsize=12)
    axs[1, 1].text(0.95, 0.75, 'n = ' + str(numberItems), transform=axs[1, 1].transAxes, fontsize=12,
                   verticalalignment='top', bbox=props)

    plt.show()




