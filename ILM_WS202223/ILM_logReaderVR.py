import datetime
import os
import matplotlib.pyplot as plt
import numpy as np


filename = "ILM_Logfile_2022-12-08_16-00-57_ILM_Teleport.ugiw"

def statistics(list):
    min = list[0]
    max = list[0]
    avg = list[0]
    count = len(list)

    for i in list:
        if (min > i):
            min = i
        if (max < i):
            max = i
        avg += i

    avg /= count
    return min, max, avg, count


def printStatistic(statistic):
    print("Statistics")
    print('Min:', statistic[0])
    print('Max:', statistic[1])
    print('Avg:', statistic[2])
    print('Count:', statistic[3])

def logParserVR(filename):
    with open(filename) as file:
        content = file.read().splitlines()

    startTeleporting = 0
    stopTeleporting = 0

    rightHandStartTime = 0
    leftHandStartTime = 0
    rightHandProgress = 0
    leftHandProgress = 0

    teleportingTimes = []
    teleportingPositions = []
    rightHandTimes = []
    leftHandTimes = []

    for line in content:
        line = line.replace(' |', '|')
        line = line.replace('| ', '|')
        columns = line.split('|')

        print(columns[2])
        print(columns[3])

        del columns[0]
        del columns[0]

        print('Column 0')
        print(columns[0])
        print(columns[1])


        # if len(columns) == 3:
        #    del columns[0]
        # columns[0] = columns[0].replace('nachm.', 'PM')



        columns[0] = datetime.datetime.strptime(columns[0], '%d/%m/%Y %I:%M:%S.%f %p')


        if 'RightHand' in columns[1]:
            if columns[1].startswith('Starting to hover over'):
                rightHandStartTime = columns[1]
                rightHandProgress = 1
            elif columns[1].startswith('Object picked up'):
                if rightHandProgress == 1:
                    rightHandProgress = 2
                else:
                    rightHandProgress = 0
            elif columns[1].startswith('Object dropped'):
                if rightHandProgress == 2:
                    rightHandProgress = 3
                else:
                    rightHandProgress = 0
            elif columns[1].startswith('Stops to hover over'):
                if rightHandProgress == 3:
                    rightHandProgress = 0
                    rightHandTimes.append(columns[1] - rightHandStartTime)
                else:
                    rightHandProgress = 0
        elif 'LeftHand' in columns[1]:
            if columns[1].startswith('Starting to hover over'):
                leftHandStartTime = columns[1]
                leftHandProgress = 1
            elif columns[1].startswith('Object picked up'):
                if leftHandProgress == 1:
                    leftHandProgress = 2
                else:
                    leftHandProgress = 0
            elif columns[1].startswith('Object dropped'):
                if leftHandProgress == 2:
                    leftHandProgress = 3
                else:
                    leftHandProgress = 0
            elif columns[1].startswith('Stops to hover over'):
                if leftHandProgress == 3:
                    leftHandProgress = 0
                    leftHandTimes.append(columns[1] - leftHandStartTime)
                else:
                    leftHandProgress = 0
                pass

        elif columns[1].startswith('Teleport;'):
            startTeleporting = columns[0]
        elif columns[1].startswith('Teleported;'):
            stopTeleporting = columns[0]
            teleportingTimes.append(stopTeleporting - startTeleporting)

            # read the position
            # tPositions = ""
            #tPositions = columns[1][28:-2]
            # print(tPositions)

            #for elem in tPositions.split(", "):
            #    print(elem)
            #    fElement = float(elem)
            #    teleportingPositions.append(fElement)


            teleportingPositions.append([float(elem) for elem in columns[1][28:-2].split(', ')])

        else:
            print('no case for:', columns[1])


    return teleportingTimes, rightHandTimes, leftHandTimes, teleportingPositions

if __name__ == "__main__":



    for file in os.listdir('logsVR/ILM_Teleport'):

        # Make Lists Empty
        teleportingTimes = []
        rightHandTimes = []
        leftHandTimes = []
        teleportingPositions = []


        print(file.title())
        filename = file
        tt, rht, lht, tp = logParserVR('logsVR/ILM_Teleport/' + file)
        teleportingTimes += tt
        rightHandTimes += rht
        leftHandTimes += lht
        teleportingPositions.append(tp)

        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
        # ax.stem(x, y, z)

        # Get the test data
        X = []
        Y = []
        Z = []
        i = 0
        for tp in teleportingPositions[0]:
            i = i + 1
            print("Values")
            print(tp[0])
            X.append(tp[0])
            Y.append(tp[1])
            Z.append(tp[2])

            ax.scatter3D(X, Y, Z, c=X, cmap='Blues')

            # ax.stem(X, Y, Z)

            # Give the second plot only wireframes of the type x = c
            # ax2.plot_wireframe(X, Y, Z, rstride=0, cstride=10)
            # ax2.set_title("Row (y) stride set to 0")

            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')

            plt.tight_layout()
            # plt.show()
            plt.savefig('images/' + file + '.png', format='png')

    print('VR:')
    printStatistic(statistics(teleportingTimes))
    print()
    # printStatistic(statistics(rightHandTimes))
    print()
    # printStatistic(statistics(leftHandTimes))

    i = 1
    x_plots = 10
    y_plots = len(teleportingPositions[0]) / x_plots
    y_plots = int(y_plots)
    # fig = plt.figure(x_plots / y_plots)

    #print(y_plots)
    #print(len(teleportingPositions[0]))
    #print(teleportingPositions)

    # plot teleporting
    #for tp in teleportingPositions:
    #    tp = np.array(tp)

    #    ax = fig.add_subplot(y_plots, x_plots, i, projection='3d')
    #    ax.plot3D(tp[:, 0], tp[:, 2], tp[:, 1])
    #    i += 1

    #plt.show()

    #plt.subplots_adjust(bottom=0.1, right=1.0, top=0.9)

    #plt.savefig('teleportingPositions_2.svg', format='svg')

    # fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8, 12), subplot_kw={'projection': '3d'}


    print('i: ' + str(i))
    #print('Y: ' + len(Y))
    #print('Z: ' + len(Z))

    # Give the first plot only wireframes of the type y = c
    # ax1.plot_wireframe(X, Y, Z)
    #ax1.set_title("Column (x) stride set to 0")

    ### Different ways how to show the plot:



