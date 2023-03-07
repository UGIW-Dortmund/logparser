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


def runAnalyzeGeneric(probands, sceneName, devices, hand, fromElement, toElement):
    allData = []

    for prob in probands:

        for ger in devices:
            probandId = prob

            x = col.find({'scene': sceneName,
                          'dev': ger,
                          'hand': hand,
                          'action': 'Set oElement',
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
                              'action': 'Set oElement',
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





def runAnalyzeElementSteps(probands, sceneName, devices, hand):
    valArray = []

    step1 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnL1', 'btnR1')
    step2 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnR1', 'btnD3')
    step3 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnD3', 'btnD2')
    step4 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnD2', 'btnL3')
    step5 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnL3', 'btnD4')
    step6 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnD4', 'btnR3')
    step7 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnR3', 'btnR4')
    step8 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnR4', 'btnD1')
    step9 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnD1', 'btnL4')
    step10 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnL4', 'btnR2')
    step11 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'btnR2', 'btnL2')


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
    valArray.append(step11)


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
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    probands = ['A06', 'A12', 'A28']
    print(probands)

    # MQ2
    sceneName = 'ILM_Snap_Right'
    devices = ['MQ2']
    hand = 'Right'
    sceneGaze_R_MQ2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Gaze_AD_R_MQ2', sceneGaze_R_MQ2)

    sceneName = 'ILM_Snap_Left'
    hand = 'Left'
    sceneGaze_L_MQ2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Gaze_AD_L_MQ2', sceneGaze_L_MQ2)




    # MQP
    sceneName = 'ILM_Snap_Right'
    devices = ['MQP']
    hand = 'Right'
    sceneGaze_R_MQP = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Gaze_AD_R_MQP', sceneGaze_R_MQP)

    sceneName = 'ILM_Snap_Left'
    hand = 'Left'
    sceneGaze_L_MQP = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Gaze_AD_L_MQP', sceneGaze_L_MQP)


    sceneGaze_R_MQP = aggregateData(sceneGaze_R_MQP)
    sceneGaze_L_MQP = aggregateData(sceneGaze_L_MQP)


    box_selectedProbands = [sceneGaze_R_MQP, sceneGaze_L_MQP]


    print(sceneGaze_L_MQ2)


    allTimes = sceneGaze_R_MQ2

    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    fig.suptitle('Bearbeitungszeit der Buttons')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0].boxplot(box_selectedProbands, notch=False)
    axs[0].set_xticks([1, 2], ["Rechte Hand" + boxplotCap(box_selectedProbands[0]),
                               "Linke Hand" + boxplotCap(box_selectedProbands[1])])


    axs[1].boxplot(sceneGaze_R_MQP, notch=False)
    axs[1].sharey(axs[0])
    # axs[1].set_xticks([1], boxplotCap(sceneGaze_R_MQP))


    axs[0].set(ylabel='Sekunden')
    axs[1].set(ylabel='Sekunden')


    axs[0].set_title('Gaze mit der MS HoloLens 2')
    # axs[0].set_xticks(xtick_HL)

    axs[1].set_title('Gaze mit der HP Reverb G2')


    plt.show()


