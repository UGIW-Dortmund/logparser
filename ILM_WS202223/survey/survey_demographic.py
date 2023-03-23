from pandas.plotting import table
import csv
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    data = pd.read_csv("20230323_ILM_survey_demo.csv", delimiter=';')

    data['gender'].value_counts().plot(kind='pie', ax=axs[0, 0],
                                       xlabel="nnn", title="Geschlecht",
                                       ylabel="")

    data['immersiveExperience'].value_counts().plot(kind='pie', ax=axs[1, 0],
                                       title="Immersive Erfahrung", ylabel="")

    data['gamingExperience'].value_counts().plot(kind='pie', ax=axs[1, 1],
                                       title="Erfahrung mit Controllern", ylabel="")

    data = pd.read_csv("20230323_ILM_survey_demo.csv", delimiter=';')

    data['dominantHand'].value_counts().plot(kind='pie', ax=axs[0, 1],
                                             title="Dominante Hand", ylabel="")


    plt.show()

    print(data)

