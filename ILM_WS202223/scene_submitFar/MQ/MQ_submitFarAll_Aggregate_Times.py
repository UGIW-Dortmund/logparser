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




def runAnalyzeFirstDropdown(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Slider',
                            'actionvalue': 'Slider3',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Dropdown',
                              'actionvalue': 'Dropdown1',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


def runAnalyzeDropdown(probands, sceneName, devices, dropdown):

    allData = []

    for prob in probands:

        probandId = prob


        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Dropdown',
                            'actionvalue': 'Dropdown' + str(dropdown),
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')

                next_slider = int(dropdown) + 1


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Dropdown',
                              'actionvalue': 'Dropdown' + str(next_slider),
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


def runAnalyzeFirstSlider(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Toggle',
                            'actionvalue': '3',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Slider',
                              'actionvalue': 'Slider1',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


def runAnalyzeSlider(probands, sceneName, devices, slider):

    allData = []

    for prob in probands:

        probandId = prob


        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Slider',
                            'actionvalue': 'Slider' + str(slider),
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')

                next_slider = int(slider) + 1


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Slider',
                              'actionvalue': 'Slider' + str(next_slider),
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


def runAnalyzeFirstToggle(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Button',
                            'actionvalue': '3',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Toggle',
                              'actionvalue': '1',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


def runAnalyzeToggle(probands, sceneName, devices, toggle):

    allData = []

    for prob in probands:

        probandId = prob


        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Toggle',
                            'actionvalue': str(toggle),
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')

                next_toggle = int(toggle) + 1


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Toggle',
                              'actionvalue': str(next_toggle),
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData



def runAnalyzeFirstButton(probands, sceneName, devices):

    allData = []

    for prob in probands:


        for ger in devices:
            probandId = prob

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Start Scene',
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Button',
                              'actionvalue': '1',
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


def runAnalyzeButton(probands, sceneName, devices, button):

    allData = []

    for prob in probands:

        probandId = prob


        for ger in devices:

            x = col.find({  'scene': sceneName,
                            'dev': ger,
                            'action': 'Submit Button',
                            'actionvalue': button,
                            'prob': probandId
                            })

            x_list = list(x)


            if len(x_list) > 0:

                print('X-List' + str(x_list))

                startAction = x_list[0].get('time')
                startDate = x_list[0].get('date')

                next_button = int(button) + 1


                y = col.find({'scene': sceneName,
                              'dev': ger,
                              'action': 'Submit Button',
                              'actionvalue': str(next_button),
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

                x = None
                y = None
                y_list = None
                x_list = None

                endAction = None
                startAction = None

    return allData


# This is added so that many files can reuse the function get_database()
def boxplotCap(valArray):

    return f' \n n = {len(valArray)} \n \n ' \
            f'Median = {round(statistics.median(valArray), 1)} s \n ' \
            f'Mittelwert = {round(statistics.mean(valArray), 1)} s \n ' \
            f'S. Abw. = {round(statistics.stdev(valArray), 1)} s \n ' \
            f'u. Q. = {round(np.percentile(valArray, 25), 1)} s \n' \
            f'o. Q. = {round(np.percentile(valArray, 75), 1)} s ';


#f'\n n = {len(valArray)} \n Wert = {valArray}';


if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    col = dbname["uwp"]



    #probands = col.distinct('prob')
    # probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14']
    # probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A18']
    probands = ['A01', 'A02', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
                'A19', 'A20', 'A21', 'A22', 'A23', 'A24,' 'A25', 'A26', 'A27', 'A28']
    #probands = ['T15']


    sceneName = 'ILM_Submit-Far_Left_Scene'
    # devices = ['MQP', 'MQ2']
    devices = ['MQP']

    # Buttons
    sceneSubmitNearButton_Left = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearButton_2_Left = runAnalyzeButton(probands, sceneName, devices, '1')
    sceneSubmitNearButton_3_Left = runAnalyzeButton(probands, sceneName, devices, '2')

    # Toggle
    sceneSubmitNearToggle_Left = runAnalyzeFirstToggle(probands, sceneName, devices)
    sceneSubmitNearToggle_2_Left = runAnalyzeToggle(probands, sceneName, devices, '1')
    sceneSubmitNearToggle_3_Left = runAnalyzeToggle(probands, sceneName, devices, '2')

    # Slider
    sceneSubmitNearSlider_Left = runAnalyzeFirstSlider(probands, sceneName, devices)
    sceneSubmitNearSlider_2_Left = runAnalyzeSlider(probands, sceneName, devices, '1')
    sceneSubmitNearSlider_3_Left = runAnalyzeSlider(probands, sceneName, devices, '2')

    # Dropdown
    sceneSubmitNearDropdown_Left = runAnalyzeFirstDropdown(probands, sceneName, devices)
    sceneSubmitNearDropdown_2_Left = runAnalyzeDropdown(probands, sceneName, devices, '1')
    sceneSubmitNearDropdown_3_Left = runAnalyzeDropdown(probands, sceneName, devices, '2')


    sceneName = 'ILM_Submit-Far_Right_Scene'

    # Buttons
    sceneSubmitNearButton_Right = runAnalyzeFirstButton(probands, sceneName, devices)
    sceneSubmitNearButton_2_Right = runAnalyzeButton(probands, sceneName, devices, '1')
    sceneSubmitNearButton_3_Right = runAnalyzeButton(probands, sceneName, devices, '2')

    # Toggle
    sceneSubmitNearToggle_Right = runAnalyzeFirstToggle(probands, sceneName, devices)
    sceneSubmitNearToggle_2_Right = runAnalyzeToggle(probands, sceneName, devices, '1')
    sceneSubmitNearToggle_3_Right = runAnalyzeToggle(probands, sceneName, devices, '2')

    # Slider
    sceneSubmitNearSlider_Right = runAnalyzeFirstSlider(probands, sceneName, devices)
    sceneSubmitNearSlider_2_Right = runAnalyzeSlider(probands, sceneName, devices, '1')
    sceneSubmitNearSlider_3_Right = runAnalyzeSlider(probands, sceneName, devices, '2')

    # Dropdown
    sceneSubmitNearDropdown_Right = runAnalyzeFirstDropdown(probands, sceneName, devices)
    sceneSubmitNearDropdown_2_Right = runAnalyzeDropdown(probands, sceneName, devices, '1')
    sceneSubmitNearDropdown_3_Right = runAnalyzeDropdown(probands, sceneName, devices, '2')

    firstElementsRight = [sceneSubmitNearButton_Right,
                          sceneSubmitNearToggle_Right,
                          sceneSubmitNearSlider_Right,
                          sceneSubmitNearDropdown_Right]


    firstElementRightArray = []
    for elem in sceneSubmitNearButton_Right:
        firstElementRightArray.append(elem)

    for elem in sceneSubmitNearToggle_Right:
        firstElementRightArray.append(elem)

    for elem in sceneSubmitNearSlider_Right:
        firstElementRightArray.append(elem)

    for elem in sceneSubmitNearDropdown_Right:
        firstElementRightArray.append(elem)



    secondElementsRight = [sceneSubmitNearButton_2_Right, sceneSubmitNearButton_3_Right,
                     sceneSubmitNearToggle_2_Right, sceneSubmitNearToggle_3_Right,
                     sceneSubmitNearSlider_2_Right,sceneSubmitNearSlider_3_Right,
                     sceneSubmitNearDropdown_2_Right, sceneSubmitNearDropdown_3_Right]

    secondElementRightArray = []
    for elem in sceneSubmitNearButton_2_Right:
        secondElementRightArray.append(elem)

    for elem in sceneSubmitNearButton_3_Right:
        secondElementRightArray.append(elem)

    for elem in sceneSubmitNearToggle_2_Right:
        secondElementRightArray.append(elem)

    for elem in sceneSubmitNearToggle_3_Right:
        secondElementRightArray.append(elem)

    for elem in sceneSubmitNearSlider_2_Right:
        secondElementRightArray.append(elem)

    for elem in sceneSubmitNearSlider_3_Right:
        secondElementRightArray.append(elem)

    for elem in sceneSubmitNearDropdown_2_Right:
        secondElementRightArray.append(elem)

    for elem in sceneSubmitNearDropdown_3_Right:
        secondElementRightArray.append(elem)

    boxplotElementRightArray = [firstElementRightArray, secondElementRightArray]

    allTimesRight = [sceneSubmitNearButton_Right, sceneSubmitNearButton_2_Right, sceneSubmitNearButton_3_Right,
                     sceneSubmitNearToggle_Right, sceneSubmitNearToggle_2_Right, sceneSubmitNearToggle_3_Right,
                     sceneSubmitNearSlider_Right, sceneSubmitNearSlider_2_Right, sceneSubmitNearSlider_3_Right,
                     sceneSubmitNearDropdown_Right, sceneSubmitNearDropdown_2_Right, sceneSubmitNearDropdown_3_Right]


    ### LEFT

    firstElementsLeft = [sceneSubmitNearButton_Left,
                         sceneSubmitNearToggle_Left,
                         sceneSubmitNearSlider_Left,
                         sceneSubmitNearDropdown_Left]


    secondElementsLeft = [ sceneSubmitNearButton_2_Left, sceneSubmitNearButton_3_Left,
                     sceneSubmitNearToggle_2_Left, sceneSubmitNearToggle_3_Left,
                     sceneSubmitNearSlider_2_Left, sceneSubmitNearSlider_3_Left,
                     sceneSubmitNearDropdown_2_Left, sceneSubmitNearDropdown_3_Left]


    firstElementsLeftArray = []
    for elem in sceneSubmitNearButton_Left:
        firstElementsLeftArray.append(elem)

    for elem in sceneSubmitNearToggle_Left:
        firstElementsLeftArray.append(elem)

    for elem in sceneSubmitNearSlider_Left:
        firstElementsLeftArray.append(elem)

    for elem in sceneSubmitNearDropdown_Left:
        firstElementsLeftArray.append(elem)


    secondElementsLeftArray = []
    for elem in sceneSubmitNearButton_2_Left:
        secondElementsLeftArray.append(elem)

    for elem in sceneSubmitNearButton_3_Left:
        secondElementsLeftArray.append(elem)


    for elem in sceneSubmitNearToggle_2_Left:
        secondElementsLeftArray.append(elem)

    for elem in sceneSubmitNearToggle_3_Left:
        secondElementsLeftArray.append(elem)


    for elem in sceneSubmitNearDropdown_2_Left:
        secondElementsLeftArray.append(elem)

    for elem in sceneSubmitNearDropdown_3_Left:
        secondElementsLeftArray.append(elem)

    for elem in sceneSubmitNearSlider_2_Left:
        secondElementsLeftArray.append(elem)

    for elem in sceneSubmitNearSlider_3_Left:
        secondElementsLeftArray.append(elem)

    boxplotElementLeftArray = [firstElementsLeftArray, secondElementsLeftArray]


    allTimesLeft = [sceneSubmitNearButton_Left, sceneSubmitNearButton_2_Left, sceneSubmitNearButton_3_Left,
                    sceneSubmitNearToggle_Left, sceneSubmitNearToggle_2_Left, sceneSubmitNearToggle_3_Left,
                    sceneSubmitNearSlider_Left, sceneSubmitNearSlider_2_Left, sceneSubmitNearSlider_3_Left,
                    sceneSubmitNearDropdown_Left, sceneSubmitNearDropdown_2_Left, sceneSubmitNearDropdown_3_Left]


    # ALL

    firstElementsArray = []

    for elem in firstElementsLeftArray:
        firstElementsArray.append(elem)

    for elem in firstElementRightArray:
        firstElementsArray.append(elem)


    secondElementsArray = []

    for elem in secondElementsLeftArray:
        secondElementsArray.append(elem)

    for elem in secondElementRightArray:
        secondElementsArray.append(elem)

    boxplotElementArray = [firstElementsArray, secondElementsArray]




    fig, axs = plt.subplots(1, 3, figsize=(10, 8))


    fig.suptitle('Bearbeitungszeit aller Schaltflächen mit dem Submit Near Operator')
    # ax = fig.add_axes(['Rechte Hand', 'Linke Hand'])

    axs[0].boxplot(boxplotElementRightArray, notch=False)

    axs[1].boxplot(boxplotElementLeftArray, notch=False)
    axs[2].boxplot(boxplotElementArray, notch=False)
    axs[1].sharey(axs[0])
    axs[2].sharey(axs[0])



    axs[0].set(ylabel='Sekunden')
    axs[1].set(ylabel='Sekunden')
    axs[2].set(ylabel='Sekunden')


    axs[0].set_title('Erste Szenen mit der rechten Hand')
    axs[0].set_xticks([1, 2], [
                                  "Erste Schaltflächen" + boxplotCap(boxplotElementRightArray[0]),
                                  "Nachgelagerte Schalftlächen" + boxplotCap(boxplotElementRightArray[1])

                                  ])


    axs[1].set_title('Zweite Szenen mit der linken Hand')
    axs[1].set_xticks([1, 2], [

                                    "Erste Schaltflächen" + boxplotCap(boxplotElementLeftArray[0]),
                                    "Nachgelagerte Schalftlächen" + boxplotCap(boxplotElementLeftArray[1])

                                ])

    axs[2].set_title('Beide Hände zusammengefasst')
    axs[2].set_xticks([1, 2], [

                                    "Erste Schaltflächen" + boxplotCap(boxplotElementArray[0]),
                                    "Nachgelagerte Schalftlächen" + boxplotCap(boxplotElementArray[1])

                                ])



    plt.show()


