import datetime
import decimal
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import locale
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf
from pandas.plotting import table

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
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24,' 'A25', 'A26', 'A27', 'A28']
    print(probands)

    sceneName = 'ILM_Submit-Far_Left_Scene'
    devices = ['MQP', 'MQ2']


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

    fig, axs = plt.subplots(2, 1, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit aller Elemente')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0].boxplot(allRight, showmeans=True, vert=True)

    axs[1].boxplot(allLeft, showmeans=True, vert=True)
    axs[1].sharey(axs[0])


    axs[0].set_ylabel('Sekunden', fontsize=12)
    axs[1].set_ylabel('Sekunden', fontsize=12)


    descArrayDetail = ["Button 1", "Button 2", "Button 3",
                 "Toggle 1", "Toggle 2", "Toggle 3",
                 "Slider 1", "Slider 2", "Slider 3",
                 "Dropdown 1", "Dropdown 2", "Dropdown 3"]

    descArray = ["B1", "B2", "B3",
                 "T1", "T2", "T3",
                 "S1", "S2", "S3",
                 "D1", "D2", "D3"]

    columnsDesc = ("B1", "B2", "B3",
                 "T1", "T2", "T3",
                 "S1", "S2", "S3",
                 "D1", "D2", "D3")
    rows = ["n", "Me.", "Mi."]
    # (x_nums, x_text) = setXTicks_param(allLeft, descArray)

    (y_nums, y_text) = setYTicks_param(allLeft, descArray)


    num, val, df_Right = gf.setXTicksMin(allRight, descArray)

    axs[0].set_title('1. Rechte Hand', fontsize=15)
    axs[0].set_xticks([])
    # axs[0].xaxis.set_tick_params(labelsize=12)
    print("1. Rechte Hand")
    # gf.reqLatexTableOutput(allRight, descArrayDetail)
    # Add a table at the bottom of the axes
    # the_table = plt.table(cellText=val, rowLabels=num, colLabels=descArray, loc='bottom')
    # plt.bar(a, grouped_dataframe.loc[0].values.tolist()[:-1], width=1, label='setosa')
    #axs[0].bar(val, height=-5)
    ttable = table(axs[0], df_Right, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
    ttable.set_fontsize(10)
    ttable.auto_set_font_size(False)
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    num, val, df_Left = gf.setXTicksMin(allLeft, descArray)

    axs[1].set_title('2. Linke Hand', fontsize=15)
    axs[1].set_xticks([])
    axs[1].xaxis.set_tick_params(labelsize=12)
    print("2. Linke Hand")
    # gf.reqLatexTableOutput(allLeft, descArrayDetail)
    ttable = table(axs[1], df_Left, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
    ttable.set_fontsize(10)
    ttable.auto_set_font_size(False)
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    plt.show()


