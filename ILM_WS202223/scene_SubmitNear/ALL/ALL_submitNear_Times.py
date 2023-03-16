import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import seaborn as sns
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf

from pymongo import MongoClient



###
### For figuring out the operating times for teleporting
###
def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://fredix:memphis55@kurz-containar.de:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['ilm']


def aggregateData(array):
    lenArray = len(array)
    print("Len array " + str(lenArray))
    data = []

    for i in range(0, lenArray):
        for elem in array[i]:
            data.append(elem)

    return data;

def boxplotCap(valArray):

    return f' \n n = {len(valArray)} \n \n ' \
            f'Me. = {round(statistics.median(valArray), 3)} s \n ' \
            f'Mi. = {round(statistics.mean(valArray), 3)} s \n ' \
            f'S. Ab. = {round(statistics.stdev(valArray), 3)} s \n ' \
            f'M. Ab. = {round(mean(valArray), 3)} s \n ' \
            f'1Q = {round(np.percentile(valArray, 25), 3)} s \n' \
            f'3Q = {round(np.percentile(valArray, 75), 3)} s ';

def convertToFloat(arr):

    arr = list(arr)
    arr = arr[0].get('values')

    floatValues = []

    for elem in arr:
        floatValues.append(float(elem))

    return  floatValues


if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    tresor = dbname["tresor"]

    #### UWP
    SN_UWP_first = tresor.find({'name': 'SN_1_Wi'})
    SN_UWP_first = convertToFloat(SN_UWP_first)

    SN_UWP_second = tresor.find({'name': 'SN_2_Wi'})
    SN_UWP_second = convertToFloat(SN_UWP_second)

    SN_UWP_boxplot = [SN_UWP_first, SN_UWP_second]


    #### Android
    SN_AD_first = tresor.find({'name': 'SN_AD_first'})
    SN_AD_first = convertToFloat(SN_AD_first)

    SN_AD_second = tresor.find({'name': 'SN_AD_second'})
    SN_AD_second = convertToFloat(SN_AD_second)

    SN_AD_boxplot = [SN_AD_first, SN_AD_second]

    #### ALL

    SN_first = [SN_AD_first, SN_UWP_first]
    SN_first = aggregateData(SN_first)

    SN_second = [SN_UWP_second, SN_AD_second]
    SN_second = aggregateData(SN_second)

    SN_boxplot = [SN_first, SN_second]

    fig, axs = plt.subplots(1, 3, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit der Buttons')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0].violinplot(SN_UWP_boxplot)
    axs[1].violinplot(SN_AD_boxplot)
    axs[1].sharey(axs[0])

    print(SN_UWP_boxplot)

    axs[2].violinplot(SN_boxplot)
    axs[2].sharey(axs[0])

    axs[0].set(ylabel='Sekunden')

    descArray = ["SN-1-Wi", "SN-2-Wi"]
    num, val = gf.setXTicks_param(SN_UWP_boxplot, descArray)
    axs[0].set_title('Windows-Anwendungen')
    axs[0].set_xticks(num, val)

    descArray = ["SN-1-Ad", "SN-2-Ad"]
    num, val = gf.setXTicks_param(SN_AD_boxplot, descArray)
    axs[1].set_title('Android-Anwendungen')
    axs[1].set_xticks(num, val)

    descArray = ["SN-1", "SN-2"]
    num, val = gf.setXTicks_param(SN_boxplot, descArray)
    axs[2].set_title('Zusammenfassung')
    axs[2].set_xticks(num, val)

    plt.show()

