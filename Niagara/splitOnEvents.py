import pandas as pd
import os
import numpy as np
from math import isclose
import re

def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if isclose(array[idx], value, abs_tol=1):
        return idx
    else:
        return idx-1
directory = r'F:\Data on BDATAPROD2\Anes Madani\Niagara\UEF_Niagara\Conversion_Result'
resultPath = r'C:\Niagara\Preprocessing_UEF'
event_names = ['Ending Purge', 'Cut OUT', 'Cut IN', 'Waiting for T', 'Starting Purge', 'Starting Draw', 'Draw Complete']
for filename in os.listdir(directory):
    if not filename.startswith("E"):
        #Load Channels and Events datasets
        df = pd.read_csv(os.path.join(directory,filename))
        dfEvent = pd.read_csv(os.path.join(directory,'E_'+filename))
        
        #Create a new column that contains the Draw Number
        df['Draw Number']=0
        df['Desc'] = ''
        start_idxs = []
        for event in event_names:
            specific_events = dfEvent.loc[dfEvent['Desc'].str.contains(event)]
            for i in range(0, len(specific_events)):
                event_time = specific_events.iloc[i][1]
                idx = find_nearest(df['TimeStamp (sec)'].values, event_time)
                if(event == 'Starting Draw'):
                    df.loc[idx, 'Desc'] = 'Starting Draw # ' + str(i+1)
                    start_idxs.append(idx)
                elif(event == 'Draw Complete'):
                    df.loc[idx, 'Desc'] = event
                    print(start_idxs)
                    print(idx)
                    df.loc[start_idxs[i]:idx, 'Draw Number'] = i+1
                else:
                    df.loc[idx, 'Desc'] = event

        df.to_csv(os.path.join(resultPath,filename), index = False)
       
    else:
        continue
#Maybe need to start TimpeStamps from 0 for each or not
#Note to self: Maybe need to optimize the code but it works just fine (for now)