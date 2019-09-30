import pandas as pd
import os
import numpy as np
from math import isclose
import re
import UEFPreProcessing as pp

def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    try: 
        if isclose(array[idx], value, abs_tol=1):
            return idx
    except:
        pass
    return idx-1

#directory = r'F:\Data on BDATAPROD2\Anes Madani\Niagara\UEF_Niagara\Conversion_Result'
events_dir = r'C:\Niagara\UEF\Events'
channels_dir = r'C:\Niagara\UEF\Channels'
resultPath = r'C:\Niagara\Preprocessing_UEF'
events = ['Purge', 'Draw', 'Cut']
startings = ['Starting Purge', 'Starting Draw', 'Cut IN']
endings = ['Ending Purge', 'Draw Complete', 'Cut OUT']

for fileName in os.listdir(channels_dir):
    print('File name:', fileName)
    df = pd.read_csv(os.path.join(channels_dir, fileName))
    split = fileName.split(" ")
    
    #if (len(split)==5 and 'ICN' in split[1]) or (len(split)==6 and 'Setpoint' in split[-1]) or (len(split)==4 and len(split[1])>3):
    #    continue
    #else:
    
    try:
        df = df[['TimeStamp (sec)', 'Ambient TC', 'Gas TC', 'Barometer', 'Gas ascf', 'WattHrs', 
              'Water (Gallons)', 'Watts', 'Water Flow (GPM)', 'Tin', 'Tout', 'Tank Outlet', 'Purge Valve', 
              'Drain Valve', 'Water Mass(lbs)', 'Drawn Water (Gallons)']].copy()
    except:
        continue
        
    df = pp.preProcess(df, split)
    dfEvent = pd.read_csv(os.path.join(events_dir, fileName))
    #Create a new column for each event with the number of the event
    for event, starting, ending in zip(events, startings, endings):
        df[event]=0
        #Indecies of event
        starting_indeces = dfEvent.loc[dfEvent['Desc'].str.contains(starting)]
        ending_indeces = dfEvent.loc[dfEvent['Desc'].str.contains(ending)]
        for i, j in zip(range(0, len(starting_indeces)), range(0, len(ending_indeces))):
            start_event_time = starting_indeces.iloc[i][1]
            end_event_time = ending_indeces.iloc[j][1]
            start_idx = find_nearest(df['TimeStamp (sec)'].values, start_event_time)
            end_idx = find_nearest(df['TimeStamp (sec)'].values, end_event_time)
            df.loc[start_idx:end_idx, event]=str(i+1)
            
    #Create a 'Waiting For T' column
    df['Waiting for T']=0
    indeces = dfEvent.loc[dfEvent['Desc'].str.contains('Waiting for T')]
    for i in range(0, len(indeces)):
        time = indeces.iloc[i][1] 
        idx = find_nearest(df['TimeStamp (sec)'].values, time)
        df.loc[idx, 'Waiting for T']=str(i+1)
    
    df.to_csv(os.path.join(resultPath,fileName), index = False)
    print('\n\n\n\n')