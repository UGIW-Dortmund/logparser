import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pymongo import MongoClient


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://fredix:memphis55@kurz-containar.de:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['ilm']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]

    sceneTimeTeleportRight = []
    sceneTimeTeleportLeft = []

    #probands = col.distinct('prob')
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    print(probands)


    usedHand = 'Right'
    plainSceneName = 'ILM_Grabbing_'
    sceneName = 'ILM_Grabbing_Right'

    for prob in probands:
        probandId = prob

        x = col.find({'scene': sceneName,
                      'action': 'Start Scene',
                      'prob': probandId})
        x_list = list(x)
        if len(x_list) > 0:

            for data in x_list:
                startAction = data.get('time')

            y = col.find({'scene': sceneName,
                          'action': 'End Scene',
                          'prob': probandId,
                          })

            y_list = list(y)

            if len(y_list) > 0:
                for data in y_list:
                    #print('End Scene')
                    # print(data)
                    endAction = data.get('time')
            elif len(y_list) == 0:
                y = col.find({'scene': sceneName,
                              'action': 'Skip Scene',
                              'prob': probandId})
                y_list = list(y)
                for data in y_list:
                    # print('Elif')
                    # print(data)
                    endAction = data.get('time')

            endAction = pd.to_datetime(endAction)
            startAction = pd.to_datetime(startAction)

            delta = endAction - startAction
            sceneTimeTeleportRight.append(delta.seconds)

            print("For Proband: " + probandId)
            print(delta.seconds)

            x = None
            y = None
            y_list = None
            x_list = None

            endAction = None
            startAction = None


    usedHand = 'Left'
    sceneName = plainSceneName + usedHand
    sceneName = 'ILM_Grabbing_Left'

    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A10', 'A12', 'A13', 'A14']

    for prob in probands:
        probandId = prob

        x = col.find({'scene': sceneName,
                      'action': 'Start Scene',
                      'prob': probandId})
        x_list = list(x)
        if len(x_list) > 0:

            for data in x_list:
                startAction = data.get('time')

            y = col.find({'scene': sceneName,
                          'action': 'End Scene',
                          'prob': probandId,
                          })

            y_list = list(y)

            if len(y_list) > 0:
                for data in y_list:
                    print('End Scene')
                    print(data)
                    endAction = data.get('time')
            elif len(y_list) == 0:
                y = col.find({'scene': sceneName,
                              'action': 'Skip Scene',
                              'prob': probandId})
                y_list = list(y)
                for data in y_list:
                    # print('Elif')
                    # print(data)
                    endAction = data.get('time')
            elif len(y_list) == 0:
                y = col.find({'scene': sceneName,
                              'actionvalue': 'Saved on device!',
                              'prob': probandId})
                y_list = list(y)
                for data in y_list:
                    # print('Elif')
                    # print(data)
                    endAction = data.get('time')

            endAction = pd.to_datetime(endAction, errors = 'coerce')
            startAction = pd.to_datetime(startAction, errors = 'coerce')

            delta = endAction - startAction
            sceneTimeTeleportLeft.append(delta.seconds)

            print("For Proband: " + probandId)
            print(delta.seconds)

            x = None
            y = None
            y_list = None
            x_list = None

            endAction = None
            startAction = None


    allTimes = [sceneTimeTeleportRight, sceneTimeTeleportLeft]

    fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit Grabbing Szene')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes)
    plt.xticks([1, 2], ['Rechte Hand', 'Linke Hand'])
    plt.show()
