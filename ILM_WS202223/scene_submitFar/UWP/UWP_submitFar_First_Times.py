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


def runAnalyzeElementSteps(probands, sceneName, device):
    timeArray = []

    for p in probands:

        for d in device:

            i = runAnalyzeCompletion(p, sceneName, d)
            sf_array = runAnalyzeSubmitFarArray(p, sceneName, d)

            if (i == 10):


                sf_array_start = runAnalyzeSubmitFarArrayFirst(p, sceneName, d)
                # sf_array = runAnalyzeSubmitFarArray(p, sceneName, d)

                start_time = sf_array_start[0].get('time')
                start_date = sf_array_start[0].get('date')

                start = pd.to_datetime(start_date + ' ' + start_time)

                end_time = sf_array[0].get('time')
                end_date = sf_array[0].get('date')

                end = pd.to_datetime(end_date + ' ' + end_time)

                delta = end - start

                timeArray.append(delta.total_seconds())

    return timeArray


""" Gibt alle SF Tupel zurück """



def runAnalyzeSubmitFarArrayFirst(proband, scene, device):
    sf_array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Start Scene',
                         'actionvalue': scene,
                         'prob': proband
                         })

    sf_array = list(sf_array)

    return sf_array

def runAnalyzeSubmitFarArray(proband, scene, device):
    sf_array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Submit Far',
                         'prob': proband
                         })

    sf_array = list(sf_array)

    return sf_array


""" Iteriert alle Probanden für Check ob diese alle Elemente geklickt haben """


def runAnalyzeCompletionForAllProbands(probands, scene, device):
    for p in probands:
        runAnalyzeCompletion(p, scene, device)


""" Prüft pro Proband alle Elemente """


def runAnalyzeCompletion(proband, scene, device):
    i = 0

    elements = ['Cube_1', 'Cube_2', 'Cube_3', 'Cube_4', 'Cube_5', 'Capsule_1', 'Capsule_2', 'Sphere_1', 'Sphere_2',
                'Sphere_3']

    for e in elements:
        if runAnalyzeCompletionElement(scene, device, e, proband):
            i = i + 1

    print("For Proband: " + str(proband) + ' : ' + str(i))

    return i


""" Aufruf auf DB ob Proband ein Element geklickt hat """


def runAnalyzeCompletionElement(scene, device, element, probandId):
    x = col.find({'scene': scene,
                  'dev': device,
                  'actionvalue': element,
                  'prob': probandId
                  })

    x_list = list(x)

    if len(x_list) > 0:
        return True
    else:
        return False


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
    print(probands)

    sceneName = 'ILM_Submit-Far_Right'
    devices = ['HPG2']
    SF_UWP_Left_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices)
    devices = ['HL2']
    SF_UWP_Left_HL2 = runAnalyzeElementSteps(probands, sceneName, devices)


    print(SF_UWP_Left_HL2)



    sceneName = 'ILM_Submit-Far_Right'
    devices = ['HPG2']
    SF_UWP_Right_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices)
    devices = ['HL2']
    SF_UWP_Right_HL2 = runAnalyzeElementSteps(probands, sceneName, devices)

    writeToDb('SF_UWP_R_HPG2_first', SF_UWP_Right_HPG2)
    writeToDb('SF_UWP_L_HPG2_first', SF_UWP_Left_HPG2)

    writeToDb('SF_UWP_R_HL2_first', SF_UWP_Right_HL2)
    writeToDb('SF_UWP_L_HL2_first', SF_UWP_Left_HL2)

    SF_UWP_Right = [SF_UWP_Right_HL2, SF_UWP_Right_HPG2]
    SF_UWP_Right = aggregateData(SF_UWP_Right)

    SF_UWP_Left = [SF_UWP_Left_HL2, SF_UWP_Left_HPG2]
    SF_UWP_Left = aggregateData(SF_UWP_Left)

    writeToDb('SF_UWP_R_first', SF_UWP_Right)
    writeToDb('SF_UWP_L_first', SF_UWP_Left)

    SF_UWP_ALL = [SF_UWP_Right, SF_UWP_Left]
    SF_UWP_ALL = aggregateData(SF_UWP_ALL)

    writeToDb('SF_UWP_ALL_first', SF_UWP_ALL)

    allBoxplot = [SF_UWP_Right_HL2, SF_UWP_Right_HPG2,
                  SF_UWP_Left_HL2, SF_UWP_Left_HPG2,
                  SF_UWP_Right, SF_UWP_Left,
                  SF_UWP_ALL]

    # fig = plt.subplot(figsize=(10, 8))

    descArray = ['Rechts HL2', 'Rechts HPG2', 'Links HL2', 'Links HPG2', 'Rechts', 'Links', 'Gesamt']

    num, val = setXTicks_param(allBoxplot, descArray)

    plt.title('Bearbeitungszeit nachgelagerte Schalftlächen UWP')
    plt.boxplot(allBoxplot, showmeans=True)

    plt.xticks(num, val)
    plt.ylabel('Sekunden')

    plt.show()




