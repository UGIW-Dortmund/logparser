import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pymongo import MongoClient
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf

def checkCompletness(proband, device):

    sceneName = 'ILM_Validierung-Logistik'
    shelfs = ['O9', 'O6', 'O8']
    actions = ['Select Start', 'Validation retrieve article', 'Validation confirm article']
    done_items = 0

    for shelf in shelfs:
        for action in actions:

            done = col.find({'scene': sceneName,
                          'dev': device,
                          'action': action,
                          'actionvalue': shelf,
                          'prob': proband})

            done_list = list(done)

            if (len(done_list) > 0):
                done_items = done_items + 1
                # print(done_list)


    if done_items == 9:
        return True
    else:
        print(f'Not complete \t \t {str(proband)} \t \t {str(device)}')
        return False


def runAnalyze(probands, sceneName, device):

    allData = []

    for prob in probands:
        probandId = prob
        if (checkCompletness(prob, device) == True):

            x = col.find({'scene': sceneName,
                          'dev': device,
                          'action': 'Start Scene',
                          'prob': probandId})
            x_list = list(x)
            if len(x_list) > 0:

                for data in x_list:
                    startAction = data.get('time')
                    startDate = data.get('date')

                y = col.find({'scene': sceneName,
                              'dev': device,
                              'action': 'End Scene',
                              'prob': probandId,
                              })

                y_list = list(y)

                if len(y_list) > 0:
                    for data in y_list:
                        # print('End Scene')
                        # print(data)
                        endAction = data.get('time')
                        endDate = data.get('date')
                elif len(y_list) == 0:
                    y = col.find({'scene': sceneName,
                                  'dev': device,
                                  'actionvalue': 'Saved on device!',
                                  'prob': probandId})
                    y_list = list(y)
                    for data in y_list:
                        # print('Elif')
                        # print(data)
                        endAction = data.get('time')
                        endDate = data.get('date')

                endAction = pd.to_datetime(endDate + ' ' + endAction)
                startAction = pd.to_datetime(startDate + ' ' + startAction)

                delta = endAction - startAction
                allData.append(delta.seconds)

                # print("For Proband: " + probandId)
                # print(delta.seconds)

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = gf.get_database()

    col = dbname["uwp"]

    probands = gf.probands
    # print(probands)

    valMQ2 = runAnalyze(probands, 'ILM_Validierung-Logistik', 'MQ2')
    valMQP = runAnalyze(probands, 'ILM_Validierung-Logistik', 'MQP')
    valMQ = [valMQ2, valMQP]
    valMQ = gf.aggregateData(valMQ)
    gf.writeToDb('Val-Ad-MQ2', valMQ2)
    gf.writeToDb('Val-Ad-MQP', valMQP)
    gf.writeToDb('Val-Ad', valMQ)


    allTimes = [valMQ2, valMQP, valMQ]


    # fig = plt.figure(figsize=(10, 7))
    plt.title('Android: Bearbeitungszeit Validierungsszene', fontsize=15)
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes, showmeans=True)
    plt.ylabel('Sekunden', fontsize=12)
    descArray = ["MQ2", "MQP", "MQ"]
    num, val, df = gf.setXTicks_param(allTimes, descArray)
    ttable = table(plt.gca(), df, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    plt.grid(axis='y', linestyle='-', which='major', color='lightgrey', alpha=0.5)
    plt.xticks([])

    plt.show()
