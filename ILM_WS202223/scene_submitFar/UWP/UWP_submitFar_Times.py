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

    dto = {"name": name, "values": value}
    tresor.insert_one(dto)




""" Ermittelt die Zeiten, welche die Probanden gebraucht haben """
def runAnalyzeElementSteps(probands, sceneName, device):

    timeArray = []

    for p in probands:

        i = runAnalyzeCompletion(p, sceneName, device)

        if (i == 10):
            sf_array = runAnalyzeSubmitFarArray(p, sceneName, device)

            start_time = sf_array[0].get('time')
            start_date = sf_array[0].get('date')

            start = pd.to_datetime(start_date + ' ' + start_time)

            end_time = sf_array[len(sf_array) - 1].get('time')
            end_date = sf_array[len(sf_array) - 1].get('date')

            end = pd.to_datetime(end_date + ' ' + end_time)

            delta = end - start

            timeArray.append(delta)

    return timeArray


""" Gibt alle SF Tupel zurück """
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

    elements = ['Cube_1', 'Cube_2', 'Cube_3', 'Cube_4', 'Cube_5', 'Capsule_1', 'Capsule_2', 'Sphere_1', 'Sphere_2', 'Sphere_3']

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
    return f'\n n = {len(valArray)} \n' \
           f'Me.={round(statistics.median(valArray), 3)} s \n ' \
           f'Mi.={round(statistics.mean(valArray), 3)} s \n ';
           # f'S. Abweichung = {round(statistics.stdev(valArray), 3)} s \n ' \
           # f'M. Abweichung = {round(mean(valArray), 3)} s \n ';

if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]

    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']
    print(probands)

    sceneName = 'ILM_Submit-Far_Left'
    devices = 'HL2'
    print(runAnalyzeElementSteps(probands, sceneName, devices))
    # runAnalyzeCompletionForAllProbands(probands, sceneName, devices)

    #sceneSubmitFar_Right_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    # writeToDb('SF_UWP_R_HPG2', sceneSubmitFar_Right_HPG2)

    sceneName = 'ILM_Submit-Far_Right'
    devices = ['HL2']
    hand = 'Right'
    # sceneSubmitFar_Right_HL2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    # writeToDb('SF_UWP_R_HPG2', sceneSubmitFar_Right_HPG2)



    #print(sceneSubmitFar_Right_HPG2)
    #allTimes = sceneSubmitFar_Right_HPG2

    '''
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit der Buttons')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0, 0].boxplot(allTimes, notch=False)
    axs[0, 1].boxplot(sceneSubmitFar_Right_HL2, notch=False)
    axs[0, 1].sharey(axs[0, 0])

    axs[1, 0].boxplot(allTimes)
    axs[1, 0].sharey(axs[0, 0])

    axs[1, 1].boxplot(allTimes)
    axs[1, 1].sharey(axs[0, 0])

    axs[0, 0].set(ylabel='Sekunden')
    axs[0, 1].set(ylabel='Sekunden')
    axs[1, 0].set(ylabel='Sekunden')
    axs[1, 1].set(ylabel='Sekunden')

   

    axs[0, 0].set_title('1. Szene: Rechte Hand - HPG2')
    axs[0, 0].set_xticks([1, 2, 3], ["Button 1" + boxplotCap(allTimes[0]),
                                           "Checkbox 1" + boxplotCap(allTimes[1]),
                                           "Button 2" + boxplotCap(allTimes[2])])

    axs[1, 0].set_title('1. Szene: Rechte Hand - HL2')
    axs[1, 0].set_xticks([1, 2, 3], ["Button 1" + boxplotCap(allTimes[0]),
                                              "Checkbox 1" + boxplotCap(allTimes[1]),
                                              "Button 2" + boxplotCap(allTimes[2])])

    axs[0, 1].set_title('2. Szene: Linke Hand - HPG2')
    axs[0, 1].set_xticks([1, 2, 3], ["Button 1" + boxplotCap(allTimes[0]),
                                        "Checkbox 1" + boxplotCap(allTimes[1]),
                                        "Button 2" + boxplotCap(allTimes[2])])

    axs[1, 1].set_title('2. Szene: Linke Hand - HL2')
    axs[1, 1].set_xticks([1, 2, 3], ["Button 1" + boxplotCap(allTimes[0]),
                                              "Checkbox 1" + boxplotCap(allTimes[1]),
                                              "Button 2" + boxplotCap(allTimes[2])])
    

    plt.show()


    '''
