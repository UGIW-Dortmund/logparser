import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pymongo import MongoClient
import seaborn as sns

import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf


if __name__ == '__main__':

    allValues = []

    val_Ad_MQ2 = gf.getDb('Val-Ad-MQ2')
    allValues.append(val_Ad_MQ2)
    val_Ad_MQP = gf.getDb('Val-Ad-MQP')
    val_Ad = gf.getDb('Val-Ad')

    val_Wi_HL2 = gf.getDb('Val-Wi-HL2')
    val_Wi_HPG2 = gf.getDb('Val-Wi-HPG2')

    descArray = ['Val-Ad-MQ2', 'Val-Ad-MQP', 'Val-Ad', 'Val-Wi-HL2', 'Val-Wi-HPG2']

    print(val_Wi_HPG2)