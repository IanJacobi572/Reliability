import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import Gen5Info as Info

directory = r'C:\gen5\prp'
resultPath = r'C:\gen5\withCycles'

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))   
    print(fileName)
    
    #Cleaning debug
    for column in list(Info.columns.keys()):
        trash=[value for value in df[column].unique() if value not in Info.columns.get(column)]
        if len(trash)!=0:
            print(column, 'trash values: ', trash)
            
    print('\n\n\n')