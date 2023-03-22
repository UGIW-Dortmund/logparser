import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
from pandas.plotting import table
from pymongo import MongoClient
import seaborn as sns
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf



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
           f'U.Q. = {first_quartil} s \n ' \
           f'O.Q. = {third_quartil} s';


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


""" Ermittelt die Zeiten, welche die Probanden gebraucht haben """


def runAnalyzeCubes(probands, sceneName, device, refreshRate):
    timeArray = []

    cubeArray = [['Cube_1', 300], ['Cube_2', 250], ['Cube_3', 200], ['Cube_4', 150], ['Cube_5', 120], ['Cube_6', 80]]
    # cubeArray = [['Cube_1', 300]]

    for p in probands:

        for d in device:

            # For-Loop mit den verschiedenen Würfeln
            for cube in cubeArray:

                start_array = runAnaStartAction(p, sceneName, d, cube[0])
                end_array = runAnaFinishAction(p, sceneName, d, cube[0])

                if len(start_array) > 0 and len(end_array) > 0:
                    start_time = start_array[0].get('time')
                    start_date = start_array[0].get('date')

                    start = pd.to_datetime(start_date + ' ' + start_time)

                    end_time = end_array[0].get('time')
                    end_date = end_array[0].get('date')

                    end = pd.to_datetime(end_date + ' ' + end_time)

                    delta = end - start

                    delta = delta.total_seconds()

                    delta = delta - (cube[1] * (1 / refreshRate))
                    # delta = delta - cube[1]

                    # delta = delta.total_seconds()

                    timeArray.append(delta)

                    print('For Proband: ' + str(p) + '\t' + str(cube[0]) + '\t Time: ' + str(delta))

    return timeArray


""" Gibt alle SF Tupel zurück """


def runAnaStartAction(proband, scene, device, cube):
    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Hover Start Interactable',
                         'actionvalue': cube,
                         'prob': proband
                         })

    array = list(array)

    return array

def runAnaFinishAction(proband, scene, device, cube):
    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Hover successfully finished',
                         'actionvalue': cube,
                         'prob': proband
                         })

    array = list(array)

    return array






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

    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
                'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
                'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    # probands = ['A16']

    print(probands)

    rrMQ2 = 120
    rrMQP = 90

    sceneName = 'ILM_Point_Left'
    devices = ['MQ2']
    PO_MQ_Left_MQ2 = runAnalyzeCubes(probands, sceneName, devices, rrMQ2)
    writeToDb('PO_MQ_Left_MQ2', PO_MQ_Left_MQ2)

    sceneName = 'ILM_Point_Right'
    PO_MQ_Right_MQ2 = runAnalyzeCubes(probands, sceneName, devices, rrMQ2)
    writeToDb('PO_MQ_Right_MQ2', PO_MQ_Right_MQ2)

    sceneName = 'ILM_Point_Left'
    devices = ['MQP']
    PO_MQ_Left_MQP = runAnalyzeCubes(probands, sceneName, devices, rrMQP)
    writeToDb('PO_MQ_Left_MQP', PO_MQ_Left_MQP)

    sceneName = 'ILM_Point_Right'
    PO_MQ_Right_MQP = runAnalyzeCubes(probands, sceneName, devices, rrMQP)
    writeToDb('PO_MQ_Right_MQP', PO_MQ_Right_MQP)

    PO_MQ_Right = [PO_MQ_Right_MQ2, PO_MQ_Right_MQP]
    PO_MQ_Right = aggregateData(PO_MQ_Right)
    writeToDb('PO_MQ_Right', PO_MQ_Right)

    PO_MQ_Left = [PO_MQ_Left_MQ2, PO_MQ_Left_MQP]
    PO_MQ_Left = aggregateData(PO_MQ_Left)
    writeToDb('PO_MQ_Left', PO_MQ_Left)

    PO_MQ = [PO_MQ_Right, PO_MQ_Left]
    PO_MQ = aggregateData(PO_MQ)
    writeToDb('P-Ad', PO_MQ)

    allBoxplot = [PO_MQ_Right_MQ2, PO_MQ_Right_MQP, PO_MQ_Left_MQ2, PO_MQ_Left_MQP, PO_MQ_Right, PO_MQ_Left, PO_MQ]


    # descArray = ['Rechts HL2', 'Rechts HPG2', 'Links HL2', 'Links HPG2', 'Rechts', 'Links', 'Gesamt']
    descArray = ['P-Ad-MQ2-R', 'P-Ad-MQP-R', 'P-Ad-MQ2-L', 'P-Ad-MQP-L', 'P-Ad-R', 'P-Ad-L', 'P-Ad']

    num, val, df = gf.setXTicks_param(allBoxplot, descArray)

    fig, axs = plt.subplots(1, 1, figsize=(10, 8))
    plt.title('Android: Bearbeitungszeit des Point-Operators', fontsize=15)
    # plt.boxplot(allBoxplot, showmeans=True)

    sns.violinplot(allBoxplot, showmeans=True, color="skyblue")
    sns.swarmplot(allBoxplot, color="black")

    axs.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    ttable = table(axs, df, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)

    plt.xticks([])
    plt.ylabel('Sekunden', fontsize=12)

    plt.show()

    # Noch Auswirkung für die einzelnen Würfel machen!


