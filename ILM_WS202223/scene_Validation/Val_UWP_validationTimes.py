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

    sceneName = 'ILM_Validation'
    shelf = 'R7E3'
    actionCubes = ['Cube Position End', 'Cube Rotation End']
    actionButtons = ['btnRetrieveArticle', 'btnConfirmArticle']
    done_items = 0

    for cubes in actionCubes:

        done = col.find({'scene': sceneName,
                      'dev': device,
                      'action': cubes,
                      'oelement': shelf,
                      'prob': proband})

        done_list = list(done)
        if (len(done_list) > 0):
            done_items = done_items + 1
            # print(done_list)

    for button in actionButtons:

        done = col.find({'scene': sceneName,
                           'dev': device,
                           'action': 'Set oElement',
                           'actionvalue': button,
                           'prob': proband})

        done_list = list(done)
        if (len(done_list) > 0):
            done_items = done_items + 1
            # print(done_list)

    if done_items == 4:
        print(f'Complete \t \t {str(proband)} \t \t {str(device)}')
        return True
    else:
        print(f'Not complete \t \t {str(proband)} \t \t {str(device)}')
        return False


def runAnalyze(probands, sceneName, device):

    allData = []

    for prob in probands:

        startTime = ''
        startDate = ''
        endTime = ''
        endDate = ''
        endAction = None
        startAction = None

        probandId = prob
        if (checkCompletness(prob, device) == True):

            x = col.find({'scene': sceneName,
                          'dev': device,
                          'action': 'Start Scene',
                          'prob': probandId})
            x_list = list(x)
            if len(x_list) > 0:


                startTime = x_list[0].get('time')
                startDate = x_list[0].get('date')
                startAction = pd.to_datetime(startDate + ' ' + startTime)

                y = col.find({'scene': sceneName,
                              'dev': device,
                              'action': 'End Scene',
                              'prob': probandId,
                              })

                y_list = list(y)

                if len(y_list) > 0:

                    endTime = y_list[0].get('time')
                    endDate = y_list[0].get('date')

                    endAction = pd.to_datetime(endDate + ' ' + endTime)

                    delta = endAction - startAction
                    allData.append(delta.seconds)

                elif len(y_list) == 0:
                    y = col.find({'scene': sceneName,
                                  'dev': device,
                                  'action': 'Saved on device',
                                  'prob': probandId})
                    y_list = list(y)

                    if len(y_list) > 0:
                        endAction = y_list[0].get('time')
                        endDate = y_list[0].get('date')

                        endAction = pd.to_datetime(endDate + ' ' + endAction)

                        delta = endAction - startAction
                        allData.append(delta.seconds)


    return allData

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = gf.get_database()

    col = dbname["uwp"]

    probands = gf.probands
    # print(probands)

    valHL2 = runAnalyze(probands, 'ILM_Validation', 'HL2')
    valHPG2 = runAnalyze(probands, 'ILM_Validation', 'HPG2')
    valUWP = [valHL2, valHPG2]
    valUWP = gf.aggregateData(valUWP)
    gf.writeToDb('Val-Wi-HL2', valHL2)
    gf.writeToDb('Val-Wi-HPG2', valHPG2)
    # gf.writeToDb('Val-Ad', valUWP)


    allTimes = [valHL2, valHPG2, valUWP]


    # fig = plt.figure(figsize=(10, 7))
    plt.title('Windows: Bearbeitungszeit Validierungsszene', fontsize=15)
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes, showmeans=True)
    plt.ylabel('Sekunden', fontsize=12)
    descArray = ["HL2", "HPG2", "Val-UWP"]
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
