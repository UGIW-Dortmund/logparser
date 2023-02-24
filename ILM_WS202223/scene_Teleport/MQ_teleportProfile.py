import datetime
import os
# import matplotlib.pyplot as plt, colors
from matplotlib import pyplot as plt, colors
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




def runAnalyze(probands, sceneName):

    allData = []
    positions = []

    for prob in probands:
        probandId = prob

        x = col.find({'scene': sceneName,
                      'action': 'Start Scene',
                      'prob': probandId})
        x_list = list(x)
        if len(x_list) > 0:

            # print("For Proband: " + probandId)
            for data in x_list:
                startAction = data.get('time')
                startDate = data.get('date')

            y = col.find({'scene': sceneName,
                          'action': 'Teleport Success',
                          'prob': probandId,
                          })

            y_list = list(y)

            if len(y_list) > 0:
                for data in y_list:
                    # print('End Scene')
                    # print(data)
                    teleportPosition = data.get('actionvalue')
                    teleportPosition = teleportPosition.replace('(', '')
                    teleportPosition = teleportPosition.replace(')', '')

                    vPosition = teleportPosition.split(',')

                    # print(str(vPosition))

                    positions.append(vPosition)



            allData.append([probandId, positions])
            x = None
            y = None
            y_list = None
            x_list = None
            positions = []



    return allData

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]

    #probands = col.distinct('prob')
    # probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    #probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18']
    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15',
                'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27']

    # probands = ['A01', 'A02']

    teleportPositions = runAnalyze(probands, 'ILM_Teleport_Scene_Left-Hand')

    # ILM_Teleport_Scene_Left-Hand
    # ILM_Submit-Near_Right_Scene

    # print(teleportPositions[0][1][0])


    all_x_values = []
    all_y_values = []

    xy_values = []
    x_values = []
    y_values = []
    # 1. Probanden
    for a in teleportPositions:
        # print(a[1])
        # 2. Verschiedene Teleport Positionen je nach Proband
        for b in a[1]:
            # print(b[1][0])
            x_values.append(float(b[0]))
            y_values.append(float(b[2]))

            all_x_values.append(float(b[0]))
            all_y_values.append(float(b[2]))

            xy_values.append([float(b[0]), float(b[2])])



        # plt.scatter(x_values, y_values, label=a[0])
        # print('X-Values:  ' + str(x_values))
        # print('Y-Values:  ' + str(y_values))
        x_values = []
        y_values = []


    #plt.legend()
    fig = plt.title('Teleport Positionen der linken Hand')
    #plt.xlabel("X-Koordinaten")
    #plt.ylabel("Z-Koordinaten")



    a = np.random.random((16, 16))
    data = np.random.random((2, 5))

    print(data)

    print(str(xy_values))
    print(all_x_values)
    print(all_y_values)
    # plt.hist(xy_values, num_bins)
    # plt.hist2d(all_x_values, all_y_values, bins=10) # imshow(data, cmap='hot', interpolation='nearest')

    # fig, ax = plt.subplots()
    # plt.hist2d(all_x_values, all_y_values, bins=10, norm=colors.Normalize())

    fig, ax = plt.subplots()

    ax.hist2d(all_x_values, all_y_values, bins=10) #, np.arange(-3, 3, 0.1)))

    ax.set(xlim=(-6, 6), ylim=(-8, 8))


    plt.show()

