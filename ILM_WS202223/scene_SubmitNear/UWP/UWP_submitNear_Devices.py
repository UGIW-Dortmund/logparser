import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import sys
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




def runAnalyzeFirstButton(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Start Scene',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                # print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'Button 1: Button Pressed',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData




def runAnalyzeSecondButton(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Near',
                            'actionvalue': 'CheckBox 1: Button Pressed',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                # print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'Button 2: Button Pressed',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData



def runAnalyzeThirdButton(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Near',
                            'actionvalue': 'CheckBox 2: Button Pressed',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                # print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'Button 3: Button Pressed',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData

def runAnalyzeFirstCheckbox(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Near',
                            'actionvalue': 'Button 1: Button Pressed',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                #print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'CheckBox 1: Button Pressed',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData



def runAnalyzeSecondCheckbox(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Near',
                            'actionvalue': 'Button 2: Button Pressed',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                # print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'CheckBox 2: Button Pressed',
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

                print(y_list[0].get('prob') + " " + str(delta))


                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


def runAnalyzeThirdCheckbox(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Near',
                            'actionvalue': 'Button 3: Button Pressed',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                # print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'CheckBox 3: Button Pressed',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData




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

    sceneName = 'ILM_Submit-Near_Right'
    devices = ['HPG2']

    sceneSubmitNearButton_1_Right = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_1_Right = runAnalyzeFirstCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_2_Right = runAnalyzeSecondButton(probands, sceneName, devices)

    # Probands without A14 = Outlier
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    sceneSubmitNearCheckbox_2_Right = runAnalyzeSecondCheckbox(probands, sceneName, devices)
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    sceneSubmitNearButton_3_Right = runAnalyzeThirdButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_3_Right = runAnalyzeThirdCheckbox(probands, sceneName, devices)

    allTimesRight_HPG2 = [sceneSubmitNearButton_1_Right, sceneSubmitNearCheckbox_1_Right,
                          sceneSubmitNearButton_2_Right, sceneSubmitNearCheckbox_2_Right,
                          sceneSubmitNearButton_3_Right, sceneSubmitNearCheckbox_3_Right]

    sceneName = 'ILM_Submit-Near_Left'

    sceneSubmitNearButton_1_Left = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_1_Left = runAnalyzeFirstCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_2_Left = runAnalyzeSecondButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_2_Left = runAnalyzeSecondCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_3_Left = runAnalyzeThirdButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_3_Left = runAnalyzeThirdCheckbox(probands, sceneName, devices)

    allTimesLeft_HPG2 = [sceneSubmitNearButton_1_Left, sceneSubmitNearCheckbox_1_Left,
                         sceneSubmitNearButton_2_Left, sceneSubmitNearCheckbox_2_Left,
                         sceneSubmitNearButton_3_Left, sceneSubmitNearCheckbox_3_Left]

    devices = ['HL2']

    sceneName = 'ILM_Submit-Near_Right'

    sceneSubmitNearButton_1_Right_HL2 = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_1_Right_HL2 = runAnalyzeFirstCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_2_Right_HL2 = runAnalyzeSecondButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_2_Right_HL2 = runAnalyzeSecondCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_3_Right_HL2 = runAnalyzeThirdButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_3_Right_HL2 = runAnalyzeThirdCheckbox(probands, sceneName, devices)

    allTimesRight_HL2 = [sceneSubmitNearButton_1_Right_HL2, sceneSubmitNearCheckbox_1_Right_HL2,
                         sceneSubmitNearButton_2_Right_HL2, sceneSubmitNearCheckbox_2_Right_HL2,
                         sceneSubmitNearButton_3_Right_HL2, sceneSubmitNearCheckbox_3_Right_HL2]

    sceneName = 'ILM_Submit-Near_Left'

    sceneSubmitNearButton_1_Left_HL2 = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_1_Left_HL2 = runAnalyzeFirstCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_2_Left_HL2 = runAnalyzeSecondButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_2_Left_HL2 = runAnalyzeSecondCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_3_Left_HL2 = runAnalyzeThirdButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_3_Left_HL2 = runAnalyzeThirdCheckbox(probands, sceneName, devices)

    allTimesLeft_HL2 = [sceneSubmitNearButton_1_Left_HL2, sceneSubmitNearCheckbox_1_Left_HL2,
                sceneSubmitNearButton_2_Left_HL2, sceneSubmitNearCheckbox_2_Left_HL2,
                sceneSubmitNearButton_3_Left_HL2, sceneSubmitNearCheckbox_3_Left_HL2]


    fig, axs = plt.subplots(2, 2, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit der Buttons')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0, 0].boxplot(allTimesRight_HPG2, showmeans=True)
    axs[0, 1].boxplot(allTimesLeft_HPG2, showmeans=True)
    axs[0, 1].sharey(axs[0, 0])

    axs[1, 0].boxplot(allTimesRight_HL2, showmeans=True)
    axs[1, 0].sharey(axs[0, 0])

    axs[1, 1].boxplot(allTimesLeft_HL2, showmeans=True)
    axs[1, 1].sharey(axs[0, 0])

    axs[0, 0].set(ylabel='Sekunden')
    axs[0, 1].set(ylabel='Sekunden')
    axs[1, 0].set(ylabel='Sekunden')
    axs[1, 1].set(ylabel='Sekunden')


    descArray = ["Button 1", "Checkbox 1", "Button 2", "Checkbox 2", "Button 3", "Checkbox 3"]

    num, val = gf.setXTicks_param_plain(allTimesRight_HPG2, descArray)
    print("HPG2 Right")
    gf.reqLatexTableOutput(allTimesRight_HPG2, descArray)
    axs[0, 0].set_title('1. Rechte Hand - HPG2', fontsize=15)
    axs[0, 0].set_xticks(num, val)

    num, val = gf.setXTicks_param_plain(allTimesRight_HL2, descArray)
    print("HL2 Right")
    gf.reqLatexTableOutput(allTimesRight_HL2, descArray)
    axs[1, 0].set_title('1. Rechte Hand - HL2', fontsize=15)
    axs[1, 0].set_xticks(num, val)

    num, val = gf.setXTicks_param_plain(allTimesLeft_HL2, descArray)
    print("HL2 Left")
    gf.reqLatexTableOutput(allTimesLeft_HL2, descArray)
    axs[1, 1].set_title('2. Linke Hand - HL2', fontsize=15)
    axs[1, 1].set_xticks(num, val)

    num, val = gf.setXTicks_param_plain(allTimesLeft_HPG2, descArray)
    print("HPG2 Left")
    gf.reqLatexTableOutput(allTimesLeft_HPG2, descArray)
    axs[0, 1].set_title('2. Linke Hand - HPG2', fontsize=15)
    axs[0, 1].set_xticks(num, val)

    plt.show()


