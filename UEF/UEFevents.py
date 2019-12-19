import pandas as pd
import os
import numpy as np

def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    try: 
        if isclose(array[idx], value, abs_tol=1):
            return idx
    except:
        pass
    return idx-1

def splitOnEvents(dfC, dfE, events, startings, endings):
    
    for event, starting, ending in zip(events, startings, endings):
        dfC[event+' no']=0
        dfC[event]=event+'0'
        #Indecies of event
        starting_indeces = dfE.loc[dfE['Desc'].str.contains(starting)]
        ending_indeces = dfE.loc[dfE['Desc'].str.contains(ending)]
        for i, j in zip(range(0, len(starting_indeces)), range(0, len(ending_indeces))):
            start_event_time = starting_indeces.iloc[i][1]
            end_event_time = ending_indeces.iloc[j][1]
            start_idx = find_nearest(dfC['TimeStamp (sec)'].values, start_event_time)
            end_idx = find_nearest(dfC['TimeStamp (sec)'].values, end_event_time)
            dfC.loc[start_idx:end_idx, event+' no']=i+1
            dfC.loc[start_idx:end_idx, event]=event+str(i+1)
            
    #Create a 'Waiting For T' column
    dfC['Waiting for T']=0
    indeces = dfE.loc[dfE['Desc'].str.contains('Waiting for T')]
    for i in range(0, len(indeces)):
        time = indeces.iloc[i][1] 
        idx = find_nearest(dfC['TimeStamp (sec)'].values, time)
        dfC.loc[idx, 'Waiting for T']=str(i+1)
            
    return dfC