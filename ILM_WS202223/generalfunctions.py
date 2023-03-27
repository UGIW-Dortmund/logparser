import pandas as pd
import statistics
import numpy as np

from pymongo import MongoClient


probands = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
            'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20',
            'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27', 'A28']

probandsFemale = ['A02', 'A16', 'A04', 'A19', 'A22', 'A24', 'A26', 'A23']

probandsMale = ['A01', 'A03', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14',
                'A15', 'A18', 'A20', 'A21', 'A25', 'A28', 'A27', 'A17']

probandsHandLeft = ['A15', 'A28']

probandsHandRight = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10',
            'A11', 'A12', 'A13', 'A14', 'A16', 'A17', 'A18', 'A19', 'A20',
            'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27']


##### Database
def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://fredix:memphis55@kurz-containar.de:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['ilm']

def writeToDb(name, value):
    dbname = get_database()
    tresor = dbname["tresor"]

    dto = tresor.find({"name": name})
    dto = list(dto)

    print("Dto")
    print(dto)

    if (len(dto) > 0):
        dto = {"name": name}
        newvalues = {"$set": {"values": value}}
        tresor.update_one(dto, newvalues)
        print("Update element")
    else:
        dto = {"name": name, "values": value}
        tresor.insert_one(dto)
        print("New element")


def getDb(queryParam):
    dbname = get_database()
    tresor = dbname["tresor"]
    queryResult = tresor.find_one({'name': str(queryParam)})
    queryResult = convertToFloat1D(queryResult)
    return queryResult



def test():
    print('test GF blub')


### Data Helpers
def aggregateData(array):
    lenArray = len(array)
    print("Len array " + str(lenArray))
    data = []

    for i in range(0, lenArray):
        for elem in array[i]:
            data.append(elem)

    return data;



def convertToFloat2D(arr):

    print(arr)

    arr2 = arr.get('values')

    print(arr2)

    arr2 = list(arr2)
    lenArray = len(arr2)

    print(lenArray)

    allValues = []

    for e in range(0, lenArray):
        floatValues = []

        for elem in arr2[e]:
            floatValues.append(float(elem))

        allValues.append(floatValues)

    return allValues


def convertToFloat1D(arr):

    arr2 = arr.get('values')

    allValues = []

    for e in arr2:

        allValues.append(float(e))

    return allValues





### Boxplots

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






def boxplotCapMin(valArray):
    median = round(statistics.median(valArray), 1)
    median = str(median).replace('.', ',')

    mean = round(statistics.mean(valArray), 1)
    mean = str(mean).replace('.', ',')


    return f'\n\n {len(valArray)} \n' \
           f'{median} s \n ' \
           f'{mean} s \n ';



##### LATEX #################

def reqLatexTableOutput(values, names):

    i = 0

    for v in values:
        latexTableOutput(names[i], v)
        i = i + 1

def latexTableOutput(opName, valArray):
    nNumber = len(valArray)

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

    print(f'{opName} & {nNumber} & {median} s & {mean} s & {stdev} s & {first_quartil} s & {third_quartil} s \\\ ')



def aggregateData(array):
    lenArray = len(array)
    print("Len array " + str(lenArray))
    data = []

    for i in range(0, lenArray):
        for elem in array[i]:
            data.append(elem)

    return data;


def setXTicks_param(valArray, descArray):
    xtick = []
    i = 0
    df = pd.DataFrame()

    # The descirption of fields
    for elem in valArray:
        s = boxplotCap(elem)

        df_entry = dfEntryMax(descArray[i], elem, i)
        df.insert(loc=(len(df.columns)), column=descArray[i], value=df_entry)

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

    return (elements, xtick, df)


def setXTicksMin(valArray, descArray):
    xtick = []
    i = 0
    df = pd.DataFrame()

    rows = []

    # The descirption of fields
    for elem in valArray:

        print("Element")
        print(elem)

        df_entry = dfEntry(descArray[i], elem, i)
        df.insert(loc=(len(df.columns)), column=descArray[i], value=df_entry)

        s = boxplotCapMin(elem)



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

    # df = pd.DataFrame(rows)

    return (elements, xtick, df)



def dfEntry(nameElement, valArray, indexI):
    nuTuple = len(valArray)
    nuTuple = str(nuTuple)

    median = round(statistics.median(valArray), 1)
    # median = float(median)
    median = str(median).replace('.', ',')
    median = median + ' s'

    mean = round(statistics.mean(valArray), 1)
    mean = str(mean).replace('.', ',')
    mean = mean + ' s'

    stdev = round(statistics.stdev(valArray), 1)
    # stdev = str(stdev).replace('.', ',')

    first_quartil = round(np.percentile(valArray, 25), 1)
    # first_quartil = str(first_quartil).replace('.', ',')

    third_quartil = round(np.percentile(valArray, 75), 1)
    # third_quartil = str(third_quartil).replace('.', ',')

    new_row = pd.DataFrame()
    #new_row = {'median': median,
    #           'mean': mean, 'stdev': stdev,
    #           'first_quartil': first_quartil, 'third_quartil': third_quartil}
    new_row = ({'n': nuTuple, 'Median': median, 'Mittelwert': mean})

    return new_row


def dfEntryMax(nameElement, valArray, indexI):
    nuTuple = len(valArray)
    nuTuple = str(nuTuple)

    median = round(statistics.median(valArray), 1)
    # median = float(median)
    median = str(median).replace('.', ',')
    median = median + ' s'

    mean = round(statistics.mean(valArray), 1)
    mean = str(mean).replace('.', ',')
    mean = mean + ' s'

    stdev = round(statistics.stdev(valArray), 1)
    stdev = str(stdev).replace('.', ',')
    stdev = str(stdev) + ' s'

    first_quartil = round(np.percentile(valArray, 25), 1)
    first_quartil = str(first_quartil).replace('.', ',')
    first_quartil = first_quartil + ' s'

    third_quartil = round(np.percentile(valArray, 75), 1)
    third_quartil = str(third_quartil).replace('.', ',')
    third_quartil = str(third_quartil) + ' s'


    new_row = pd.DataFrame()
    #new_row = {'median': median,
    #           'mean': mean, 'stdev': stdev,
    #           'first_quartil': first_quartil, 'third_quartil': third_quartil}
    new_row = ({'n': nuTuple, 'Median': median, 'Mittelwert': mean,
                'S. Abw.': stdev, 'u. Q.': first_quartil, 'o. Q.': third_quartil})

    return new_row

def setXTicks_param_plain(valArray, descArray):
    xtick = []
    i = 0

    # The descirption of fields
    for elem in valArray:
        s = ''
        # str(elem)
        # boxplotCap(elem)

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



