import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import seaborn as sns
from pandas.plotting import table
import sys
sys.path.append('/ILM_WS202223')
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


def aggregateDataOneDimension(array):
    lenArray = len(array)
    print("Len array " + str(lenArray))
    data = []

    for i in range(0, lenArray):
        for elem in array[i]:
            data.append(elem)

    return data;

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
           f'Median ={round(statistics.median(valArray), 3)} s \n ' \
           f'Mittelwert ={round(statistics.mean(valArray), 3)} s \n '\
            f'S. Abw. = {round(statistics.stdev(valArray), 3)} s \n ' \
            f'M. Abw. = {round(mean(valArray), 3)} s \n ' \
           f'1Q = {round(np.percentile(valArray, 25), 3)} s \n' \
           f'3Q = {round(np.percentile(valArray, 75), 3)} s ';


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
        xtick.append(descArray[i] + "\n" + s)
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

    sceneName = 'ILM_Gaze'
    devices = ['HPG2']
    hand = 'Generic'
    # sceneGaze_HPG2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    sceneGaze_HPG2 = tresor.find_one({'name': 'Gaze_UWP_HPG2'})
    #print(sceneGaze_HPG2.get('values'))
    sceneGaze_HPG2 = convertToFloat(sceneGaze_HPG2)

    print("Länge")
    print(len(sceneGaze_HPG2))

    sceneGaze_HPG2_first = [sceneGaze_HPG2[0], sceneGaze_HPG2[1]]
    sceneGaze_HPG2_second = []

    for e in range(2, len(sceneGaze_HPG2)):
        sceneGaze_HPG2_second.append(sceneGaze_HPG2[e])



    sceneGaze_HPG2_first = aggregateData(sceneGaze_HPG2_first)
    sceneGaze_HPG2_second = aggregateData(sceneGaze_HPG2_second)

    print("second")
    print(sceneGaze_HPG2_second)

    writeToDb("Gaze_UWP_HPG2_first", sceneGaze_HPG2_first)

    writeToDb("Gaze_UWP_HPG2_second", sceneGaze_HPG2_second)

    box_sceneGaze_HPG2 = [sceneGaze_HPG2_first, sceneGaze_HPG2_second]


    devices = ['HL2']

    # sceneGaze_HL2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    sceneGaze_HL2 = tresor.find_one({'name': 'Gaze_UWP_HL2'})
    sceneGaze_HL2 = convertToFloat(sceneGaze_HL2)

    sceneGaze_HL2_first = [sceneGaze_HL2[0], sceneGaze_HL2[1]]
    sceneGaze_HL2_second = []

    for e in range(2, len(sceneGaze_HL2)):
        sceneGaze_HL2_second.append(sceneGaze_HL2[e])

    # Flatten the data
    sceneGaze_HL2_first = aggregateData(sceneGaze_HL2_first)
    sceneGaze_HL2_second = aggregateData(sceneGaze_HL2_second)

    writeToDb("Gaze_UWP_HL2_first", sceneGaze_HL2_first)
    writeToDb("Gaze_UWP_HL2_second", sceneGaze_HL2_second)

    box_sceneGaze_HL2 = [sceneGaze_HL2_first, sceneGaze_HL2_second]

    Ga_1_Wi = [sceneGaze_HL2_first, sceneGaze_HPG2_first]
    Ga_1_Wi = aggregateData(Ga_1_Wi)
    writeToDb('Ga_1_Wi', Ga_1_Wi)

    Ga_2_Wi = [sceneGaze_HL2_second, sceneGaze_HPG2_second]
    Ga_2_Wi = aggregateData(Ga_2_Wi)
    writeToDb('Ga_2_Wi', Ga_2_Wi)

    Ga_Wi = [Ga_1_Wi, Ga_2_Wi]


    ### Graphic
    fig, axs = plt.subplots(1, 3, figsize=(10, 8))

    fig.suptitle('Bearbeitungszeit mit dem Gaze-Operator')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    # axs[0].violinplot(box_sceneGaze_HPG2)
    sns.violinplot(box_sceneGaze_HPG2, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(box_sceneGaze_HPG2, color="black", ax=axs[0])

    sns.violinplot(box_sceneGaze_HL2, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(box_sceneGaze_HL2, color="black", ax=axs[1])

    sns.violinplot(Ga_Wi, showmeans=True, color="skyblue", ax=axs[2])
    sns.swarmplot(Ga_Wi, color="black", ax=axs[2])


    axs[1].sharey(axs[0])
    axs[2].sharey(axs[0])

    axs[0].set_ylabel('Sekunden', fontsize=12)
    axs[1].set_ylabel('Sekunden', fontsize=12)
    axs[2].set_ylabel('Sekunden', fontsize=12)

    xtick_HPG2 = []

    len2 = len(sceneGaze_HPG2)

    for elem2 in sceneGaze_HPG2:
        s = boxplotCap(elem2)
        xtick_HPG2.append(s)

    descArrayXTicks = ["Ga-1-Wi-HL2", "Ga-2-Wi-HL2"]
    (elemHL, xHL, dfHL2) = gf.setXTicks_param(box_sceneGaze_HL2, descArrayXTicks)

    descArrayXTicks = ["Ga-1-Wi-HPG2", "Ga-2-Wi-HPG2"]
    (elemHPG2, xHPG2, dfHPG2) = gf.setXTicks_param(box_sceneGaze_HPG2, descArrayXTicks)

    descArrayXTicks = ["Ga-1-Wi", "Ga-2-Wi"]
    (elemAll, xAll, dfAll) = gf.setXTicks_param(Ga_Wi, descArrayXTicks)



    axs[0].set_title('Gaze mit der HoloLens 2')
    axs[0].set_xticks([])
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ttable = table(axs[0], dfHL2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(10)
    ttable.auto_set_font_size(False)



    axs[1].set_title('Gaze mit der Reverb G2')
    axs[1].set_xticks([])
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    dfHPG2 = dfHPG2.reset_index(drop=True)
    ttable = table(axs[1], dfHPG2, loc='bottom', colLoc='center', cellLoc='center', rowLabels=None, colLabels=None)
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(10)
    # ttable.style.hide_index()
    ttable.auto_set_font_size(False)

    axs[2].set_title('Gaze mit HPG2 und HL2')
    axs[2].set_xticks([])
    axs[2].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    dfAll = dfAll.reset_index(drop=True)
    ttable = table(axs[2], dfAll, loc='bottom', colLoc='center', cellLoc='center', rowLabels=None, colLabels=None)
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(10)
    # ttable.style.hide_index()
    ttable.auto_set_font_size(False)

    plt.show()


