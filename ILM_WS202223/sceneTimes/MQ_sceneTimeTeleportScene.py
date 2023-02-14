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

    #probands = col.distinct('prob')
    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    print(probands)


    sceneTeleportRightMQ2 = runAnalyze(probands, 'ILM_Teleport_Scene_Right-Hand', 'MQ2')
    sceneTeleportLeftMQ2 = runAnalyze(probands, 'ILM_Teleport_Scene_Left-Hand', 'MQ2')
    sceneTeleportRightMQP = runAnalyze(probands, 'ILM_Teleport_Scene_Right-Hand', 'MQP')
    sceneTeleportLeftMQP = runAnalyze(probands, 'ILM_Teleport_Scene_Left-Hand', 'MQP')


    allTimes = [sceneTeleportRightMQ2, sceneTeleportLeftMQ2, sceneTeleportRightMQP, sceneTeleportLeftMQP]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title='Comparison of IID Bootstrap Resampling Across Five Distributions',
        xlabel='Distribution',
        ylabel='Value',
    )

    num_boxes = len(sceneTeleportRightMQ2)
    medians = np.empty(num_boxes)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(num_boxes)
    upper_labels = [str(round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    i = 0
    for at in allTimes:
        # k = tick % 2
        i = i + 1
        ax1.text(pos[i], .95, 'n = ' + str(len(at)),
                 transform=ax1.get_xaxis_transform(),
                 horizontalalignment='center',
                 size='x-small')


    # fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit Teleport Szene')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes)
    plt.ylabel('Sekunden')
    plt.xticks([1, 2, 3, 4], ['MQ2 Rechte Hand', 'MQ2 Linke Hand', 'MQP Rechte Hand', 'MQP Linke Hand'])
    # plt.xticks([1, 2, 3, 4], [str(len(sceneTeleportRightMQ2)), str(len(sceneTeleportLeftMQ2)), 'MQP Rechte Hand', 'MQP Linke Hand'])
    plt.show()
