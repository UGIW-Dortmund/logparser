import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean

from pymongo import MongoClient
import sys
sys.path.append('/ILM_WS202223')



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

    dto = {"name": name, "values": value}
    tresor.insert_one(dto)

def runAnalyzeElementSteps(probands, sceneName, devices, hand):

    valArray = []

    step1 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'T1_Cube', 'L1_Sphere')
    step2 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'L1_Sphere', 'B1_Cube')
    step3 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'B1_Cube', 'R1_Cube')
    step4 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'R1_Cube', 'B2_Capsule')
    step5 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'B2_Capsule', 'T2_Capsule')
    step6 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'T2_Capsule', 'R2_Cube')
    step7 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'R2_Cube', 'R3_Capsule')
    step8 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'R3_Capsule', 'L2_Cube')
    step9 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'L2_Cube', 'L3_Capsule')
    step10 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'L3_Capsule', 'T3_Sphere')
    step11 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'T3_Sphere', 'R4_Sphere')
    step12 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'R4_Sphere', 'L4_Cube')
    step13 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'L4_Cube', 'B3_Sphere')
    step14 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'B3_Sphere', 'R5_Cube')
    step15 = runAnalyzeGeneric(probands, sceneName, devices, hand, 'R5_Cube', 'L5_Sphere')

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
    valArray.append(step12)
    valArray.append(step13)
    valArray.append(step14)
    valArray.append(step15)

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

    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
                'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19',  'A20',
                'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']



    print(probands)

    sceneName = 'ILM_Gaze'
    devices = ['HPG2']
    hand = 'Generic'
    sceneGaze_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Ga-Wi-HPG2', sceneGaze_HPG2)

    sceneName = 'ILM_Gaze'
    devices = ['HL2']

    sceneGaze_HL2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Ga-Wi-HL2', sceneGaze_HL2)



    print(sceneGaze_HL2)
    allTimes = sceneGaze_HPG2


    fig, axs = plt.subplots(2, 1, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit der Buttons')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0].boxplot(sceneGaze_HL2, notch=False)
    # axs[0].sns.violinplot(sceneGaze_HL2, showmeans=True, color="skyblue")
    # axs[0].sns.swarmplot(sceneGaze_HL2, color="black")
    axs[1].boxplot(sceneGaze_HPG2, notch=False)
    axs[1].sharey(axs[0])

    axs[0].set(ylabel='Sekunden')
    axs[1].set(ylabel='Sekunden')


    xtick_HL = []

    for elem in sceneGaze_HL2:
        s = boxplotCap(elem)

        xtick_HL.append(s)

    axs[0].set_title('Gaze mit der HoloLens 2')
    axs[0].set_xticks(xtick_HL)

    axs[1].set_title('Gaze mit der Reverb G2')


    plt.show()


