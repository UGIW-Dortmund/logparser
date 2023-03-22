import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
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
    return f'\n n = {len(valArray)} \n' \
           f'Me. = {round(statistics.median(valArray), 3)} s \n ' \
           f'Mi. = {round(statistics.mean(valArray), 2)}s \n ' \
            f'S. Abw. = {round(statistics.stdev(valArray), 3)} s \n ' \
            f'M. Abw. = {round(mean(valArray), 3)} s \n ';

def convertToFloat(arr):

    arr = arr.get('values')

    print(arr)

    arr = list(arr)
    lenArray = len(arr)

    print(lenArray)

    allValues = []

    for e in range(0, lenArray):
        floatValues = []

        for elem in arr[e]:
            floatValues.append(float(elem))

        allValues.append(floatValues)

    return allValues


def convertToFloat1D(arr):

    arr = arr.get('values')
    arr = list(arr)
    lenArray = len(arr)


    allValues = []

    for elem in arr:
        allValues.append(float(elem))


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

    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
                'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
                'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']


    # sceneGaze_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    sceneGaze_R_MQP = tresor.find_one({'name': 'Gaze_AD_R_MQP'})
    sceneGaze_L_MQP = tresor.find_one({'name': 'Gaze_AD_L_MQP'})
    sceneGaze_R_MQ2 = tresor.find_one({'name': 'Gaze_AD_R_MQ2'})
    sceneGaze_L_MQ2 = tresor.find_one({'name': 'Gaze_AD_L_MQ2'})

    sceneGaze_HL2_first = tresor.find_one({'name': 'Gaze_UWP_HL2_first'})
    sceneGaze_HL2_second = tresor.find_one({'name': 'Gaze_UWP_HL2_second'})

    sceneGaze_HPG2_first = tresor.find_one({'name': 'Gaze_UWP_HPG2_first'})
    sceneGaze_HPG2_second = tresor.find_one({'name': 'Gaze_UWP_HPG2_second'})

    Ga_Ad = tresor.find_one({'name': 'Ga-Ad'})
    Ga_Ad = convertToFloat1D(Ga_Ad)

    Ga_1_Wi_HPG2 = tresor.find_one({'name': 'Ga-1-Wi-HPG2'})
    Ga_1_Wi_HPG2 = convertToFloat1D(Ga_1_Wi_HPG2)

    Ga_2_Wi_HPG2 = tresor.find_one({'name': 'Ga-2-Wi-HPG2'})
    Ga_2_Wi_HPG2 = convertToFloat1D(Ga_2_Wi_HPG2)

    Ga_VR = [Ga_Ad, Ga_1_Wi_HPG2, Ga_2_Wi_HPG2]
    Ga_VR = aggregateData(Ga_VR)




    sceneGaze_R_MQP = convertToFloat(sceneGaze_R_MQP)
    sceneGaze_L_MQP = convertToFloat(sceneGaze_L_MQP)
    sceneGaze_R_MQ2 = convertToFloat(sceneGaze_R_MQ2)
    sceneGaze_L_MQ2 = convertToFloat(sceneGaze_L_MQ2)

    sceneGaze_HL2_first = convertToFloat1D(sceneGaze_HL2_first)
    sceneGaze_HL2_second = convertToFloat1D(sceneGaze_HL2_second)
    sceneGaze_HPG2_first = convertToFloat1D(sceneGaze_HPG2_first)
    sceneGaze_HPG2_second = convertToFloat1D(sceneGaze_HPG2_second)


    sceneGaze_R_MQP = aggregateData(sceneGaze_R_MQP)
    sceneGaze_L_MQP = aggregateData(sceneGaze_L_MQP)
    sceneGaze_R_MQ2 = aggregateData(sceneGaze_R_MQ2)
    sceneGaze_L_MQ2 = aggregateData(sceneGaze_L_MQ2)



    # Aggregieren der Daten
    operatorGaze_second = [sceneGaze_R_MQP, sceneGaze_L_MQP, sceneGaze_R_MQ2, sceneGaze_L_MQ2, sceneGaze_HL2_second, sceneGaze_HPG2_second]

    operatorGaze_UWP_second = [sceneGaze_HL2_second, sceneGaze_HPG2_second]
    operatorGaze_AD_second = [sceneGaze_R_MQP, sceneGaze_L_MQP, sceneGaze_R_MQ2, sceneGaze_L_MQ2]

    operatorGaze_first = [sceneGaze_HL2_first, sceneGaze_HPG2_first]

    operatorGaze_first = aggregateData(operatorGaze_first)
    operatorGaze_second = aggregateData(operatorGaze_second)

    operatorGaze_UWP_second = aggregateData(operatorGaze_UWP_second)
    operatorGaze_AD_second = aggregateData(operatorGaze_AD_second)

    writeToDb("Gaze_first", operatorGaze_first)
    writeToDb("Gaze_second", operatorGaze_second)

    writeToDb("Gaze_AD_second", operatorGaze_AD_second)
    writeToDb("Gaze_UWP_second", operatorGaze_UWP_second)

    writeToDb("Ga-VR", Ga_VR)
    writeToDb("Ga-AR-1", sceneGaze_HL2_first)
    writeToDb("Ga-AR-2", sceneGaze_HL2_second)


    operatorGaze = [operatorGaze_AD_second, operatorGaze_UWP_second, Ga_VR]


    print("Operator Gaze")
    print(operatorGaze)



    box_MQP = [sceneGaze_R_MQP, sceneGaze_L_MQP]
    box_MQ2 = [sceneGaze_R_MQ2, sceneGaze_L_MQ2]

    box_R = [sceneGaze_R_MQP, sceneGaze_R_MQ2]
    box_L = [sceneGaze_L_MQP, sceneGaze_L_MQ2]

    writeToDb("Gaze_AD_MQP", box_MQP)
    writeToDb("Gaze_AD_MQ2", box_MQ2)

    writeToDb("Gaze_AD_R", box_R)
    writeToDb("Gaze_AD_L", box_L)



    ### Graphic
    fig, axs = plt.subplots(1, 1, figsize=(10, 8))

    fig.suptitle('Bearbeitungszeit mit dem nachgelagerten Schaltflächen des Gaze-Operators: Gesamt mit HPG2, MQ2, MQP, HL2')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.violinplot(operatorGaze)

    plt.ylabel('Sekunden')
    # axs[1].set(ylabel='Sekunden')


    descArrayXTicks = ["Android Plattform", "Windows Plattform", "Ga-VR"]

    (elemALL, xALL, dfALL) = gf.setXTicks_param(operatorGaze, descArrayXTicks)

    # axs[0].set_title('Gaze mit der MS HoloLens 2')
    plt.xticks(elemALL, xALL)

    plt.show()
