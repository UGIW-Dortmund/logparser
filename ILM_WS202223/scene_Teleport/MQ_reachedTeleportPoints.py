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



def setXTicks_param(valArray, descArray):
    xtick = []
    i = 0

    # The descirption of fields
    for elem in valArray:
        s = boxplotCap(elem)

        if descArray:
            xtick.append(descArray[i] + s)
        else:
            xtick.append(s)
        i = i + 1

    lenVA = len(valArray)

    # First Parameter the number of fields
    elements = []
    for elem in range(0, lenVA):
        elements.append((elem + 1))

    return (elements, xtick)



def boxplotCap(valArray):
    median = round(statistics.median(valArray), 1)
    median = str(median).replace('.', ',')

    mean = round(statistics.mean(valArray), 1)
    mean = str(mean).replace('.', ',')

    stdev = round(statistics.stdev(valArray), 1)
    stdev = str(stdev).replace('.', ',')

    first_quartil = round(np.percentile(valArray, 25), 1)
    first_quartil = str(first_quartil).replace('.', ',')

    third_quartil = round(np.percentile(valArray, 75), 1)
    third_quartil = str(third_quartil).replace('.', ',')

    return f'\n\n n = {len(valArray)} \n' \
           f'Me. = {median} s \n ' \
           f'Mi. = {mean} s \n ' \
           f'S. Abw. = {stdev} s \n ' \
           f'u. Q. = {first_quartil} s \n ' \
           f'o. Q. = {third_quartil} s';


def runAnalyze(probands, sceneName, devices, anchor):

    allData = []

    for prob in probands:

        probandId = prob

        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Teleport Anchor Reached',
                            'actionvalue': anchor,
                            'prob': probandId})
            x_list = list(x)


            if len(x_list) > 0:



                next_anchor = int(anchor) + 1

                print('Next anchor ' + str(next_anchor))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Teleport Anchor Reached',
                              'actionvalue': str(next_anchor),
                              'prob': probandId,
                              })


                y_list = list(y)



                if len(y_list) > 0:

                    endAction = y_list[0].get('time')
                    endDate = y_list[0].get('date')

                endAction = pd.to_datetime(endDate + ' ' + endAction)
                startAction = pd.to_datetime(startDate + ' ' + startAction)

                delta = endAction - startAction

                print('X-List' + str(x_list[0]))
                print('Y-List' + str(y_list[0]))
                print('Delta: ' + str(delta))


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



# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]



    #probands = col.distinct('prob')
    probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
                'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
                'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

    print(probands)

    sceneName = 'ILM_Teleport_Scene_Right-Hand'


    devices = ['MQ2', 'MQP']
    devices = ['MQP']

    sceneTeleportRightMQ2_1 = runAnalyze(probands, sceneName, devices, '1')
    sceneTeleportLeftMQ2_2 = runAnalyze(probands, sceneName, devices, '2')
    sceneTeleportRightMQ2_3 = runAnalyze(probands, sceneName, devices, '3')
    sceneTeleportLeftMQ2_4 = runAnalyze(probands, sceneName, devices, '4')

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

    # fig = plt.figure(figsize=(10, 7))
    plt.title('Bearbeitungszeit der Teleport-Szene mit der rechten Hand -- MQP', fontsize=15)
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])
    plt.boxplot(allTimes, showmeans=True)
    plt.ylabel('Sekunden', fontsize=12)
    # plt.xticks([1, 2, 3, 4], [f'T-Stop 1 zu 2 \n n = {len(allTimes[0])}' , f'T-Stop 2 zu 3 \n n = {len(allTimes[1])}', f'T-Stop 3 zu 4 \n n = {len(allTimes[2])}', f'T-Stop 4 zu 5 \n n = {len(allTimes[3])}'])


    descArray = ["T-Stopp 1 zu 2", "T-Stopp 2 zu 3", "T-Stopp 3 zu 4", "T-Stopp 4 zu 5"]
    num, val = setXTicks_param(allTimes, descArray)

    plt.xticks(num, val)

    plt.show()
