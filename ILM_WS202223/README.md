# Readme ILM-Parser

This Parser is for proceeding the Log Files of the ILM project.

## Scripts

### Standart Queries

#### UWP_gaze_Times.py
Getting all execution times of the `Gaze Operator`.

#### UWP_gaze_Times_db.py

Getting the data from above from the db.

#### UWP_gaze_Times_db_aggr_db.py
Aggregates the data from above by retrieving it from the db.

####  test.py
Testing the single scripts for VR



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

    return f' \n n = {len(valArray)} \n \n ' \
            f'Me. = {round(statistics.median(valArray), 3)} s \n ' \
            f'Mi. = {round(statistics.mean(valArray), 3)} s \n ' \
            f'S. Ab. = {round(statistics.stdev(valArray), 3)} s \n ' \
            f'M. Ab. = {round(mean(valArray), 3)} s \n ' \
            f'1Q = {round(np.percentile(valArray, 25), 3)} s \n' \
            f'3Q = {round(np.percentile(valArray, 75), 3)} s ';

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