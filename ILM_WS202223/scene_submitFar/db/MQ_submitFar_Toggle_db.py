import datetime
import decimal
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean
import locale

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



def runAnalyzeFirstToggle(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Button',
                            'actionvalue': '3',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Toggle',
                              'actionvalue': '1',
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


def runAnalyzeToggle(probands, sceneName, devices, toggle):

    allData = []

    for prob in probands:

        probandId = prob


        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Toggle',
                            'actionvalue': str(toggle),
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')

                next_toggle = int(toggle) + 1


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Toggle',
                              'actionvalue': str(next_toggle),
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
    median = round(statistics.median(valArray), 2)
    median = str(median).replace('.', ',')

    mean = round(statistics.mean(valArray), 2)
    mean = str(mean).replace('.', ',')

    stdev = round(statistics.stdev(valArray), 2)
    stdev = str(stdev).replace('.', ',')

    first_quartil = round(np.percentile(valArray, 25), 2)
    first_quartil = str(first_quartil).replace('.', ',')

    third_quartil = round(np.percentile(valArray, 75), 2)
    third_quartil = str(third_quartil).replace('.', ',')


    return f'\n n = {len(valArray)} \n' \
           f'Me. = {median} s \n ' \
           f'Mi. = {mean} s \n ' \
           f'S. Abw. = {stdev} s \n ' \
           f'1Q = {first_quartil} s \n ' \
            f'3Q = {third_quartil} s';


def convertToFloat(arr):

    print(arr)

    arr2 = arr.get('values')

    print(arr2)

    arr2 = list(arr2)
    lenArray = len(arr2)

    print(lenArray)

    allValues = []

    for e in range(0, lenArray):
        floatValues = []

        for elem in arr2[e]:
            floatValues.append(float(elem))

        allValues.append(floatValues)

    return allValues

if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]
    tresor = dbname["tresor"]

    locale.setlocale(locale.LC_ALL, 'de_DE')


    #probands = col.distinct('prob')
    # probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    # probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A18']
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24,' 'A25', 'A26', 'A27', 'A28']
    print(probands)

    sceneName = 'ILM_Submit-Far_Left_Scene'
    devices = ['MQP', 'MQ2']

    #sceneSubmitNearButton =
    #sceneSubmitNearButton_2 = runAnalyzeToggle(probands, sceneName, devices, '1')
    #sceneSubmitNearButton_3 = runAnalyzeToggle(probands, sceneName, devices, '2')

    #allTimesLeft = [sceneSubmitNearButton, sceneSubmitNearButton_2, sceneSubmitNearButton_3]
    allTimesLeft = tresor.find_one({'name': 'SF_MQ_L_Toggle'})
    allTimesLeft = convertToFloat(allTimesLeft)


    sceneName = 'ILM_Submit-Far_Right_Scene'

    #sceneSubmitNearButton_Right = runAnalyzeFirstToggle(probands, sceneName, devices)
    #sceneSubmitNearButton_2_Right = runAnalyzeToggle(probands, sceneName, devices, '1')
    #sceneSubmitNearButton_3_Right = runAnalyzeToggle(probands, sceneName, devices, '2')

    allTimesRight = tresor.find_one({'name': 'SF_MQ_R_Toggle'})
    allTimesRight = convertToFloat(allTimesRight)
    # allTimesRight = [sceneSubmitNearButton_Right, sceneSubmitNearButton_2_Right, sceneSubmitNearButton_3_Right]

    # writeToDb("SF_MQ_R_Toggle", allTimesRight)


    fig, axs = plt.subplots(1, 2, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit der Toggles')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    axs[1].boxplot(allTimesLeft, showmeans=True)
    axs[1].sharey(axs[0])
    axs[0].boxplot(allTimesRight, showmeans=True)


    axs[0].set(ylabel='Sekunden')
    axs[1].set(ylabel='Sekunden')


    axs[1].set_title('2. Szene: Linke Hand')
    axs[1].set_xticks([1, 2, 3], ["Toggle 1" + boxplotCap(allTimesLeft[0]),
                              "Toggle 2" + boxplotCap(allTimesLeft[1]),
                              "Toggle 3" + boxplotCap(allTimesLeft[2])])

    axs[0].set_title('1. Szene: Rechte Hand')
    axs[0].set_xticks([1, 2, 3], ["Toggle 1" + boxplotCap(allTimesRight[0]),
                                  "Toggle 2" + boxplotCap(allTimesRight[1]),
                                  "Toggle 3" + boxplotCap(allTimesRight[2])])

    plt.show()


