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

    return f'\n \n n = {len(valArray)} \n' \
           f'Me. = {median} s \n ' \
           f'Mi. = {mean} s \n ' \
           f'S. Abw. = {stdev} s \n ' \
           f'u. Q. = {first_quartil} s \n ' \
           f'o. Q. = {third_quartil} s';


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


def runAnalyzeCubes(probands, sceneName, device):
    timeArray = []

    cubeArray = [['Cube_1', -4.4, 2.2], ['Cube_2', -4.3, -2.4], ['Cube_3', 1.7, 2.2], ['Cube_4', 0.3, -3.1]]

    for p in probands:

        for d in device:

            # For-Loop mit den verschiedenen Würfeln
            for cube in cubeArray:

                start_array = runAnaStartAction(p, sceneName, d, cube[0])
                end_array = runAnaFinishAction(p, sceneName, d, str(cube[0]))

                if len(start_array) > 0 and len(end_array) > 0:
                    start_time = start_array[0].get('time')
                    start_date = start_array[0].get('date')

                    start = pd.to_datetime(start_date + ' ' + start_time)

                    finItem = len(end_array) - 1
                    cube_end_position = end_array[finItem].get('actionvalue')
                    cube_end_position = str(cube_end_position).replace(')', '')
                    cube_end_position = str(cube_end_position).replace('(', '')
                    cube_end_position = str(cube_end_position).split(',')
                    cube_end_position_x = float(cube_end_position[0])
                    cube_end_position_z = float(cube_end_position[2])

                    # Bedingung das die Würfel an den richtigen Orten sind - inklusive Toleranz
                    if (cube_end_position_x >= (cube[1] - 0.2)) & (cube_end_position_x <= (cube[1] + 0.2)):

                        if (cube_end_position_z >= (cube[2] - 0.2)) & (cube_end_position_z <= (cube[2] + 0.2)):

                            end_time = end_array[finItem].get('time')
                            end_date = end_array[finItem].get('date')

                            end = pd.to_datetime(end_date + ' ' + end_time)

                            delta = end - start

                            delta = delta.total_seconds()

                            print('For Proband: ' + str(p) + '\t' + str(cube[0]) + '       End Position: x: ' + str(
                                cube_end_position_x)
                                  + '\t z: ' + str(cube_end_position_z))

                            timeArray.append(delta)




    return timeArray


""" Gibt alle SF Tupel zurück """


def runAnaStartAction(proband, scene, device, cube):
    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Cube Position Start',
                         'oelement': cube,
                         'prob': proband
                         })

    array = list(array)

    return array

def runAnaFinishAction(proband, scene, device, cube):
    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Cube Position End',
                         'oelement': cube,
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

    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    devices = ['HPG2']
    sceneName = 'ILM_Grab_Right'
    GR_UWP_Right_HPG2 = runAnalyzeCubes(probands, sceneName, devices)
    writeToDb('GR_UWP_Right_HPG2', GR_UWP_Right_HPG2)
    # print(GR_MQ_Right_MQ2)

    sceneName = 'ILM_Grab_Left'
    GR_UWP_Left_HPG2 = runAnalyzeCubes(probands, sceneName, devices)
    writeToDb('GR_UWP_Left_HPG2', GR_UWP_Left_HPG2)

    devices = ['HL2']
    sceneName = 'ILM_Grab_Right'
    GR_UWP_Right_HL2 = runAnalyzeCubes(probands, sceneName, devices)
    writeToDb('GR_UWP_Right_HL2', GR_UWP_Right_HL2)

    sceneName = 'ILM_Grab_Left'
    GR_UWP_Left_HL2 = runAnalyzeCubes(probands, sceneName, devices)
    writeToDb('GR_UWP_Left_HL2', GR_UWP_Left_HL2)


    GR_UWP_Right = [GR_UWP_Right_HPG2, GR_UWP_Right_HL2]
    GR_UWP_Right = aggregateData(GR_UWP_Right)
    writeToDb('GR_UWP_Right', GR_UWP_Right)

    GR_UWP_Left = [GR_UWP_Left_HL2, GR_UWP_Left_HPG2]
    GR_UWP_Left = aggregateData(GR_UWP_Left)
    writeToDb('GR_UWP_Left', GR_UWP_Left)

    GR_UWP = [GR_UWP_Right, GR_UWP_Left]
    GR_UWP = aggregateData(GR_UWP)
    writeToDb('GR_UWP', GR_UWP)

    GR_UWP_HPG2 = [GR_UWP_Right_HPG2, GR_UWP_Left_HPG2]
    GR_UWP_HPG2 = aggregateData(GR_UWP_HPG2)
    writeToDb('GR_HPG2', GR_UWP_HPG2)

    GR_UWP_HL2 = [GR_UWP_Right_HL2, GR_UWP_Left_HL2]
    GR_UWP_HL2 = aggregateData(GR_UWP_HL2)
    writeToDb('GR_UWP_HL2', GR_UWP_HL2)


    allBoxplot = [GR_UWP_Right_HL2, GR_UWP_Right_HPG2, GR_UWP_Left_HL2, GR_UWP_Left_HPG2, GR_UWP_Right, GR_UWP_Left, GR_UWP_HL2, GR_UWP_HPG2, GR_UWP]


    # descArray = ['Rechts HL2', 'Rechts HPG2', 'Links HL2', 'Links HPG2', 'Rechts', 'Links', 'Gesamt']
    descArray = ['Rechts HL2', 'Rechts HPG2', 'Links HL2', 'Links HPG2', 'Rechts', 'Links', 'HL2', 'HPG2', 'Gesamt']

    num, val = setXTicks_param(allBoxplot, descArray)

    plt.title('Windows: Bearbeitungszeit des Grab-Operators',fontsize=15)
    plt.boxplot(allBoxplot, showmeans=True)

    plt.xticks(num, val,fontsize=12)
    plt.ylabel('Sekunden', fontsize=12)

    plt.show()

