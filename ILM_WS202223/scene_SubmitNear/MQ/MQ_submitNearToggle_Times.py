import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics

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




def runAnalyzeFirstButton(probands, sceneName, device):

    allData = []

    for prob in probands:
        probandId = prob

        x = col.find({  'scene': sceneName,
                        'dev': device,
                        'action': 'Submit Button',
                        'actionvalue': '3',
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            #print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')


            y = col.find({'scene': sceneName,
                          'dev': device,
                          'action': 'Submit Toggle',
                          'actionvalue': '1',
                          'prob': probandId,
                          })

            y_list = list(y)

            #print('Y-List' + str(y_list))

            if len(y_list) > 0:

                endAction = y_list[0].get('time')
                endDate = y_list[0].get('date')

            endAction = pd.to_datetime(endDate + ' ' + endAction)
            startAction = pd.to_datetime(startDate + ' ' + startAction)

            delta = endAction - startAction
            # float(delta.seconds + '.' + delta.)
            allData.append(delta.total_seconds())

            print('Proband ' + str(probandId))
            print('Toggle 1 ' + str(delta.total_seconds()))

            x = None
            y = None
            y_list = None
            x_list = None

            endAction = None
            startAction = None

    return allData


def runAnalyzeButton(probands, sceneName, device, button):

    allData = []

    for prob in probands:
        probandId = prob

        x = col.find({  'scene': sceneName,
                        'dev': device,
                        'action': 'Submit Toggle',
                        'actionvalue': button,
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

           # print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')

            next_button = int(button) + 1


            y = col.find({'scene': sceneName,
                          'dev': device,
                          'action': 'Submit Toggle',
                          'actionvalue': str(next_button),
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

            print('Proband ' + str(probandId))
            print('Toggle ' + button + ' - ' + str(delta.total_seconds()))

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
    dbname = get_database()

    col = dbname["uwp"]



    #probands = col.distinct('prob')
    #probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    #probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18']
    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27']
    #probands = col.distinct('prob')
    print(probands)

    sceneName = 'ILM_Submit-Near_Right_Scene'
    query_string = {'$regex': 'MQ*'}
    deviceName = query_string


    sceneSubmitNearButton = runAnalyzeFirstButton(probands, sceneName, deviceName)
    sceneSubmitNearButton_2 = runAnalyzeButton(probands, sceneName, deviceName, '1')
    sceneSubmitNearButton_3 = runAnalyzeButton(probands, sceneName, deviceName, '2')


    # print(sceneSubmitNearButton)


    allTimes = [sceneSubmitNearButton, sceneSubmitNearButton_2, sceneSubmitNearButton_3]

    fig, ax1 = plt.subplots(figsize=(12, 12))



    # num_boxes = len(sceneTeleportRightMQ2_1)
    # medians = np.empty(num_boxes)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)

    # fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit der Toggles mit der rechten Hand')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes)
    plt.ylabel('Sekunden')

    plt.xticks([1, 2, 3], [f'Toggle 1 \n \n n = {len(allTimes[0])} \n Median = {round(statistics.median(allTimes[0]), 3)} s \n Mittelwert = {round(statistics.mean(allTimes[0]), 3)} s \n 1. Quartil = {round(np.percentile(allTimes[0], 25), 3)} s \n 3. Quartil = {round(np.percentile(allTimes[0], 75), 3)} s',
                           f'Toggle 2 \n \n n = {len(allTimes[1])} \n Median = {round(statistics.median(allTimes[1]), 3)} s \n Mittelwert = {round(statistics.mean(allTimes[1]), 3)} s \n 1. Quartil = {round(np.percentile(allTimes[1], 25), 3)} s \n 3. Quartil = {round(np.percentile(allTimes[1], 75), 3)} s',
                           f'Toggle 3 \n \n n = {len(allTimes[2])} \n Median = {round(statistics.median(allTimes[2]), 3)} s \n Mittelwert = {round(statistics.mean(allTimes[2]), 3)} s \n 1. Quartil = {round(np.percentile(allTimes[2], 25), 3)} s \n 3. Quartil = {round(np.percentile(allTimes[2], 75), 3)} s'])

    plt.show()
