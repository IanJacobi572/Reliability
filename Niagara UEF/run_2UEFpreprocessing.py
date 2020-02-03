import pandas as pd
import os
import numpy as np
from math import isclose
import re
import UEFcleaning as c
import UEFevents as e
import UEFeffCalc as f

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
#resultPath = r'C:\Niagara\Takashi_Preprocessing_UEF'
events = ['Purge', 'Draw', 'Cut']
startings = ['Starting Purge', 'Starting Draw', 'Cut IN']
endings = ['Ending Purge', 'Draw Complete', 'Cut OUT']
ICNs = [10266, 10289, 10493, 10494, 10636, 10637, 10638, 10792]
#ICNs = [10266]

for fileName in os.listdir(channels_dir):
    print('File name:', fileName)
    
    #for elm in ICNs:
    #    if str(elm) in fileName:
    #Skip files with a lot of missing data
    dfC = pd.read_csv(os.path.join(channels_dir, fileName))
    if dfC.shape[0]<1000 or fileName=='ST4 ICN 10493 RTGH-S11iS1-6928.SM22014.csv' or os.path.isfile(fileName):
        continue
    
    dfC = c.clean(fileName, channels_dir)
    dfE = pd.read_csv(os.path.join(events_dir, fileName))
    dfV = pd.read_csv(os.path.join(variables_dir, fileName))
    
    #Create a new column for each event with the number of the event
    dfCC = e.splitOnEvents(dfC, dfE, events, startings, endings)
    
    #Calculate efficiency
    dfC = f.effCalc(dfC, dfE, dfV)
    
    dfCC['Validity']='Valid'       
    #Check if Room Temperature in range 65-70 and draws are 14 or (more?)
    if (dfC['Ambient TC'].astype('float64') > 70).any() or (dfC['Ambient TC'] < 65).any() or max(dfC['Draw no'].astype('int64').values)<14:
        dfC['Validity']='Not Valid'
    #If it's still valid then check Tin during draws if it's in range 56-60
    else:
        for i in range(1,dfC['Draw no'].max()+1):
            t1 = dfC.loc[dfC['Draw no']==i, 'TimeStamp (sec)'].iloc[0]
            idx1 = find_nearest(dfC['TimeStamp (sec)'].values, t1+5)
            idx2 = dfC.index[dfC['Draw no']==i][-1]
            x = (dfC.loc[idx1:idx2, 'Tin']<56).any()
            if (dfC.loc[idx1:idx2, 'Tin']<56).any() or (dfC.loc[idx1:idx2, 'Tin']>60).any():
                dfC['Validity']='Not Valid'
                break
                
    dfC.to_csv(os.path.join(resultPath,fileName), index = False)
    print('\n\n\n\n')
#        else:
#            continue