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


def runAnalyze(probands, sceneName, device):

    allData = []

    for prob in probands:
        probandId = prob

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
                              'action': 'Skip Scene',
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

            print("For Proband: " + probandId)
            print(delta.seconds)

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

    sceneTimeTeleportRight = []
    sceneTimeTeleportLeft = []
    device = 'HPG2'

    allTimes = None

    # Can't use 13 becs it broke

    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A14']


    sceneGrabRightHL2 = runAnalyze(probands, 'ILM_Grab_Right', 'HL2')
    sceneGrabLeftHL2 = runAnalyze(probands, 'ILM_Grab_Left', 'HL2')

    sceneGrabRightHPG2 = runAnalyze(probands, 'ILM_Grab_Right', 'HPG2')
    sceneGrabLeftHPG2 = runAnalyze(probands, 'ILM_Grab_Left', 'HPG2')

    allTimes = [sceneGrabRightHL2, sceneGrabLeftHL2, sceneGrabRightHPG2, sceneGrabLeftHPG2]

    fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit UWP Grabbing Szene')

    plt.boxplot(allTimes)
    plt.xticks([1, 2, 3, 4], ['HL2 Rechte Hand', 'HL2 Linke Hand', 'HPG2 Rechte Hand', 'HPG2 Linke Hand'])
    plt.show()
