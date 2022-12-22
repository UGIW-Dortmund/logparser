import datetime
import os
import matplotlib.pyplot as plt
import math
import numpy as np
from lib_logparser import statistics, printStatistic


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
    
    # start position for teleporting
    teleportingPositions.append([0.0, 1.0, -7.5])

    for line in content:
        line = line.replace(' |', '|')
        line = line.replace('| ', '|')
        columns = line.split('|')
        del columns[0]
        del columns[0]
        if len(columns) == 3:
            del columns[0]
        columns[1] = columns[1].replace('nachm.', 'PM')
        columns[1] = columns[1].replace('vorm.', 'AM')
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

    # add a teleporting position (approximation) because the last one (to the button) is missing
    teleportingPositions.append([3.0, 1.0, -8.5])
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
        print(file)
        tt, rht, lht, tp = logParserVR('logsVR/' + file)
        teleportingTimes += tt
        rightHandTimes += rht
        leftHandTimes += lht
        teleportingPositions.append(tp)
        
    # convert the datetime to seconds inside a numpy array
    teleportingTimes = np.array([x.total_seconds() for x in teleportingTimes])
    rightHandTimes = np.array([x.total_seconds() for x in rightHandTimes])
    leftHandTimes = np.array([x.total_seconds() for x in leftHandTimes])

    print('VR:')
    printStatistic(statistics(teleportingTimes), 'teleportingTimes')
    print()
    printStatistic(statistics(rightHandTimes), 'rightHandTimes')
    print()
    printStatistic(statistics(leftHandTimes), 'leftHandTimes')
    
    # create boxplots for VR actions
    figBoxplotsVR, axsVR = plt.subplots(1, 3, sharey=True)
    # teleportingtimes
    axsVR[0].boxplot(teleportingTimes)
    #axsVR[0].boxplot(list(map(lambda x : x.total_seconds(), teleportingTimes)))
    axsVR[0].set(ylabel = 'time (s)')
    axsVR[0].get_xaxis().set_visible(False)
    axsVR[0].title.set_text('teleporting time')
    
    # right hand times
    axsVR[1].boxplot(rightHandTimes)
    #axsVR[1].boxplot(list(map(lambda x : x.total_seconds(), rightHandTimes)))
    axsVR[1].get_xaxis().set_visible(False)
    axsVR[1].title.set_text('right hand')
    
    # left hand times
    axsVR[2].boxplot(leftHandTimes)
    #axsVR[2].boxplot(list(map(lambda x : x.total_seconds(), leftHandTimes)))
    axsVR[2].get_xaxis().set_visible(False)
    axsVR[2].title.set_text('left hand')
    
    figBoxplotsVR.savefig('images/boxplotsVR.png')
    
    
    i = 0
    x_plots = 3
    y_plots = math.ceil(len(teleportingPositions) / x_plots)
    figTeleporting, axsTeleporting = plt.subplots(y_plots, x_plots)
    # plot teleporting
    for tp in teleportingPositions:
        tp = np.array(tp)
        
        axsTeleporting[int(i/x_plots)][i%x_plots].plot(tp[:,2], -tp[:,0])
        axsTeleporting[int(i/x_plots)][i%x_plots].scatter(tp[:,2][0], -tp[:,0][0], marker='o', color='g') # starting position
        axsTeleporting[int(i/x_plots)][i%x_plots].scatter(tp[:,2][-1], -tp[:,0][-1], marker='o', color='r') # end position
        axsTeleporting[int(i/x_plots)][i%x_plots].plot([-5.5,-5.5],[2,-2]) # table
        axsTeleporting[int(i/x_plots)][i%x_plots].axis('equal')
        axsTeleporting[int(i/x_plots)][i%x_plots].get_xaxis().set_visible(False)
        axsTeleporting[int(i/x_plots)][i%x_plots].get_yaxis().set_visible(False)
        
        i += 1
        
    # hide any remaining plots
    for j in range(i%x_plots, x_plots):
        axsTeleporting[x_plots-1][j].axis('off')
        
    figTeleporting.savefig('images/teleportingPositions.png')
        
    
    # scatter plot
    figTimeDistance, axTimeDistance = plt.subplots()

    dataX = np.zeros(len(teleportingTimes))
    dataY = np.zeros(len(teleportingTimes))     
    totalPos = 0
    for run in teleportingPositions:
        teleportingCount = len(run) - 2
        for i in range(0, teleportingCount):
            dataY[totalPos] = teleportingTimes[totalPos]
            dataX[totalPos] = math.sqrt(math.pow(run[i+1][0] - run[i][0], 2) + math.pow(run[i+1][2] - run[i][2], 2))
            
            totalPos += 1
            
    axTimeDistance.scatter(dataX, dataY)
    axTimeDistance.set(xlabel = 'distance', ylabel = 'time (s)')
    figTimeDistance.savefig('images/scatterTimeDistance.png')














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
    
    # convert the datetime to seconds inside a numpy array
    selectionSuccessfulTimes = np.array([x.total_seconds() for x in selectionSuccessfulTimes])
    speechSuccessfulTimes = np.array([x.total_seconds() for x in speechSuccessfulTimes])
    speechFailedTimes = np.array([x.total_seconds() for x in speechFailedTimes])
    
    print()
    print()
    print('AR:')
    printStatistic(statistics(selectionSuccessfulTimes), 'selectionSuccessfulTimes')
    print()
    print('selectionFailedCount:')
    print('\t' + str(selectionFailedCount))
    print()
    printStatistic(statistics(speechSuccessfulTimes), 'speechSuccessfulTimes')
    print()
    printStatistic(statistics(speechFailedTimes), 'speechFailedTimes')

    print('Values with error:')
    statSST = statistics(speechSuccessfulTimes)
    statSFT = statistics(speechFailedTimes)
    statSelect = statistics(selectionSuccessfulTimes)
    print("speech (avg): ", statSFT[2] * (1 + statSFT[5] / (statSST[5] + statSFT[5])))
    print("speech (mean): ", statSFT[3] * (1 + statSFT[5] / (statSST[5] + statSFT[5])))
    print("speech (std): ", statSFT[4] * (1 + statSFT[5] / (statSST[5] + statSFT[5])))

    print("select (avg): ", statSelect[2] * (1 + selectionFailedCount / (statSelect[5] + selectionFailedCount)))
    print("select (mean): ", statSelect[3] * (1 + selectionFailedCount / (statSelect[5] + selectionFailedCount)))
    print("select (std): ", statSelect[4] * (1 + selectionFailedCount / (statSelect[5] + selectionFailedCount)))
    
    # create boxplots for AR actions
    figBoxplotsAR, axsAR = plt.subplots(1, 2)
    #figBoxplotsAR.tight_layout()
    # selection successful
    axsAR[0].boxplot(selectionSuccessfulTimes)
    #axsAR[0].boxplot(list(map(lambda x : x.total_seconds(), selectionSuccessfulTimes)))
    axsAR[0].set(ylabel = 'time (s)')
    axsAR[0].get_xaxis().set_visible(False)
    axsAR[0].title.set_text('selection successful')
    
    # speech failed
    axsAR[1].boxplot(speechFailedTimes)
    #axsAR[1].boxplot(list(map(lambda x : x.total_seconds(), speechFailedTimes)))
    axsAR[1].set(ylabel = 'time (s)')
    axsAR[1].get_xaxis().set_visible(False)
    axsAR[1].title.set_text('speech command failed')
    
    figBoxplotsAR.savefig('images/boxplotsAR.png')
















    figsize = plt.figaspect(0.3)
    figBoxPlots, axs = plt.subplots(1, 5, figsize=figsize)
    figBoxPlots.subplots_adjust(wspace=0.5, left=0.03, right=0.97)

    axs[0].boxplot(teleportingTimes)
    axs[0].set(ylabel = 'time (s)')
    axs[0].get_xaxis().set_visible(False)
    axs[0].title.set_text('Teleport')

    # left hand times
    axs[1].boxplot(leftHandTimes)
    axs[1].get_xaxis().set_visible(False)
    axs[1].title.set_text('Grab left')

    # right hand times
    axs[2].boxplot(rightHandTimes)
    axs[2].get_xaxis().set_visible(False)
    axs[2].title.set_text('Grab right')

    # selection successful
    axs[3].boxplot(selectionSuccessfulTimes)
    axs[3].get_xaxis().set_visible(False)
    axs[3].title.set_text('Submit')

    # speech failed
    axs[4].boxplot(speechFailedTimes)
    axs[4].get_xaxis().set_visible(False)
    axs[4].title.set_text('Speech')

    figBoxPlots.savefig('images/boxplots.png')

    
    pass

