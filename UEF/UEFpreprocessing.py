import pandas as pd
import os
import numpy as np
from math import isclose
import re
import UEFcleaning as c
import UEFevents as e
import UEFeff as f

def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    try: 
        if isclose(array[idx], value, abs_tol=1):
            return idx
    except:
        pass
    return idx-1

events_dir = r'C:\Niagara\UEF\Events'
channels_dir = r'C:\Niagara\UEF\Channels'
variables_dir = r'C:\Niagara\UEF\Variables'
resultPath = r'C:\Niagara\Preprocessing_UEF'
events = ['Purge', 'Draw', 'Cut']
startings = ['Starting Purge', 'Starting Draw', 'Cut IN']
endings = ['Ending Purge', 'Draw Complete', 'Cut OUT']

for fileName in os.listdir(channels_dir):
    print('File name:', fileName)

    #Skip files with a lot of missing data
    df = pd.read_csv(os.path.join(channels_dir, fileName))
    if df.shape[0]<1000:
        continue
    
    #Select and add useful columns
    dfC = c.clean(fileName, channels_dir)        
    dfE = pd.read_csv(os.path.join(events_dir, fileName))
    dfV = pd.read_csv(os.path.join(variables_dir, fileName))
    
    #Create a new column for each event with the number of the event
    dfC = e.splitOnEvents(dfC, dfE, events, startings, endings)
    
    #Calculate efficiency
    dfC = f.effCalc(dfC, dfE, dfV)
    
    dfC.to_csv(os.path.join(resultPath,fileName), index = False)
    print('\n\n\n\n')