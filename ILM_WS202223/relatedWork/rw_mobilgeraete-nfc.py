import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import numpy as np
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf

if __name__ == '__main__':

    # Setup
    klmValues = [2900, 6100, 8900]
    measurements = [2600, 4900, 6200]
    updatedKlmValues = [2600, 4000, 6000]

    #klmValues = [2900, 2600, 2600]
    #measurements = [6100, 4900, 4000]
    #updatedKlmValues = [8900, 6200, 6000]

    width = 0.2

    # Plot


    X = ['Task 1', 'Task 2', 'Task 3']
    X = np.arange(len(klmValues))

    plt.title('Überarbeites KLM für den Einsatz von NFC', fontsize=15)
    plt.grid(axis='y', linestyle='-', which='major', color='lightgray', alpha=0.5)

    plt.bar(X - width, klmValues, width, label="Original KLM-Werte")
    plt.bar(X, measurements, width, label="Messwerte")
    plt.bar(X + width, updatedKlmValues, width, label="Überarbeitete KLM-Werte")
    plt.legend(prop={'size': 14})
    plt.xticks([0, 1, 2], ['Task 1', 'Task 2', 'Task 3'])
    plt.ylabel("Millisekunden", fontsize=15)

    plt.show()