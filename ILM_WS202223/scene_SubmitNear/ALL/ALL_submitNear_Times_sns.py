import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import seaborn as sns

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
    SN_UWP_first = tresor.find({'name': 'SN_UWP_first'})
    SN_UWP_first = convertToFloat(SN_UWP_first)

    SN_UWP_second = tresor.find({'name': 'SN_UWP_second'})
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

    plt.figure(figsize=(10, 6))

    sns.set_palette("RdBu")
    sns.set_style("darkgrid")


    sns.boxplot(SN_boxplot)


    plt.show()


