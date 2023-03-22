import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf


from pymongo import MongoClient



def runAnalyze(probands, sceneName, devices, anchor):

    allData = []

    for prob in probands:

        probandId = prob

        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Teleport Anchor Reached',
                            'actionvalue': anchor,
                            'prob': probandId})
            x_list = list(x)

            if len(x_list) > 0:

                next_anchor = int(anchor) + 1
                print('Next anchor ' + str(next_anchor))
                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')

                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Teleport Anchor Reached',
                              'actionvalue': str(next_anchor),
                              'prob': probandId,
                              })

                y_list = list(y)

                if len(y_list) > 0:
                    endAction = y_list[0].get('time')
                    endDate = y_list[0].get('date')

                endAction = pd.to_datetime(endDate + ' ' + endAction)
                startAction = pd.to_datetime(startDate + ' ' + startAction)

                delta = endAction - startAction

                print('X-List' + str(x_list[0]))
                print('Y-List' + str(y_list[0]))
                print('Delta: ' + str(delta))

                # float(delta.seconds + '.' + delta.)
                allData.append(delta.total_seconds())

            x = None
            y = None
            y_list = None
            x_list = None
            delta = None

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


# f'Varianz = {round(statistics.variance(valArray), 3)} \n ' \
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = gf.get_database()

    col = dbname["uwp"]

    #probands = col.distinct('prob')
    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
                'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
                'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    print(probands)

    sceneName = 'ILM_Teleport_Scene_Right-Hand'
    # query_string = {'$regex': 'MQ*'}
    # deviceName = query_string

    devices = ['MQ2', 'MQP']
    # devices = ['MQP']

    sceneTeleportRightMQ_1 = runAnalyze(probands, sceneName, devices, '1')
    sceneTeleportRightMQ_2 = runAnalyze(probands, sceneName, devices, '2')
    sceneTeleportRightMQ_3 = runAnalyze(probands, sceneName, devices, '3')
    sceneTeleportRightMQ_4 = runAnalyze(probands, sceneName, devices, '4')


    allDataRightHand = [sceneTeleportRightMQ_2, sceneTeleportRightMQ_3, sceneTeleportRightMQ_4]
    allDataRightHand = aggregateData(allDataRightHand)

    sceneName = 'ILM_Teleport_Scene_Left-Hand'
    sceneTeleportLeftMQ_1 = runAnalyze(probands, sceneName, devices, '1')
    sceneTeleportLeftMQ_2 = runAnalyze(probands, sceneName, devices, '2')
    sceneTeleportLeftMQ_3 = runAnalyze(probands, sceneName, devices, '3')
    sceneTeleportLeftMQ_4 = runAnalyze(probands, sceneName, devices, '4')

    allDataLeftHand = [sceneTeleportLeftMQ_1, sceneTeleportLeftMQ_2,sceneTeleportLeftMQ_3, sceneTeleportLeftMQ_4]
    allDataLeftHand = aggregateData(allDataLeftHand)

    allDataHand = [allDataRightHand, allDataLeftHand]
    allDataHand = aggregateData(allDataHand)



    T_1 = [sceneTeleportRightMQ_1]
    T_1 = aggregateData(T_1)
    gf.writeToDb('T-1', T_1)

    T_2 = [sceneTeleportRightMQ_2, sceneTeleportRightMQ_3, sceneTeleportRightMQ_4,
           sceneTeleportLeftMQ_1, sceneTeleportLeftMQ_2, sceneTeleportLeftMQ_3, sceneTeleportLeftMQ_4]
    T_2 = aggregateData(T_2)
    gf.writeToDb('T-2', T_2)

    allTimes = [T_1, T_2]

    fig, ax1 = plt.subplots(figsize=(10, 15))

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)


    # fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit der Teleport Szene mit beiden Händen und der Meta Quest Pro')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes, showmeans=True)
    plt.ylabel('Sekunden')

    descArray = ["T-1", "T-2"]
    num, val, df = gf.setXTicks_param(allTimes, descArray)

    plt.xticks(num, val)

    plt.show()
