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


    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15',
               'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    # probands = ['A01', 'A02']

    teleportPositionsRight = runAnalyze(probands, 'ILM_Teleport_Scene_Right-Hand')
    teleportPositionsLeft = runAnalyze(probands, 'ILM_Teleport_Scene_Left-Hand')

    all_x_values_right = []
    all_y_values_right = []

    all_x_values_left = []
    all_y_values_left = []

    xy_values_right = []
    xy_values_left = []

    x_values = []
    y_values = []
    # 1. Probanden
    for a in teleportPositionsRight:
        # print(a[1])
        # 2. Verschiedene Teleport Positionen je nach Proband
        for b in a[1]:
            # print(b[1][0])
            x_values.append(float(b[0]))
            y_values.append(float(b[2]))

            all_x_values_right.append(float(b[0]))
            all_y_values_right.append(float(b[2]))

            xy_values_right.append([float(b[0]), float(b[2])])



        # plt.scatter(x_values, y_values, label=a[0])
        # print('X-Values:  ' + str(x_values))
        # print('Y-Values:  ' + str(y_values))



        x_values = []
        y_values = []

    for a in teleportPositionsLeft:
        # print(a[1])
        # 2. Verschiedene Teleport Positionen je nach Proband
        for b in a[1]:
            # print(b[1][0])
            x_values.append(float(b[0]))
            y_values.append(float(b[2]))

            all_x_values_left.append(float(b[0]))
            all_y_values_left.append(float(b[2]))

            xy_values_left.append([float(b[0]), float(b[2])])



        # plt.scatter(x_values, y_values, label=a[0])
        # print('X-Values:  ' + str(x_values))
        # print('Y-Values:  ' + str(y_values))
        x_values = []
        y_values = []


    # fig, (ax1, ax2) = plt.subplots(1, 2)
    fig, axs = plt.subplots(1, 2, figsize=(10, 10))
    fig = plt.title('Teleport Positionen der rechten Hand')


    h_2 = axs[0].hist2d(all_x_values_right, all_y_values_right, bins=10, vmin=0, vmax=50, cmap=plt.cm.YlGnBu)
    axs[0].set_title('1. Rechte Hand', size=18)
    print('X-Right' + str(all_x_values_right))
    print('Y-Right' + str(all_y_values_right))

    h_1 = axs[1].hist2d(all_x_values_left, all_y_values_left, bins=10, vmin=0, vmax=50, cmap=plt.cm.YlGnBu)
    axs[1].set_title('2. Linke Hand', size=18)

    axs[1].sharey(axs[0])
    axs[1].sharex(axs[0])

    axs[0].set_facecolor((1.0, 0.47, 0.42))
    axs[1].set_facecolor((1.0, 0.47, 0.42))

    axs[0].set_xlabel('X-Koordinaten', fontsize=12)
    axs[0].set_ylabel('Z-Koordinaten', fontsize=12)
    axs[1].set_xlabel('X-Koordinaten', fontsize=12)
    axs[1].set_ylabel('Z-Koordinaten', fontsize=12)


    cb = plt.colorbar(h_1[3], ax=axs[0], label='Anzahl Teleport-Positionen')

    #cb = plt.colorbar(h_2[3], ax=axs[1], label='Anzahl der Teleport-Positionen')
    # cb.set_label(label='Anzahl der Teleport-Positionen', fontsize=12)



    plt.show()

