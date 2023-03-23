import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean

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


""" Global Definition of Boxplot Captions """


def boxplotCap(valArray):
    median = round(statistics.median(valArray), 2)
    median = str(median).replace('.', ',')

    mean = round(statistics.mean(valArray), 2)
    mean = str(mean).replace('.', ',')

    stdev = round(statistics.stdev(valArray), 2)
    stdev = str(stdev).replace('.', ',')

    first_quartil = round(np.percentile(valArray, 25), 2)
    first_quartil = str(first_quartil).replace('.', ',')

    third_quartil = round(np.percentile(valArray, 75), 2)
    third_quartil = str(third_quartil).replace('.', ',')

    return f'\n n = {len(valArray)} \n' \
           f'Me. = {median} s \n ' \
           f'Mi. = {mean} s \n ' \
           f'S. Abw. = {stdev} s \n ' \
           f'1Q = {first_quartil} s \n ' \
           f'3Q = {third_quartil} s';


def aggregateData(array):
    lenArray = len(array)
    print("Len array " + str(lenArray))
    data = []

    for i in range(0, lenArray):
        for elem in array[i]:
            data.append(elem)

    return data;


def writeToDb(name, value):
    dbname = get_database()
    tresor = dbname["tresor"]

    dto = {"name": name, "values": value}
    tresor.insert_one(dto)




def convertToFloat(arr):

    print(arr)

    arr2 = arr.get('values')

    print(arr2)

    arr2 = list(arr2)
    lenArray = len(arr2)

    print(lenArray)

    allValues = []

    for e in range(0, lenArray):
        allValues.append(float(arr2[e]))



    return allValues



def setXTicks_param(valArray, descArray):
    xtick = []
    i = 0

    # The descirption of fields
    for elem in valArray:
        s = boxplotCap(elem)

        if descArray:
            xtick.append(descArray[i] + s)
        else:
            xtick.append(s)
        i = i + 1

    lenVA = len(valArray)

    # First Parameter the number of fields
    elements = []
    for elem in range(0, lenVA):
        elements.append((elem + 1))

    return (elements, xtick)


if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]
    tresor = dbname["tresor"]

    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']
    print(probands)


    SF_UWP_Left_HPG2 = tresor.find({'name': 'SF_UWP_L_HPG2'})
    SF_UWP_Left_HPG2 = convertToFloat(SF_UWP_Left_HPG2[0])
    SF_UWP_Left_HL2 = tresor.find({'name': 'SF_UWP_L_HL2'})
    SF_UWP_Left_HL2 = convertToFloat(SF_UWP_Left_HL2[0])


    SF_UWP_Right_HPG2 = tresor.find({'name': 'SF_UWP_R_HPG2'})
    SF_UWP_Right_HPG2 = convertToFloat(SF_UWP_Right_HPG2[0])
    SF_UWP_Right_HL2 = tresor.find({'name': 'SF_UWP_R_HL2'})
    SF_UWP_Right_HL2 = convertToFloat(SF_UWP_Right_HL2[0])


    SF_UWP_Right = [SF_UWP_Right_HL2, SF_UWP_Right_HPG2]
    SF_UWP_Right = aggregateData(SF_UWP_Right)

    SF_UWP_Left = [SF_UWP_Left_HL2, SF_UWP_Left_HPG2]
    SF_UWP_Left = aggregateData(SF_UWP_Left)

    SF_UWP_ALL = [SF_UWP_Right, SF_UWP_Left]
    SF_UWP_ALL = aggregateData(SF_UWP_ALL)
    # SF_UWP_ALL = tresor.find_one({'name': 'SF_UWP_ALL'})
    # SF_UWP_ALL = convertToFloat(SF_UWP_ALL)

    SF_AD_second = tresor.find_one({'name': 'Sf-2-Ad'})
    SF_AD_second = convertToFloat(SF_AD_second)

    SF_AD_first = tresor.find_one({'name': 'Sf-1-Ad'})
    SF_AD_first = convertToFloat(SF_AD_first)
    writeToDb('Sf-1', SF_AD_first)

    SF_ALL = [SF_UWP_ALL, SF_AD_second]
    SF_ALL = aggregateData(SF_ALL)
    writeToDb('Sf-2', SF_ALL)





    allBoxplot = [SF_UWP_Right, SF_UWP_Left, SF_UWP_ALL, SF_AD_second, SF_ALL]

    # fig = plt.subplot(figsize=(10, 8))

    descArray = ['UWP Right', 'UWP Left', 'UWP', 'MQ', 'Gesamt']

    num, val = setXTicks_param(allBoxplot, descArray)

    plt.title('Bearbeitungszeit nachgelagerte Schalftlächen')
    plt.violinplot(allBoxplot)
    # plt.axes().yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    plt.xticks(num, val)
    plt.ylabel('Sekunden')

    plt.show()
