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




def runAnalyze(probands, sceneName, device, anchor):

    allData = []

    for prob in probands:
        probandId = prob

        x = col.find({  'scene': sceneName,
                        'dev': device,
                        'action': 'Teleport Anchor Reached',
                        'actionvalue': anchor,
                        'prob': probandId})

        x_list = list(x)


        if len(x_list) > 0:

            print('X-List' + str(x_list))

            next_anchor = int(anchor) + 1

            print('Next anchor ' + str(next_anchor))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')


            y = col.find({'scene': sceneName,
                          'dev': device,
                          'action': 'Teleport Anchor Reached',
                          'actionvalue': str(next_anchor),
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




            # print("For T-Stop: " + str(anchor))
            # print('Delta ' + str(delta))
            # print('Sekunden ' + str(delta.seconds))
            # print('Milliseconds ' + str(delta.microseconds))
            # print('Total seconds ' + str(delta.total_seconds()))

            x = None
            y = None
            y_list = None
            x_list = None

            endAction = None
            startAction = None

    return allData

def boxplotCap(valArray):
    return f'\n n = {len(valArray)} \n' \
           f'Median = {round(statistics.median(valArray), 3)} s \n ' \
           f'Mittelwert = {round(statistics.mean(valArray), 3)} s \n ' \
           f'Standardabweichung = {round(statistics.stdev(valArray), 3)} s \n ' \
           f'Mittlere Abweichung = {round(mean(valArray), 3)} s \n ' \
           f'1. Quartil = {round(np.percentile(valArray, 25), 3)} s \n' \
           f'3. Quartil = {round(np.percentile(valArray, 75), 3)} s ';

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]



    #probands = col.distinct('prob')
    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27']
   # probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'A21', 'A22']
    probands = col.distinct('prob')
    print(probands)

    sceneName = 'ILM_Teleport_Scene_Left-Hand'
    query_string = {'$regex': 'MQ*'}
    deviceName = query_string


    sceneTeleportRightMQ2_1 = runAnalyze(probands, sceneName, deviceName, '1')
    sceneTeleportLeftMQ2_2 = runAnalyze(probands, sceneName, deviceName, '2')
    sceneTeleportRightMQ2_3 = runAnalyze(probands, sceneName, deviceName, '3')
    sceneTeleportLeftMQ2_4 = runAnalyze(probands, sceneName, deviceName, '4')

    print(sceneTeleportRightMQ2_1)


    allTimes = [sceneTeleportRightMQ2_1, sceneTeleportLeftMQ2_2,
                sceneTeleportRightMQ2_3, sceneTeleportLeftMQ2_4]

    fig, ax1 = plt.subplots(figsize=(10, 15))

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title='Comparison of IID Bootstrap Resampling Across Five Distributions',
        xlabel='',
        ylabel='Sekunden',
    )

    num_boxes = len(sceneTeleportRightMQ2_1)
    # medians = np.empty(num_boxes)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(num_boxes)
    #upper_labels = [str(round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    i = 0
    '''
    for at in allTimes:
        # k = tick % 2
        i = i + 1
        ax1.text(pos[i], .97, 'n = ' + str(len(at)),
                 transform=ax1.get_xaxis_transform(),
                 horizontalalignment='center',
                 size='small')

    '''
    # fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit Teleport Szene mit der linken Hand')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes)
    plt.ylabel('Sekunden')
    plt.xticks([1, 2, 3, 4], [f'T-Stop 1 zu 2 \n n = {len(allTimes[0])}' , f'T-Stop 2 zu 3 \n n = {len(allTimes[1])}', f'T-Stop 3 zu 4 \n n = {len(allTimes[2])}', f'T-Stop 4 zu 5 \n n = {len(allTimes[3])}'])
    # plt.xticks([1, 2, 3, 4], [str(len(sceneTeleportRightMQ2)), str(len(sceneTeleportLeftMQ2)), 'MQP Rechte Hand', 'MQP Linke Hand'])

    plt.xticks([1, 2, 3, 4], [
        "T-Stopp 1 zu 2 \n " + boxplotCap(allTimes[0]),
        "T-Stopp 2 zu 3 \n " + boxplotCap(allTimes[1]),
        "T-Stopp 3 zu 4 \n " + boxplotCap(allTimes[2]),
        "T-Stopp 4 zu 5 \n " + boxplotCap(allTimes[3])])

    plt.show()
