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
    median = round(statistics.median(valArray), 1)
    median = str(median).replace('.', ',')

    mean = round(statistics.mean(valArray), 1)
    mean = str(mean).replace('.', ',')

    stdev = round(statistics.stdev(valArray), 1)
    stdev = str(stdev).replace('.', ',')

    first_quartil = round(np.percentile(valArray, 25), 1)
    first_quartil = str(first_quartil).replace('.', ',')

    third_quartil = round(np.percentile(valArray, 75), 1)
    third_quartil = str(third_quartil).replace('.', ',')

    return f'\n\n n = {len(valArray)} \n' \
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
    grabLeftArray = []
    subFarRightArray = []
    subFarLeftArray = []
    subNearRightArray = []
    subNearLeftArray = []

    for p in probands:

        for d in device:

            # ILM Point
            point_start_array = runAnalyzeStartScene(p, 'ILM_Point', d)
            point_end_array = runAnalyzeTaskPoint(p, 'ILM_Point', d)

            if ((len(point_start_array) > 0) and len(point_end_array) > 0):

                point_delta = getDelta(point_start_array, point_end_array)

                #print('Point for Proband ' + str(p) + '\t\t Delta Time: ' + str(point_delta))
                printTimes('Point Generic', p, point_delta)

                timeArray.append(point_delta)
                pointArray.append(point_delta)




            # ILM Gaze
            gaze_start_array = runAnalyzeStartScene(p, 'ILM_Gaze', d)
            gaze_end_array = runAnalyzeTaskGaze(p, 'ILM_Gaze', d)


            if ((len(gaze_start_array) > 0) and len(gaze_end_array) > 0):

                gaze_delta = getDelta(gaze_start_array, gaze_end_array)
                # print('Gaze for Proband ' + str(p) + '\t\t Delta Time: ' + str(gaze_delta))
                printTimes('Gaze Generic', p, gaze_delta)


                timeArray.append(gaze_delta)
                gazeArray.append(gaze_delta)




            # ILM Grab Right
            grabRight_start_array = runAnalyzeSetScene(p, 'ILM_Grab_Right', d)
            grabRight_end_array = runAnalyzeTaskGrab(p, 'ILM_Grab_Right', d)


            if ((len(grabRight_start_array) > 0) and len(grabRight_end_array) > 0):

                grabRight_delta = getDelta(grabRight_start_array, grabRight_end_array)
                # print('Grab Right for Proband ' + str(p) + '\t\t Delta Time: ' + str(grabRight_delta))
                printTimes('GR Right', p, grabRight_delta)

                timeArray.append(grabRight_delta)
                grabRightArray.append(grabRight_delta)






            # ILM Grab Left
            grabLeft_start_array = runAnalyzeSetScene(p, 'ILM_Grab_Left', d)
            grabLeft_end_array = runAnalyzeTaskGrab(p, 'ILM_Grab_Left', d)

            if ((len(grabLeft_start_array) > 0) and len(grabLeft_end_array) > 0):
                grabLeft_delta = getDelta(grabLeft_start_array, grabLeft_end_array)
                # print('Grab Left for Proband ' + str(p) + '\t\t Delta Time: ' + str(grabLeft_delta))
                printTimes('GR Left', p, grabLeft_delta)

                timeArray.append(grabLeft_delta)
                grabLeftArray.append(grabLeft_delta)



            # ILM Submit Far Right
            subFarRight_start_array = runAnalyzeSetScene(p, 'ILM_Submit-Far_Right', d)
            subFarRight_end_array = runAnalyzeTaskSubmitFar(p, 'ILM_Submit-Far_Right', d)

            if ((len(subFarRight_start_array) > 0) and len(subFarRight_end_array) > 0):
                subFarRight_delta = getDelta(subFarRight_start_array, subFarRight_end_array)

                # print('Sub Far Right for Proband ' + str(p) + '\t\t Delta Time: ' + str(subFarRight_delta))
                printTimes('SF Right', p, subFarRight_delta)

                timeArray.append(subFarRight_delta)
                subFarRightArray.append(subFarRight_delta)




            # ILM Submit Far Left
            subFarLeft_start_array = runAnalyzeSetScene(p, 'ILM_Submit-Far_Left', d)
            subFarLeft_end_array = runAnalyzeTaskSubmitFar(p, 'ILM_Submit-Far_Left', d)

            if ((len(subFarLeft_start_array) > 0) and len(subFarLeft_end_array) > 0):
                subFarLeft_delta = getDelta(subFarLeft_start_array, subFarLeft_end_array)

                printTimes('SF Left', p, subFarLeft_delta)

                timeArray.append(subFarLeft_delta)
                subFarLeftArray.append(subFarLeft_delta)




            # ILM Submit Near Right
            subNearRight_start_array = runAnalyzeStartScene(p, 'ILM_Submit-Near_Right', d)
            subNearRight_end_array = runAnalyzeTaskSubmitNear(p, 'ILM_Submit-Near_Right', d)

            if ((len(subNearRight_start_array) > 0) and len(subNearRight_end_array) > 0):
                subNearRight_delta = getDelta(subNearRight_start_array, subNearRight_end_array)

                printTimes('SN Right', p, subNearRight_delta)

                timeArray.append(subNearRight_delta)
                subNearRightArray.append(subNearRight_delta)




            # ILM Submit Near Left
            subNearLeft_start_array = runAnalyzeStartSubmitNear(p, 'ILM_Submit-Near_Left', d)
            subNearLeft_end_array = runAnalyzeTaskSubmitNear(p, 'ILM_Submit-Near_Left', d)

            if ((len(subNearLeft_start_array) > 0) and len(subNearLeft_end_array) > 0):
                subNearLeft_delta = getDelta(subNearLeft_start_array, subNearLeft_end_array)

                printTimes('SN Left', p, subNearLeft_delta)

                timeArray.append(subNearLeft_delta)
                subNearLeftArray.append(subNearLeft_delta)



    tempArray = []

    for elem in timeArray:
        if elem >= 0.0:
            tempArray.append(elem)

    timeArray = tempArray

    return timeArray




def printTimes(operator, p, delta):
    print('Proband ' + str(p) + '\t\t Delta Time: ' + str(delta) + "\t\t" + str(operator))

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




def runAnalyzeTaskSubmitFar(proband, scene, device):
    sf_array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Submit Far',
                         'prob': proband
                         })

    sf_array = list(sf_array)

    return sf_array




def runAnalyzeStartSubmitNear(proband, scene, device):
    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Start Scene',
                         'prob': proband
                         })

    array = list(array)

    return array


def runAnalyzeTaskSubmitNear(proband, scene, device):
    array = col.find({'scene': scene,
                         'dev': device,
                         'action': 'Submit Near',
                         'actionvalue': 'Button 1: Button Pressed',
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
    print(probands)

    devices = ['HL2']
    M_UWP_HL2 = runAnalyzeElementSteps(probands, devices)
    writeToDb('M_UWP_HL2', M_UWP_HL2)

    devices = ['HPG2']
    M_UWP_HPG2 = runAnalyzeElementSteps(probands, devices)
    writeToDb('M_UWP_HPG2', M_UWP_HPG2)


    M_UWP = [M_UWP_HL2, M_UWP_HPG2]
    M_UWP = aggregateData(M_UWP)
    writeToDb('M_UWP', M_UWP)


    allBoxplot = [M_UWP_HL2, M_UWP_HPG2, M_UWP]

    # fig = plt.subplot(figsize=(10, 8))

    descArray = ['HL2', 'HPG2', 'Gesamt']

    num, val = setXTicks_param(allBoxplot, descArray)

    plt.title('Windows: Mentale Vorbereitungszeit', fontsize=15)
    plt.boxplot(allBoxplot, showmeans=True)

    plt.xticks(num, val, fontsize=12)
    plt.ylabel('Sekunden', fontsize=12)

    plt.show()




