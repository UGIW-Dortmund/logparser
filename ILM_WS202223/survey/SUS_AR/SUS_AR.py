from pandas.plotting import table
import csv
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    data = pd.read_csv("20230324_ILM_SUS_AR_2.csv", delimiter=';')

    print(data)

