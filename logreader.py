import datetime
import os
import matplotlib.pyplot as plt
import numpy as np


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
        del columns[0]
        del columns[0]
        if len(columns) == 3:
            del columns[0]
        columns[1] = columns[1].replace('nachm.', 'PM')
        columns[1] = datetime.datetime.strptime(columns[1], '%d.%m.%Y %I:%M:%S.%f %p')

        if 'RightHand' in columns[0]:
            if columns[0].startswith('Starting to hover over'):
                rightHandStartTime = columns[1]
                rightHandProgress = 1
            elif columns[0].startswith('Object picked up'):
                if rightHandProgress == 1:
                    rightHandProgress = 2
                else:
                    rightHandProgress = 0
            elif columns[0].startswith('Object dropped'):
                if rightHandProgress == 2:
                    rightHandProgress = 3
                else:
                    rightHandProgress = 0
            elif columns[0].startswith('Stops to hover over'):
                if rightHandProgress == 3:
                    rightHandProgress = 0
                    rightHandTimes.append(columns[1] - rightHandStartTime)
                else:
                    rightHandProgress = 0
        elif 'LeftHand' in columns[0]:
            if columns[0].startswith('Starting to hover over'):
                leftHandStartTime = columns[1]
                leftHandProgress = 1
            elif columns[0].startswith('Object picked up'):
                if leftHandProgress == 1:
                    leftHandProgress = 2
                else:
                    leftHandProgress = 0
            elif columns[0].startswith('Object dropped'):
                if leftHandProgress == 2:
                    leftHandProgress = 3
                else:
                    leftHandProgress = 0
            elif columns[0].startswith('Stops to hover over'):
                if leftHandProgress == 3:
                    leftHandProgress = 0
                    leftHandTimes.append(columns[1] - leftHandStartTime)
                else:
                    leftHandProgress = 0
                pass

        elif columns[0] == 'Wants to teleport...':
            startTeleporting = columns[1]
        elif columns[0].startswith('Teleported'):
            stopTeleporting = columns[1]
            teleportingTimes.append(stopTeleporting - startTeleporting)
            # read the position
            teleportingPositions.append([float(elem) for elem in columns[0][28:-1].split(', ')])
        else:
            print('no case for:', columns[0])

    return teleportingTimes, rightHandTimes, leftHandTimes, teleportingPositions


def logParserAR(gestureFilename, speechFilename):
    with open(gestureFilename) as file:
        content = file.read().splitlines()
    with open(speechFilename) as file:
        content += file.read().splitlines()
    
    # maybe sort content later?
    
    selectionProgress = 0
    selectionStartTime = 0
    selectionSuccessfulTimes = []
    selectionFailedCount = 0
    speechStartTime = 0
    speechSuccessfulTimes = []
    speechFailedTimes = []
    
    for line in content:
        line = line.replace(' |', '|')
        line = line.replace('| ', '|')
        columns = line.split('|')
        del columns[0]
        columns[1] = datetime.datetime.strptime(columns[1], '%d/%m/%Y %I:%M:%S.%f %p')
        
        if columns[0] == 'Clear Space':
            selectionProgress = 1
        elif columns[0] == 'Gaze has changed':
            if selectionProgress in (1,2):
                if selectionProgress == 1:
                    selectionStartTime = columns[1]                    
                selectionProgress = 2
            else:
                selectionProgress = 0
        elif columns[0] == 'Selection successfull':
            if selectionProgress in (2,3):
                selectionSuccessfulTimes.append(columns[1] - selectionStartTime)
            selectionProgress = 0
        elif columns[0] == 'Selection NOT successfull':
            selectionFailedCount += 1
            selectionProgress = 0
        elif columns[0] == 'Speech Attempt':
            if speechStartTime != 0:
                # speech command failed
                speechFailedTimes.append(columns[1] - speechStartTime)
            speechStartTime = columns[1]
        elif columns[0] in ['Speech Reset World', 'Speech Drop Sphere']:
            speechSuccessfulTimes.append(columns[1] - speechStartTime)
            speechStartTime = 0
        else:
            print('no case for:', columns[0])
            
    # if last speech attempt failed count is wrong. should we care?
            
    return selectionSuccessfulTimes, selectionFailedCount, speechSuccessfulTimes, speechFailedTimes


if __name__ == "__main__":
    
    teleportingTimes = []
    rightHandTimes = []
    leftHandTimes = []
    teleportingPositions = []
    
    for file in os.listdir('logsVR'):
        tt, rht, lht, tp = logParserVR('logsVR/' + file)
        teleportingTimes += tt
        rightHandTimes += rht
        leftHandTimes += lht
        teleportingPositions.append(tp)
        
    
    print('VR:')
    printStatistic(statistics(teleportingTimes))
    print()
    printStatistic(statistics(rightHandTimes))
    print()
    printStatistic(statistics(leftHandTimes))
    
    i = 1
    x_plots = 3
    y_plots = len(teleportingPositions) / x_plots
    fig = plt.figure(x_plots/y_plots)
    # plot teleporting
    for tp in teleportingPositions:
        tp = np.array(tp)
        
        ax = fig.add_subplot(y_plots, x_plots, i, projection='3d')
        ax.plot3D(tp[:,0], tp[:,2], tp[:,1])
        i += 1
    #plt.show()
    plt.subplots_adjust(bottom=0.1, right=1.0, top=0.9)
    plt.savefig('teleportingPositions.svg')
        
    
    selectionSuccessfulTimes = []
    selectionFailedCount = 0
    speechSuccessfulTimes = []
    speechFailedTimes = []
    
    for folder in os.listdir('logsAR/'):
        sst, sfc, speech, sft = logParserAR('logsAR/' + folder + '/UGIWGestureLogs.txt', 'logsAR/' + folder + '/SpeechLogHandler.txt')
        selectionSuccessfulTimes += sst
        selectionFailedCount += sfc
        speechSuccessfulTimes += speech
        speechFailedTimes += sft
    
    
    print()
    print()
    print('AR:')
    printStatistic(statistics(selectionSuccessfulTimes))
    print()
    print(selectionFailedCount)
    print()
    printStatistic(statistics(speechSuccessfulTimes))
    print()
    printStatistic(statistics(speechFailedTimes))
    
    pass
