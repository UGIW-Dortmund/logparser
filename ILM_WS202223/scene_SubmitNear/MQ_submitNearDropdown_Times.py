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




def runAnalyzeFirstDropdown(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Slider',
                            'actionvalue': 'Slider3',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Dropdown',
                              'actionvalue': 'Dropdown1',
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


def runAnalyzeDropdown(probands, sceneName, devices, dropdown):

    allData = []

    for prob in probands:

        probandId = prob


        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Dropdown',
                            'actionvalue': 'Dropdown' + str(dropdown),
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')

                next_slider = int(dropdown) + 1


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Dropdown',
                              'actionvalue': 'Dropdown' + str(next_slider),
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



    #probands = col.distinct('prob')
    # probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    # probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A18']
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24,' 'A25', 'A26', 'A27', 'A28']
    print(probands)

    sceneName = 'ILM_Submit-Near_Left_Scene'
    devices = ['MQP', 'MQ2']

    sceneSubmitNearButton = runAnalyzeFirstDropdown(probands, sceneName, devices)
    sceneSubmitNearButton_2 = runAnalyzeDropdown(probands, sceneName, devices, '1')
    sceneSubmitNearButton_3 = runAnalyzeDropdown(probands, sceneName, devices, '2')

    allTimesLeft = [sceneSubmitNearButton, sceneSubmitNearButton_2, sceneSubmitNearButton_3]

    sceneName = 'ILM_Submit-Near_Right_Scene'

    sceneSubmitNearButton_Right = runAnalyzeFirstDropdown(probands, sceneName, devices)
    sceneSubmitNearButton_2_Right = runAnalyzeDropdown(probands, sceneName, devices, '1')
    sceneSubmitNearButton_3_Right = runAnalyzeDropdown(probands, sceneName, devices, '2')

    allTimesRight = [sceneSubmitNearButton_Right, sceneSubmitNearButton_2_Right, sceneSubmitNearButton_3_Right]

    fig, axs = plt.subplots(1, 2, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit der Dropdown-Menüs')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[1].boxplot(allTimesLeft, notch=False)
    axs[1].sharey(axs[0])
    axs[0].boxplot(allTimesRight, notch=False)


    axs[0].set(ylabel='Sekunden')
    axs[1].set(ylabel='Sekunden')


    axs[1].set_title('2. Szene: Linke Hand')
    axs[1].set_xticks([1, 2, 3], ["Dropdown 1" + boxplotCap(allTimesLeft[0]),
                              "Dropdown 2" + boxplotCap(allTimesLeft[1]),
                              "Dropdown 3" + boxplotCap(allTimesLeft[2])])

    axs[0].set_title('1. Szene: Rechte Hand')
    axs[0].set_xticks([1, 2, 3], ["Dropdown 1" + boxplotCap(allTimesRight[0]),
                                  "Dropdown 2" + boxplotCap(allTimesRight[1]),
                                  "Dropdown 3" + boxplotCap(allTimesRight[2])])

    plt.show()


