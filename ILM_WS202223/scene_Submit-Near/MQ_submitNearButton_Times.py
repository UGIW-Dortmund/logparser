import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
                        'action': 'Start Scene',
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')


            y = col.find({'scene': sceneName,
                          'dev': device,
                          'action': 'Submit Button',
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


def runAnalyzeButton(probands, sceneName, device, button):

    allData = []

    for prob in probands:
        probandId = prob

        x = col.find({  'scene': sceneName,
                        'dev': device,
                        'action': 'Submit Button',
                        'actionvalue': button,
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')

            next_button = int(button) + 1


            y = col.find({'scene': sceneName,
                          'dev': device,
                          'action': 'Submit Button',
                          'actionvalue': str(next_button),
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
if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]



    #probands = col.distinct('prob')
    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    print(probands)

    sceneName = 'ILM_Submit-Far_Left_Scene'
    query_string = {'$regex': 'MQ*'}
    deviceName = query_string


    sceneSubmitNearButton = runAnalyzeFirstButton(probands, sceneName, deviceName)
    sceneSubmitNearButton_2 = runAnalyzeButton(probands, sceneName, deviceName, '1')
    sceneSubmitNearButton_3 = runAnalyzeButton(probands, sceneName, deviceName, '2')
    # sceneTeleportLeftMQ2_2 = runAnalyze(probands, sceneName, deviceName, '2')
    # sceneTeleportRightMQ2_3 = runAnalyze(probands, sceneName, deviceName, '3')
    # sceneTeleportLeftMQ2_4 = runAnalyze(probands, sceneName, deviceName, '4')

    print(sceneSubmitNearButton)


    allTimes = [sceneSubmitNearButton, sceneSubmitNearButton_2, sceneSubmitNearButton_3]

    fig, ax1 = plt.subplots(figsize=(10, 6))



    # num_boxes = len(sceneTeleportRightMQ2_1)
    # medians = np.empty(num_boxes)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)

    # fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit der Buttons mit der linken Hand')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes)
    plt.ylabel('Sekunden')

    plt.xticks([1, 2, 3], [f'Button 1 \n n = {len(allTimes[0])}',  f'Button 2 \n n = {len(allTimes[1])}', f'Button 3 \n n = {len(allTimes[2])}'])
    # plt.xticks([1, 2, 3, 4], [f'T-Stop 1 zu 2 \n n = {len(allTimes[0])}' , f'T-Stop 2 zu 3 \n n = {len(allTimes[1])}', f'T-Stop 3 zu 4 \n n = {len(allTimes[2])}', f'T-Stop 4 zu 5 \n n = {len(allTimes[3])}'])

    plt.show()
