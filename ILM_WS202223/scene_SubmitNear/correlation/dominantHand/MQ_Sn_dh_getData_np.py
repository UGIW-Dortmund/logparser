import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics
from statistics import mean

import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf

import seaborn as sns
from pandas.plotting import table

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

    # for prob in probands:


    for ger in devices:
        probandId = probands

        x = col.find({  'scene': sceneName,
                        'dev': ger,
                        'action': 'Submit Slider',
                        'actionvalue': 'Slider3',
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            # print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')


            y = col.find({'scene': sceneName,
                          'dev': ger,
                          'action': 'Submit Dropdown',
                          'actionvalue': 'Dropdown1',
                          'prob': probandId,
                          })

            y_list = list(y)

            # print('Y-List' + str(y_list))

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

    # for prob in probands:

    probandId = probands


    for ger in devices:

        x = col.find({  'scene': sceneName,
                        'dev': ger,
                        'action': 'Submit Dropdown',
                        'actionvalue': 'Dropdown' + str(dropdown),
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            # print('X-List' + str(x_list))

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

            # print('Y-List' + str(y_list))

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

    # for prob in probands:


    for ger in devices:
        probandId = probands

        x = col.find({  'scene': sceneName,
                        'dev': ger,
                        'action': 'Submit Toggle',
                        'actionvalue': '3',
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            # print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')


            y = col.find({'scene': sceneName,
                          'dev': ger,
                          'action': 'Submit Slider',
                          'actionvalue': 'Slider1',
                          'prob': probandId,
                          })

            y_list = list(y)

            # print('Y-List' + str(y_list))

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

    # for prob in probands:

    probandId = probands


    for ger in devices:

        x = col.find({  'scene': sceneName,
                        'dev': ger,
                        'action': 'Submit Slider',
                        'actionvalue': 'Slider' + str(slider),
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            # print('X-List' + str(x_list))

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

            # print('Y-List' + str(y_list))

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

    # for prob in probands:


    for ger in devices:
        probandId = probands

        x = col.find({  'scene': sceneName,
                        'dev': ger,
                        'action': 'Submit Button',
                        'actionvalue': '3',
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            # print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')


            y = col.find({'scene': sceneName,
                          'dev': ger,
                          'action': 'Submit Toggle',
                          'actionvalue': '1',
                          'prob': probandId,
                          })

            y_list = list(y)

            # print('Y-List' + str(y_list))

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

                #print('X-List' + str(x_list))

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

                #print('Y-List' + str(y_list))

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

    #for prob in probands:


    for ger in devices:
        probandId = probands

        x = col.find({  'scene': sceneName,
                        'dev': ger,
                        'action': 'Start Scene',
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            #print('X-List' + str(x_list))

            startAction = x_list[0].get('time')
            startDate = x_list[0].get('date')


            y = col.find({'scene': sceneName,
                          'dev': ger,
                          'action': 'Submit Button',
                          'actionvalue': '1',
                          'prob': probandId,
                          })

            y_list = list(y)

            #print('Y-List' + str(y_list))

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

    # for prob in probands:

    probandId = probands


    for ger in devices:

        x = col.find({  'scene': sceneName,
                        'dev': ger,
                        'action': 'Submit Button',
                        'actionvalue': button,
                        'prob': probandId
                        })

        x_list = list(x)


        if len(x_list) > 0:

            # print('X-List' + str(x_list))

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

            # print('Y-List' + str(y_list))

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


def writeToDb(name, value):
    dbname = get_database()
    tresor = dbname["tresor"]

    dto = {"name": name, "values": value}
    tresor.insert_one(dto)



# This is added so that many files can reuse the function get_database()
def boxplotCap(valArray):

    return f' \n n = {len(valArray)} \n \n ' \
            f'Me. = {round(statistics.median(valArray), 3)} s \n ' \
            f'Mi. = {round(statistics.mean(valArray), 3)} s \n ' \
            f'S. Ab. = {round(statistics.stdev(valArray), 3)} s \n ' \
            f'M. Ab. = {round(mean(valArray), 3)} s \n ' \
            f'1Q = {round(np.percentile(valArray, 25), 3)} s \n' \
            f'3Q = {round(np.percentile(valArray, 75), 3)} s ';


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

    probands = gf.probandsHandLeft

    sceneNameLeft = 'ILM_Submit-Near_Left_Scene'
    sceneNameRight = 'ILM_Submit-Near_Right_Scene'

    devices = ['MQP', 'MQ2']


    all_Sn_1 = []
    all_Sn_2 = []


    for p in probands:

        # Buttons
        sceneSubmitNearButton_Left = runAnalyzeFirstButton(p, sceneNameLeft, devices)
        sceneSubmitNearButton_2_Left = runAnalyzeButton(p, sceneNameLeft, devices, '1')
        sceneSubmitNearButton_3_Left = runAnalyzeButton(p, sceneNameLeft, devices, '2')

        # Toggle
        sceneSubmitNearToggle_Left = runAnalyzeFirstToggle(p, sceneNameLeft, devices)
        sceneSubmitNearToggle_2_Left = runAnalyzeToggle(p, sceneNameLeft, devices, '1')
        sceneSubmitNearToggle_3_Left = runAnalyzeToggle(p, sceneNameLeft, devices, '2')

        # Slider
        sceneSubmitNearSlider_Left = runAnalyzeFirstSlider(p, sceneNameLeft, devices)
        sceneSubmitNearSlider_2_Left = runAnalyzeSlider(p, sceneNameLeft, devices, '1')
        sceneSubmitNearSlider_3_Left = runAnalyzeSlider(p, sceneNameLeft, devices, '2')

        # Dropdown
        sceneSubmitNearDropdown_Left = runAnalyzeFirstDropdown(p, sceneNameLeft, devices)
        sceneSubmitNearDropdown_2_Left = runAnalyzeDropdown(p, sceneNameLeft, devices, '1')
        sceneSubmitNearDropdown_3_Left = runAnalyzeDropdown(p, sceneNameLeft, devices, '2')

        # Buttons
        sceneSubmitNearButton_Right = runAnalyzeFirstButton(p, sceneNameRight, devices)
        sceneSubmitNearButton_2_Right = runAnalyzeButton(p, sceneNameRight, devices, '1')
        sceneSubmitNearButton_3_Right = runAnalyzeButton(p, sceneNameRight, devices, '2')

        # Toggle
        sceneSubmitNearToggle_Right = runAnalyzeFirstToggle(p, sceneNameRight, devices)
        sceneSubmitNearToggle_2_Right = runAnalyzeToggle(p, sceneNameRight, devices, '1')
        sceneSubmitNearToggle_3_Right = runAnalyzeToggle(p, sceneNameRight, devices, '2')

        # Slider
        sceneSubmitNearSlider_Right = runAnalyzeFirstSlider(p, sceneNameRight, devices)
        sceneSubmitNearSlider_2_Right = runAnalyzeSlider(p, sceneNameRight, devices, '1')
        sceneSubmitNearSlider_3_Right = runAnalyzeSlider(p, sceneNameRight, devices, '2')

        # Dropdown
        sceneSubmitNearDropdown_Right = runAnalyzeFirstDropdown(p, sceneNameRight, devices)
        sceneSubmitNearDropdown_2_Right = runAnalyzeDropdown(p, sceneNameRight, devices, '1')
        sceneSubmitNearDropdown_3_Right = runAnalyzeDropdown(p, sceneNameRight, devices, '2')


        print(f"each proband {str(p)}" )

        ## Sn-1
        Sn_1 = [sceneSubmitNearButton_Left, sceneSubmitNearToggle_Left, sceneSubmitNearSlider_Left, sceneSubmitNearDropdown_Left,
                sceneSubmitNearButton_Right, sceneSubmitNearToggle_Right, sceneSubmitNearSlider_Right, sceneSubmitNearDropdown_Right ]

        Sn_1 = gf.aggregateData(Sn_1)

        if Sn_1 != []:
            print(Sn_1)
            Sn_1 = statistics.mean(Sn_1)
            all_Sn_1.append(Sn_1)



        Sn_2 = [sceneSubmitNearButton_2_Left, sceneSubmitNearButton_3_Left, sceneSubmitNearToggle_2_Left, sceneSubmitNearToggle_3_Left,
                sceneSubmitNearSlider_2_Left, sceneSubmitNearSlider_3_Left, sceneSubmitNearDropdown_2_Left, sceneSubmitNearDropdown_3_Left,
                sceneSubmitNearButton_2_Right, sceneSubmitNearButton_3_Right, sceneSubmitNearToggle_2_Right, sceneSubmitNearToggle_3_Right,
                sceneSubmitNearSlider_2_Right, sceneSubmitNearSlider_3_Right, sceneSubmitNearDropdown_2_Right, sceneSubmitNearDropdown_3_Right]
        Sn_2 = gf.aggregateData(Sn_2)

        if Sn_2 != []:
            print(Sn_2)
            Sn_2 = statistics.mean(Sn_2)
            all_Sn_2.append(Sn_2)




    ### LEFT

    firstElementsLeft = [sceneSubmitNearButton_Left,
                         sceneSubmitNearToggle_Left,
                         sceneSubmitNearSlider_Left,
                         sceneSubmitNearDropdown_Left]

    firstElementsLeft = gf.aggregateData(firstElementsLeft)


    secondElementsLeft = [ sceneSubmitNearButton_2_Left, sceneSubmitNearButton_3_Left,
                     sceneSubmitNearToggle_2_Left, sceneSubmitNearToggle_3_Left,
                     sceneSubmitNearSlider_2_Left, sceneSubmitNearSlider_3_Left,
                     sceneSubmitNearDropdown_2_Left, sceneSubmitNearDropdown_3_Left]

    secondElementsLeft = gf.aggregateData(secondElementsLeft)



    boxplotElementLeftArray = [firstElementsLeft, secondElementsLeft]




    Ad_Sn_1 = [firstElementsLeft]
    Ad_Sn_1 = gf.aggregateData(Ad_Sn_1)
    gf.writeToDb('Sn-Ad-1-DH-L', all_Sn_1)


    Ad_Sn_2 = [secondElementsLeft]
    Ad_Sn_2 = gf.aggregateData(Ad_Sn_2)
    gf.writeToDb('Sn-Ad-2-DH-L', all_Sn_2)

    Ad_Sn = [Ad_Sn_1, Ad_Sn_2]

    fig, axs = plt.subplots(1, 2, figsize=(10, 8))


    fig.suptitle('Correlation: Submit Near Operator', fontsize=15)


    axs[1].sharey(axs[0])

    axs[0].set_ylabel('Sekunden', fontsize=12)
    axs[1].set_ylabel('Sekunden', fontsize=12)

    descArray = ["Sn-1-Ad", "Sn-2-Ad"]

    num, val, df1 = gf.setXTicks_param(Ad_Sn, descArray)


    axs[0].set_title('Sn-Ad', fontsize=15)
    ttable = table(axs[0], df1, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    sns.violinplot(Ad_Sn, showmeans=True, color="skyblue", ax=axs[0])
    sns.swarmplot(Ad_Sn, color="black", ax=axs[0])
    axs[0].set_xticks([])

    descArray = ["Sn-1-Ad-L", "Sn-2-Ad-L"]

    num, val, df2 = gf.setXTicks_param(boxplotElementLeftArray, descArray)
    sns.violinplot(boxplotElementLeftArray, showmeans=True, color="skyblue", ax=axs[1])
    sns.swarmplot(boxplotElementLeftArray, color="black", ax=axs[1])
    df2 = df2.reset_index(drop=True)
    axs[1].set_title('2. Linke Hand', fontsize=15)
    ttable = table(axs[1], df2, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    axs[1].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    axs[1].set_xticks([])

    #plt.show()


