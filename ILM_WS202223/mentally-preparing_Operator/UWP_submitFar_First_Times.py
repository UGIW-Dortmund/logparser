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



def getDelta(start_array, end_array):
    point_start_time = start_array[0].get('time')
    point_start_date = start_array[0].get('date')

    point_start = pd.to_datetime(point_start_date + ' ' + point_start_time)

    end_time = end_array[0].get('time')
    end_date = end_array[0].get('date')

    point_end = pd.to_datetime(end_date + ' ' + end_time)

    point_delta = point_end - point_start
    point_delta = point_delta.total_seconds()

    return point_delta



def runAnalyzeElementSteps(probands, device):
    timeArray = []

    pointArray = []
    gazeArray = []
    grabRightArray = []

    for p in probands:

        for d in device:

            # ILM Point
            point_start_array = runAnalyzeStartScene(p, 'ILM_Point', d)
            point_end_array = runAnalyzeTaskPoint(p, 'ILM_Point', d)

            if ((len(point_start_array) > 0) and len(point_end_array) > 0):

                point_delta = getDelta(point_start_array, point_end_array)
                # print('Point for Proband ' + str(p) + ' Delta Time: ' + str(point_delta))

                timeArray.append(point_delta)
                pointArray.append(point_delta)




            # ILM Gaze
            gaze_start_array = runAnalyzeStartScene(p, 'ILM_Gaze', d)
            gaze_end_array = runAnalyzeTaskGaze(p, 'ILM_Gaze', d)


            if ((len(gaze_start_array) > 0) and len(gaze_end_array) > 0):

                gaze_delta = getDelta(gaze_start_array, gaze_end_array)
                # print('Gaze for Proband ' + str(p) + ' Delta Time: ' + str(gaze_delta))

                timeArray.append(gaze_delta)
                gazeArray.append(gaze_delta)




            # ILM Grab Right
            grabRight_start_array = runAnalyzeSetScene(p, 'ILM_Grab_Right', d)
            grabRight_end_array = runAnalyzeTaskGrab(p, 'ILM_Grab_Right', d)
            

            if ((len(grabRight_start_array) > 0) and len(grabRight_end_array) > 0):

                grabRight_delta = getDelta(grabRight_start_array, grabRight_end_array)
                print('Grab Right for Proband ' + str(p) + ' Delta Time: ' + str(grabRight_delta))

                timeArray.append(grabRight_delta)
                grabRightArray.append(grabRight_delta)








    return timeArray


""" Gibt alle SF Tupel zurück """



def runAnalyzeStartScene(proband, scene, device):
    sf_array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Start Scene',
                         'actionvalue': scene,
                         'prob': proband
                         })

    sf_array = list(sf_array)

    return sf_array


def runAnalyzeSetScene(proband, scene, device):
    sf_array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Set Scene',
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


def runAnalyzeTaskPoint(proband, scene, device):
    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Point Count Start',
                         'prob': proband
                         })

    array = list(array)

    return array



def runAnalyzeTaskGaze(proband, scene, device):

    # Kann wsl das Schlüsselwort 'object' nicht lesen.
    # Hoffe das T1_Cube alles abdeckt

    array = col.find({'scene': scene,
                         'dev': device,
                         'actionvalue': 'T1_Cube',
                         'prob': proband
                         })

    array = list(array)

    return array



def runAnalyzeTaskGrab(proband, scene, device):


    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Cube Position Start',
                         'prob': proband
                         })

    array = list(array)

    return array





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

    devices = ['HL2']
    SF_UWP_Left_HPG2 = runAnalyzeElementSteps(probands, devices)

    '''
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

    plt.title('Bearbeitungszeit ersten Schalftlächen UWP')
    plt.boxplot(allBoxplot, showmeans=True)

    plt.xticks(num, val)
    plt.ylabel('Sekunden')

    plt.show()
    '''



