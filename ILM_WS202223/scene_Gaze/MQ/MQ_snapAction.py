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







def runAnalyzeSnap(probands, sceneName, devices, searchTerm):
    allData = []

    for prob in probands:

        for ger in devices:
            probandId = prob

            x = col.find({'scene': sceneName,
                          'dev': ger,
                          'action': searchTerm,
                          'prob': probandId
                          })

            x_list = list(x)

            # Number of Gaze-Movements of each proband
            lenX_List = len(x_list)

            data = [prob, lenX_List]

            allData.append(data)

            x = None
            y = None
            y_list = None
            x_list = None

            endAction = None
            startAction = None

    return allData

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



def getDataXY(valArray):

    xArray = []
    yArray = []

    for elem in valArray:
        xArray.append(elem[0])
        yArray.append(elem[1])

    return (xArray, yArray)


# This is added so that many files can reuse the function get_database()
def boxplotCap(valArray):
    return f'\n n = {len(valArray)} \n' \
           f'Me.={round(statistics.median(valArray), 3)} s \n ' \
           f'Mi.={round(statistics.mean(valArray), 3)} s \n ';
    # f'S. Abweichung = {round(statistics.stdev(valArray), 3)} s \n ' \
    # f'M. Abweichung = {round(mean(valArray), 3)} s \n ';




def setXTicks_param(valArray, descArray):
    xtick = []
    i = 0

    # The descirption of fields
    for elem in valArray:
        xtick.append(elem)


    lenVA = len(valArray)

    # First Parameter the number of fields
    elements = []
    for elem in range(0, lenVA):
        elements.append(elem)

    return (elements, xtick)


if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]

    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']
    print(probands)

    # MQ2
    sceneName = 'ILM_Snap_Right'
    devices = ['MQ2']
    searchTerm = 'Snap Action Right'
    snap_MQ2_Right = runAnalyzeSnap(probands, sceneName, devices, searchTerm)
    x_snap_MQ2_Right, y_snap_MQ2_Right = getDataXY(snap_MQ2_Right)


    sceneName = 'ILM_Snap_Left'
    searchTerm = 'Snap Action Left'
    snap_MQ2_Left = runAnalyzeSnap(probands, sceneName, devices, searchTerm)
    x_snap_MQ2_Left, y_snap_MQ2_Left = getDataXY(snap_MQ2_Left)

    # MQP
    sceneName = 'ILM_Snap_Right'
    devices = ['MQP']
    searchTerm = 'Snap Action Right'
    snap_MQP_Right = runAnalyzeSnap(probands, sceneName, devices, searchTerm)
    x_snap_MQP_Right, y_snap_MQP_Right = getDataXY(snap_MQP_Right)

    sceneName = 'ILM_Snap_Left'
    searchTerm = 'Snap Action Left'
    snap_MQP_Left = runAnalyzeSnap(probands, sceneName, devices, searchTerm)
    x_snap_MQP_Left, y_snap_MQP_Left = getDataXY(snap_MQP_Left)


    # fig, axs = plt.subplots(1, 1, figsize=(10, 8))
    X = np.arange(len(x_snap_MQ2_Right))
    width = 0.5
    plt.ylabel("Anzahl Daumenstick-Bewegungen", fontsize=15)
    plt.xlabel("Probanden ID", fontsize=15)
    plt.title("Android: Verwendung der Daumensticks", fontsize=15)


    (e_X, x_X) = setXTicks_param(x_snap_MQP_Right, x_snap_MQP_Right)
    plt.xticks(e_X, x_X ,fontsize=12)

    print("e_X")
    print(e_X)

    print("x_X")
    print(x_X)

    plt.grid(axis='y', linestyle='-', which='major', color='lightgrey', alpha=0.5)
    plt.bar(X, y_snap_MQ2_Right, width, label="Ga-Ad-MQ2-R")
    plt.bar(X, y_snap_MQ2_Left, width, label="Ga-Ad-MQ2-L")
    plt.bar(X + width, y_snap_MQP_Right, width, label="Ga-Ad-MQP-R")
    plt.bar(X, y_snap_MQP_Left, width, label="Ga-Ad-MQP-L")
    plt.legend(prop={'size': 14})

    plt.show()

