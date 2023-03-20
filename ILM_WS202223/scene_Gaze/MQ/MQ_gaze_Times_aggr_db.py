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


def setXTicks_param(valArray, descArray):
    xtick = []
    i = 0

    # The descirption of fields
    for elem in valArray:
        s = boxplotCap(elem)

        if arrayDescr:
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
    probands = ['A06', 'A12', 'A28']

    # sceneGaze_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    sceneGaze_R_MQP = tresor.find_one({'name': 'Gaze_AD_R_MQP'})
    sceneGaze_L_MQP = tresor.find_one({'name': 'Gaze_AD_L_MQP'})
    sceneGaze_R_MQ2 = tresor.find_one({'name': 'Gaze_AD_R_MQ2'})
    sceneGaze_L_MQ2 = tresor.find_one({'name': 'Gaze_AD_L_MQ2'})

    sceneGaze_R_MQP = convertToFloat(sceneGaze_R_MQP)
    sceneGaze_L_MQP = convertToFloat(sceneGaze_L_MQP)
    sceneGaze_R_MQ2 = convertToFloat(sceneGaze_R_MQ2)
    sceneGaze_L_MQ2 = convertToFloat(sceneGaze_L_MQ2)

    sceneGaze_R_MQP = aggregateData(sceneGaze_R_MQP)
    sceneGaze_L_MQP = aggregateData(sceneGaze_L_MQP)
    sceneGaze_R_MQ2 = aggregateData(sceneGaze_R_MQ2)
    sceneGaze_L_MQ2 = aggregateData(sceneGaze_L_MQ2)

    box_MQP = [sceneGaze_R_MQP, sceneGaze_L_MQP]
    box_MQ2 = [sceneGaze_R_MQ2, sceneGaze_L_MQ2]

    box_R = [sceneGaze_R_MQP, sceneGaze_R_MQ2]
    box_L = [sceneGaze_L_MQP, sceneGaze_L_MQ2]

    writeToDb("Gaze_AD_MQP", box_MQP)
    writeToDb("Gaze_AD_MQ2", box_MQ2)

    writeToDb("Gaze_AD_R", box_R)
    writeToDb("Gaze_AD_L", box_L)


    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    fig.suptitle('')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0, 0].violinplot(box_MQP)
    axs[1, 0].violinplot(box_MQ2)

    axs[0, 1].violinplot(box_R)
    axs[1, 1].violinplot(box_L)


    axs[0, 1].sharey(axs[0, 0])
    axs[1, 1].sharey(axs[0, 0])
    axs[1, 0].sharey(axs[0, 0])



    axs[0, 0].set(ylabel='Sekunden')
    axs[0, 1].set(ylabel='Sekunden')
    axs[1, 0].set(ylabel='Sekunden')
    axs[1, 1].set(ylabel='Sekunden')

    arrayDescr = ['Rechte Hand', 'Linke Hand']

    (e_R_MQP, x_R_MQP) = setXTicks_param(box_MQP, arrayDescr)
    (e_L_MQP, x_L_MQP) = setXTicks_param(box_MQ2, arrayDescr)

    arrayDescr = ['Meta Quest Pro', 'Meta Quest 2']

    (e_R_MQ2, x_R_MQ2) = setXTicks_param(box_R, arrayDescr)
    (e_L_MQ2, x_L_MQ2) = setXTicks_param(box_L, arrayDescr)

    axs[0, 0].set_title('Gaze mit der MQP')
    axs[0, 0].set_xticks(e_R_MQP, x_R_MQP)

    axs[1, 0].set_title('Gaze mit der MQP')
    axs[1, 0].set_xticks(e_L_MQP, x_L_MQP)

    axs[0, 1].set_title('Gaze mit der rechten Hand')
    axs[0, 1].set_xticks(e_R_MQ2, x_R_MQ2)

    axs[1, 1].set_title('Gaze mit der linken Hand')
    axs[1, 1].set_xticks(e_L_MQ2, x_L_MQ2)

    plt.show()


