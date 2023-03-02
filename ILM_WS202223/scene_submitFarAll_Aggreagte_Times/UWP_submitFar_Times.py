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




def runAnalyzeGeneric(probands, sceneName, devices, hand, fromElement, toElement):

    allData = []

    for prob in probands:

        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'hand': hand,
                            'actionvalue': fromElement,
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:
                # print(x_list[0])
                # print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'hand': hand,
                              'actionvalue': toElement,
                              'prob': probandId,
                              })

                y_list = list(y)

                # print('Y-List' + str(y_list))

                if len(y_list) > 0:

                    endAction = y_list[0].get('time')
                    endDate = y_list[0].get('date')

                    endAction = pd.to_datetime(endDate + ' ' + endAction)
                    startAction = pd.to_datetime(startDate + ' ' + startAction)

                    delta = endAction - startAction
                    # float(delta.seconds + '.' + delta.)
                    allData.append(delta.total_seconds())

                    print("Proband" + str(y_list[0].get('prob')))

                    print("Device" + str(y_list[0].get('dev')))

                    print("Delta" + str(delta))

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

    dto = {"name": name, "values": value}
    tresor.insert_one(dto)

def runAnalyzeElementSteps(probands, sceneName, devices, hand):

    valArray = []

    step1 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'startButton', 'Cube_1')
    step2 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Cube_1', 'Capsule_1')
    step3 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Capsule_1', 'Cube_3')
    step4 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Cube_3', 'Sphere_2')
    step5 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Sphere_2', 'Cube_5')
    step6 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Cube_5', 'Sphere_3')
    step7 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Sphere_3', 'Cube_4')
    step8 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Cube_4', 'Capsule_2')
    step9 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Capsule_2', 'Cube_2')
    step10 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'Cube_2', 'Sphere_1')

    valArray.append(step1)
    valArray.append(step2)
    valArray.append(step3)
    valArray.append(step4)
    valArray.append(step5)
    valArray.append(step6)
    valArray.append(step7)
    valArray.append(step8)
    valArray.append(step9)
    valArray.append(step10)

    # valArray = aggregateData(valArray)

    return valArray



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
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24,' 'A25', 'A26', 'A27', 'A28']
    print(probands)

    sceneName = 'ILM_Submit-Far_Right'
    devices = ['HPG2']
    hand = 'Right'
    sceneSubmitFar_Right_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    # writeToDb('SF_UWP_R_HPG2', sceneSubmitFar_Right_HPG2)

    sceneName = 'ILM_Submit-Far_Right'
    devices = ['HL2']
    hand = 'Right'
    sceneSubmitFar_Right_HL2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    # writeToDb('SF_UWP_R_HPG2', sceneSubmitFar_Right_HPG2)



    print(sceneSubmitFar_Right_HPG2)
    allTimes = sceneSubmitFar_Right_HPG2


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

    '''

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
    '''


    plt.show()


