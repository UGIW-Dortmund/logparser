# Readme ILM-Parser

This Parser is for proceeding the Log Files of the ILM project.

## Scripts
### test.py
Testing the single scripts for VR


## Write Deltas to Database 
Name of the database is tresor

```
def writeToDb(name, value):
    dbname = get_database()
    tresor = dbname["tresor"]

    dto = {"name": name, "value": value}
    tresor.insert_one(dto)
```

### ILM_logReaderVR.py
Parser dedicated for ILM log files which are slightly different to the previous from UGIW


## Universal Tools

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