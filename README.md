# Readme ILM-Parser

This Parser is for proceeding the Log Files of the ILM project.

## Styling
In order to read the text of the diagramms properly on DIN A4 pages. 
Add the following settings to the diagramms: 

``
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf
``

 
- X-Ticks 
  - ``plt.xticks(num, val, fontsize=12)``
  - ``fig.suptitle('This is the figure title', fontsize=12)``


- Diagramm Title 
`` plt.title('XXX', fontsize=15)``


- X- and Y-Label: 
``plt.ylabel('XXX', fontsize=12)``
``axs[0].set_xlabel('X-Koordinaten', fontsize=12)``

- X-Ticks
``axs[0].xaxis.set_tick_params(labelsize=12)``

- Grid on the line 
``axs[0].yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)``


- Table with Values and Dataframe
``
from pandas.plotting import table
ttable = table(axs[0], df_Right, loc='bottom', colLoc='center', cellLoc='center')
for key, cell in ttable.get_celld().items():
    cell.set_edgecolor('lightgrey')
    cell.set_height(0.05)
ttable.set_fontsize(12)
ttable.auto_set_font_size(False)
``


``
fig, axs = plt.subplots(1, 1, figsize=(10, 8))
ttable = table(axs, df, loc='bottom', colLoc='center', cellLoc='center')
plt.xticks([])
axs.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
plt.grid(axis='y', linestyle='-', which='major', color='lightgrey', alpha=0.5)
``

SNS Swarm- and Violinplot
``
sns.violinplot(allBoxplot, showmeans=True, color="skyblue")
sns.swarmplot(allBoxplot, color="black")
``

## Scripts

- `` generalfunctions ``: Script which inculdes all necesary functions which are shared all over other functions
- 

### scene_Grab

#### MQ
- ``GR_MQ_Times `` Aggregation of all times
- `` GR_MQ_Times_boxes `` Separation of the different cubes in the android scene.
- `` GR_MQ_Times_First-Second `` Separation into first and second times


#### UWP
- ``GR_UWP_Times `` Checks if the Cubes are in the correct place and get the delta times 
- ``GR_UWP_Times_boxes `` Checks the times of the four different cubes.

### scene_Point

#### MQ
- ``PO_MQ_Times``: Getting all times for pointing at the MQ applications

### scene_submitFar


#### all
- ```SF_ALL.py```: Aggregiert alle Werte der nachgelagerten Schaltflächen.

#### UWP

- ``UWP_submitFar_First_Times``: Die Zeiten der ersten Schaltflächen aller Windows-Anwendungen
- ``UWP_submitFar_Second_Times_2``: Die Zeiten aller nachgelagerten Schaltflächen für den SF-Operator
- - ``UWP_submitFar_Second_Times.py``: Vorherige Version des oberen Skript mit einer groben Aggregation



## Universal Tools

### Write Deltas to Database 
This is increasing the query times tremendously.
Name of the database is `tresor`. 
First it proves if there is any similar dataset already existing. If not it will create a new tuple.

```
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

```

### Converting data from the db
Data from db is retrieved as strings. This method turns it into floats.


This is for 2 Dimensions Array
```
def convertToFloat(arr):

    arr = arr.get('values')

    print(arr)

    arr = list(arr)
    lenArray = len(arr)

    print(lenArray)

    allValues = []

    for e in range(0, lenArray):
        floatValues = []

        for elem in arr[e]:
            floatValues.append(float(elem))

        allValues.append(floatValues)

    return allValues
```


This is for 1 Dimension Array
```
def convertToFloat(arr):
    print(arr)
    arr2 = arr.get('values')
    print(arr2)
    arr2 = list(arr2)
    lenArray = len(arr2)
    print(lenArray)

    allValues = []

    for e in range(0, lenArray):
        allValues.append(float(e))



    return allValues
```


### Flatten the data 
Having a 2D array it turns it into 1D array.
```
def aggregateData(array):
    lenArray = len(array)
    print("Len array " + str(lenArray))
    data = []

    for i in range(0, lenArray):
        for elem in array[i]:
            data.append(elem)

    return data;
 ```

### ILM_logReaderVR.py
Parser dedicated for ILM log files which are slightly different to the previous from UGIW



### Boxplot
Giving caption with stat values to the boxplots
```
def boxplotCap(valArray):
    median = round(statistics.median(valArray), 2)
    median = str(median).replace('.', ',')

    mean = round(statistics.mean(valArray), 2)
    mean = str(mean).replace('.', ',')

    stdev = round(statistics.stdev(valArray), 2)
    stdev = str(stdev).replace('.', ',')

    first_quartil = round(np.percentile(valArray, 25), 2)
    first_quartil = str(first_quartil).replace('.', ',')

    third_quartil = round(np.percentile(valArray, 75), 2)
    third_quartil = str(third_quartil).replace('.', ',')


    return f'\n n = {len(valArray)} \n' \
           f'Me. = {median} s \n ' \
           f'Mi. = {mean} s \n ' \
           f'S. Abw. = {stdev} s \n ' \
           f'U.Q. = {first_quartil} s \n ' \
           f'O.Q. = {third_quartil} s';
```

### Aggregate Data
Method to put data of various arrays togehter.
```
def aggregateData(array):

    lenArray = len(array)
    print("Len array " + str(lenArray) )
    data = []

    for i in range(0, lenArray):
        for elem in array[i]:
            data.append(elem)

    return data;
```