# Readme ILM-Parser

This Parser is for proceeding the Log Files of the ILM project.

## Scripts
### test.py
Testing the single scripts for VR


### ILM_logReaderVR.py
Parser dedicated for ILM log files which are slightly different to the previous from UGIW


## Universal Tools

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