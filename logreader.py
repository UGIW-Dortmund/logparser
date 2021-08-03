import datetime
import os


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
    rightHandTimes = []
    leftHandTimes = []

    for line in content:
        line = line.replace(' |', '|')
        line = line.replace('| ', '|')
        columns = line.split('|')
        del columns[0]
        del columns[0]
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

        if columns[0] == 'Wants to teleport...':
            startTeleporting = columns[1]
        elif columns[0].startswith('Teleported'):
            stopTeleporting = columns[1]
            teleportingTimes.append(stopTeleporting - startTeleporting)

    return teleportingTimes, rightHandTimes, leftHandTimes


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
            selectionStartTime = columns[1]
            selectionProgress = 1
        elif columns[0] == 'Gaze has changed':
            if selectionProgress in (1,2):
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
            
    # if last speech attempt failed count is wrong. should we care?
            
    return selectionSuccessfulTimes, selectionFailedCount, speechSuccessfulTimes, speechFailedTimes


if __name__ == "__main__":
    '''teleportingTimes, rightHandTimes, leftHandTimes = logParserVR('ProbeLogs.ugiw')
    
    printStatistic(statistics(teleportingTimes))
    print()
    printStatistic(statistics(rightHandTimes))
    print()
    printStatistic(statistics(leftHandTimes))'''
    
    selectionSuccessfulTimes = []
    selectionFailedCount = 0
    speechSuccessfulTimes = []
    speechFailedTimes = []
    
    for folder in os.listdir('logs/'):
        sst, sfc, speech, sft = logParserAR('logs/' + folder + '/UGIWGestureLogs.txt', 'logs/' + folder + '/SpeechLogHandler.txt')
        selectionSuccessfulTimes += sst
        selectionFailedCount += sfc
        speechSuccessfulTimes += speech
        speechFailedTimes += sft
    
    printStatistic(statistics(selectionSuccessfulTimes))
    print()
    print(selectionFailedCount)
    print()
    printStatistic(statistics(speechSuccessfulTimes))
    print()
    printStatistic(statistics(speechFailedTimes))
    
    pass
