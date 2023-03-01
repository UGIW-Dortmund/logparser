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

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'Button 1: Button Pressed',
                              'prob': probandId,
                              })

                y_list = list(y)

                print('Y-List' + str(y_list))

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

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'Button 2: Button Pressed',
                              'prob': probandId,
                              })

                y_list = list(y)

                print('Y-List' + str(y_list))

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

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'Button 3: Button Pressed',
                              'prob': probandId,
                              })

                y_list = list(y)

                print('Y-List' + str(y_list))

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

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'CheckBox 1: Button Pressed',
                              'prob': probandId,
                              })

                y_list = list(y)

                print('Y-List' + str(y_list))

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

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'CheckBox 2: Button Pressed',
                              'prob': probandId,
                              })

                y_list = list(y)

                print('Y-List' + str(y_list))

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

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Near',
                              'actionvalue': 'CheckBox 3: Button Pressed',
                              'prob': probandId,
                              })

                y_list = list(y)

                print('Y-List' + str(y_list))

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
           f'Median = {round(statistics.median(valArray), 3)} s \n ' \
           f'Mittelwert = {round(statistics.mean(valArray), 3)} s \n ';
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

    sceneName = 'ILM_Submit-Near_Right'
    devices = ['HPG2', 'HL2']

    sceneSubmitNearButton_1_Right = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_1_Right = runAnalyzeFirstCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_2_Right = runAnalyzeSecondButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_2_Right = runAnalyzeSecondCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_3_Right = runAnalyzeThirdButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_3_Right = runAnalyzeThirdCheckbox(probands, sceneName, devices)

    allTimes = [sceneSubmitNearButton_1_Right, sceneSubmitNearCheckbox_1_Right,
                sceneSubmitNearButton_2_Right, sceneSubmitNearCheckbox_2_Right,
                sceneSubmitNearButton_3_Right, sceneSubmitNearCheckbox_3_Right]

    sceneName = 'ILM_Submit-Near_Left'
    devices = ['HPG2', 'HL2']

    sceneSubmitNearButton_1_Left = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_1_Left = runAnalyzeFirstCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_2_Left = runAnalyzeSecondButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_2_Left = runAnalyzeSecondCheckbox(probands, sceneName, devices)
    sceneSubmitNearButton_3_Left = runAnalyzeThirdButton(probands, sceneName, devices)
    sceneSubmitNearCheckbox_3_Left = runAnalyzeThirdCheckbox(probands, sceneName, devices)

    allTimesLeft = [sceneSubmitNearButton_1_Left, sceneSubmitNearCheckbox_1_Left,
                sceneSubmitNearButton_2_Left, sceneSubmitNearCheckbox_2_Left,
                sceneSubmitNearButton_3_Left, sceneSubmitNearCheckbox_3_Left]


    fig, axs = plt.subplots(2, 1, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit der Buttons')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[0].boxplot(allTimes, notch=False)
    axs[1].boxplot(allTimesLeft, notch=False)
    axs[1].sharey(axs[0])



    axs[0].set(ylabel='Sekunden')
    axs[1].set(ylabel='Sekunden')

    axs[0].set_title('1. Szene: Rechte Hand')
    axs[0].set_xticks([1, 2, 3, 4, 5, 6], ["Button 1" + boxplotCap(allTimes[0]),
                                           "Checkbox 1" + boxplotCap(allTimes[1]),
                                           "Button 2" + boxplotCap(allTimes[2]),
                                           "Checkbox 2" + boxplotCap(allTimes[3]),
                                           "Button 3" + boxplotCap(allTimes[4]),
                                           "Checkbox 3" + boxplotCap(allTimes[5])])

    axs[1].set_title('2. Szene: Linke Hand')
    axs[1].set_xticks([1, 2, 3, 4, 5, 6], ["Button 1" + boxplotCap(allTimesLeft[0]),
                                        "Checkbox 1" + boxplotCap(allTimesLeft[1]),
                                        "Button 2" + boxplotCap(allTimesLeft[2]),
                                        "Checkbox 2" + boxplotCap(allTimesLeft[3]),
                                        "Button 3" + boxplotCap(allTimesLeft[4]),
                                           "Checkbox 3" + boxplotCap(allTimesLeft[5])])


    plt.show()


