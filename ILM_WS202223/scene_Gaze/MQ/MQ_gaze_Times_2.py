import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
from pandas.plotting import table
import sys
import seaborn as sns
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
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

                    print(f'P \t {prob} \t \t D {ger}  \t \t T {delta.total_seconds()}')

                    # print("Prob   " + str(y_list[0].get('prob')))
                    # print("Device" + str(y_list[0].get('dev')))
                    # print("Delta" + str(delta.total_seconds()))

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

    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
                'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
                'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    # probands = ['A06', 'A12', 'A28']
    # print(probands)

    # MQ2
    sceneName = 'ILM_Snap_Right'
    devices = ['MQ2']
    hand = 'Right'
    sceneGaze_R_MQ2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Ga-Ad-R-MQ2', sceneGaze_R_MQ2)

    sceneName = 'ILM_Snap_Left'
    hand = 'Left'
    sceneGaze_L_MQ2 = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Ga-Ad-L-MQ2', sceneGaze_L_MQ2)

    sceneGaze_R_MQ2 = aggregateData(sceneGaze_R_MQ2)
    sceneGaze_L_MQ2 = aggregateData(sceneGaze_L_MQ2)


    sceneGaze_MQ2 = [sceneGaze_R_MQ2, sceneGaze_L_MQ2]

    print('sceneGaze_MQ2')
    print(sceneGaze_MQ2)

    # MQP
    sceneName = 'ILM_Snap_Right'
    devices = ['MQP']
    hand = 'Right'
    sceneGaze_R_MQP = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Ga-Ad-L-MQP', sceneGaze_R_MQP)

    sceneName = 'ILM_Snap_Left'
    hand = 'Left'
    sceneGaze_L_MQP = runAnalyzeElementSteps(probands, sceneName, devices, hand)
    writeToDb('Ga-Ad-L-MQP', sceneGaze_L_MQP)


    sceneGaze_R_MQP = aggregateData(sceneGaze_R_MQP)
    sceneGaze_L_MQP = aggregateData(sceneGaze_L_MQP)

    sceneGaze_MQP = [sceneGaze_R_MQP, sceneGaze_L_MQP]

    Ga_Ad_L = [sceneGaze_L_MQP, sceneGaze_L_MQ2]
    Ga_Ad_L = aggregateData(Ga_Ad_L)
    gf.writeToDb('GA-Ad-L', Ga_Ad_L)

    Ga_Ad_R = [sceneGaze_R_MQP, sceneGaze_R_MQ2]
    Ga_Ad_R = aggregateData(Ga_Ad_R)
    gf.writeToDb('Ga-Ad-R', Ga_Ad_R)



    Ga_Ad = [sceneGaze_R_MQP, sceneGaze_L_MQP, sceneGaze_L_MQ2, sceneGaze_R_MQ2]
    Ga_Ad = aggregateData(Ga_Ad)
    gf.writeToDb('Ga-Ad', Ga_Ad)

    Ga_Ad_RL = [Ga_Ad_R, Ga_Ad_L, Ga_Ad]


    box_selectedProbands = [sceneGaze_R_MQP, sceneGaze_L_MQP]


    allTimes = sceneGaze_R_MQ2

    fig, axs = plt.subplots(1, 3, figsize=(10, 8))

    fig.suptitle('Android: Bearbeitungszeit Gaze-Operator')
    axs[0].set_title('Gaze mit der Quest 2')
    descArray = ["Ga-Ad-R-MQ2", "Ga-Ad-L-MQ2"]
    (num, val, dfMQ2) = gf.setXTicks_param(sceneGaze_MQ2, descArray)
    sns.violinplot(sceneGaze_MQ2, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(sceneGaze_MQ2, color="black", ax=axs[0])
    axs[0].set_xticks([])

    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ttable = table(axs[0], dfMQ2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)





    axs[0].set_ylabel('Sekunden', fontsize=12)
    axs[1].set_ylabel('Sekunden', fontsize=12)
    axs[2].set_ylabel('Sekunden', fontsize=12)



    # axs[0].set_xticks(xtick_HL)

    sns.violinplot(sceneGaze_MQP, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(sceneGaze_MQP, color="black", ax=axs[1])
    # axs[1].boxplot(sceneGaze_MQP)
    axs[1].sharey(axs[0])
    axs[1].set_title('Gaze mit der Quest Pro')
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    descArray = ["Ga-Ad-R-MQP", "Ga-Ad-L-MQP"]
    (num, val, dfMQP) = gf.setXTicks_param(sceneGaze_MQP, descArray)
    dfMQP = dfMQP.reset_index(drop=True)
    dfMQP.reset_index(drop=True)
    axs[1].set_xticks([])
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ttable = table(axs[1], dfMQP, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)



    sns.violinplot(Ga_Ad_RL, showmeans=True, color="skyblue", ax=axs[2])
    sns.swarmplot(Ga_Ad_RL, color="black", ax=axs[2])
    # axs[1].boxplot(sceneGaze_MQP)
    axs[2].sharey(axs[0])
    axs[2].set_title('Gaze mit der Quest 2 und Pro')
    axs[2].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    descArray = ["Ga-Ad-R", "Ga-Ad-L", "Ga-Ad"]
    (num, val, dfMQ) = gf.setXTicks_param(Ga_Ad_RL, descArray)
    dfMQ = dfMQ.reset_index(drop=True)
    dfMQ.reset_index(drop=True)
    axs[2].set_xticks([])
    axs[2].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ttable = table(axs[2], dfMQ, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)





    plt.show()


