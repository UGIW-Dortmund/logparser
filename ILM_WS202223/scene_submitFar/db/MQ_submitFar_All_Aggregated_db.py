import datetime
import decimal
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import locale
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



def setYTicks_param(valArray, descArray):
    xtick = []
    i = 0

    # The descirption of fields
    for elem in valArray:
        s = ''
        # str(elem)
        # boxplotCap(elem)

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


def writeToDb(name, value):
    dbname = get_database()
    tresor = dbname["tresor"]

    dto = tresor.find({"name": name})
    dto = list(dto)

    print("Dto")
    print(dto)

    if (len(dto) > 0):
        dto = {"name": name}
        newvalues = {"$set": {"values": value}}
        tresor.update_one(dto, newvalues)
        print("Update element")
    else:
        dto = {"name": name, "values": value}
        tresor.insert_one(dto)
        print("New element")




# This is added so that many files can reuse the function get_database()
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


def convertToFloat(arr):

    print(arr)

    arr2 = arr.get('values')

    print(arr2)

    arr2 = list(arr2)
    lenArray = len(arr2)

    print(lenArray)

    allValues = []

    for e in range(0, lenArray):
        floatValues = []

        for elem in arr2[e]:
            floatValues.append(float(elem))

        allValues.append(floatValues)

    return allValues

if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]
    tresor = dbname["tresor"]

    locale.setlocale(locale.LC_ALL, 'de_DE')


    #probands = col.distinct('prob')
    # probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    # probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A18']
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
                'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24,' 'A25', 'A26', 'A27', 'A28']
    print(probands)

    sceneName = 'ILM_Submit-Far_Left_Scene'
    devices = ['MQP', 'MQ2']
    devices = ['MQ2']


    # Toggle
    allTimesToggleLeft = tresor.find_one({'name': 'SF_MQ_L_Toggle'})
    allTimesToggleLeft = convertToFloat(allTimesToggleLeft)

    allTimesToggleRight = tresor.find_one({'name': 'SF_MQ_R_Toggle'})
    allTimesToggleRight = convertToFloat(allTimesToggleRight)



    # Button
    allTimesButtonLeft = tresor.find_one({'name': 'SF_MQ_L_Button'})
    allTimesButtonLeft = convertToFloat(allTimesButtonLeft)

    allTimesButtonRight = tresor.find_one({'name': 'SF_MQ_R_Button'})
    allTimesButtonRight = convertToFloat(allTimesButtonRight)

    # Slider
    allTimesSliderLeft = tresor.find_one({'name': 'SF_MQ_L_Slider'})
    allTimesSliderLeft = convertToFloat(allTimesSliderLeft)


    allTimesSliderRight = tresor.find_one({'name': 'SF_MQ_R_Slider'})
    allTimesSliderRight = convertToFloat(allTimesSliderRight)


    # Dropdown
    allTimesDropdownLeft = tresor.find_one({'name': 'SF_MQ_L_Dropdown'})
    allTimesDropdownLeft = convertToFloat(allTimesDropdownLeft)

    allTimesDropdownRight = tresor.find_one({'name': 'SF_MQ_R_Dropdown'})
    allTimesDropdownRight = convertToFloat(allTimesDropdownRight)




    allLeft =  allTimesButtonLeft + allTimesToggleLeft\
               + allTimesSliderLeft + allTimesDropdownLeft



    allRight = allTimesButtonRight + allTimesToggleRight \
               + allTimesSliderRight + allTimesDropdownRight


    allFirst = allTimesButtonLeft[0] + allTimesToggleLeft[0] \
              + allTimesSliderLeft[0] + allTimesDropdownLeft[0] \
              + allTimesButtonRight[0] + allTimesToggleRight[0] \
              + allTimesSliderRight[0] + allTimesDropdownRight[0]

    writeToDb('SF_AD_first', allFirst)

    #allFirst = aggregateData(allFirst)

    allSecond = allTimesButtonLeft[1] + allTimesToggleLeft[1] \
               + allTimesSliderLeft[1] + allTimesDropdownLeft[1] \
               + allTimesButtonRight[1] + allTimesToggleRight[1] \
               + allTimesSliderRight[1] + allTimesDropdownRight[1] \
                + allTimesButtonLeft[2] + allTimesToggleLeft[2] \
                + allTimesSliderLeft[2] + allTimesDropdownLeft[2] \
                + allTimesButtonRight[2] + allTimesToggleRight[2] \
                + allTimesSliderRight[2] + allTimesDropdownRight[2]

    writeToDb('SF_AD_second', allSecond)

    # allSecond = aggregateData(allSecond)

    # allBoxplot = [{'first': allFirst, 'second': allSecond}]

    allBoxplot = [allFirst, allSecond]

    fig = plt.subplots(figsize=(10, 8))

    plt.title('Android: Sf MQ2')
    plt.ylabel('Sekunden')


    # fig.suptitle('Bearbeitungszeit aller Elemente')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])

    descArray = ["Erste S.", "Nachgelagerte S."]

    plt.axes().yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    (x_nums, x_text) = setXTicks_param(allBoxplot, descArray)

    sns.violinplot(allBoxplot, split=True)

    plt.xticks([0, 1], x_text)

    plt.show()


