import numpy as np
import pandas as pd
from datetime import datetime
import os
from scipy.signal import argrelextrema
import Gen5Info as Info
from datetime import datetime
#from scipy.signal import argrelextrema

directory = r'C:\gen5\preprocessed'
resultPath = r'C:\gen5\processed'

print('DATA PROCESS STARTED')

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))
    
    print(fileName)
    
    #Every cycle should take getCycles() and timestamp between each row of data is 30sec 
    #so getCycles()/30=X records hence X rows per cycle
    key = df.loc[1, 'Station']
    key = Info.info.get(key)
    
    #Combine Station and UnitName columns in a new column
    df['Station/UnitName']=key.getStation() + '/' + key.getIcn()
    #Addd Heater Base Model column
    df['Heater Base Model']=key.getBaseModel()
    
    #Add Cycling Option that has 3 different types
    if key.getCycles()==78.5:
        df['Cycling Option']='3 (78.5 Cycles/Day)'
    elif key.getCycles()==76.5:
        df['Cycling Option']='2 (76.5 Cycles/Day)'
    elif key.getCycles()==80:
        df['Cycling Option']='1 (80 Cycles/Day)'
        
    print('\nSorting by date/time')
    #Sort by date then by time
    df['Comb'] = df['Date'] + ' ' + df['Time']
    df['Comb'] = pd.to_datetime(df['Comb'], infer_datetime_format=True)
    df['Time'] = pd.to_datetime(df.Time, infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df.Date, infer_datetime_format=True)
    if len(df['Date'].unique())>0:
        df.sort_values(by=['Date', 'Time'], inplace=True)
    else:
        df.sort_values(by=['Time'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    print('Sort by date/time complete!')
    
    df['Start Date'] = key.getTeamStartDate()
    df['Switch Start Date'] = key.getChangedDate()

    actual_start_date = datetime.strptime(key.getTeamStartDate(), '%Y-%m-%d')
    NL_start_date = datetime.strptime(key.getStartDate(), '%Y-%m-%d')
    changed_start_date = datetime.strptime(key.getChangedDate(), '%Y-%m-%d')
    delta_days = (NL_start_date - actual_start_date).days
    old_days = (changed_start_date - actual_start_date).days
    delta_weeks = int(delta_days/7)
        
    change_index = df.index[df['Date'].dt.date == changed_start_date.date()][0]
        
    day0 = pd.Series(pd.to_datetime(df.loc[0, 'Date'])).dt.dayofyear[0]
    df['Day'] = df['Date'].dt.dayofyear-day0+delta_days+1

    week0 = pd.Series(pd.to_datetime(df.loc[0, 'Date'])).dt.weekofyear[0]
    df['Week'] = df['Date'].dt.weekofyear-week0+delta_weeks+1
    
    #df['deltaT'] = df['Comb'].diff().dt.total_seconds()
    df['deltaT'] = df['Comb'].groupby(df['Day']).diff().dt.total_seconds()
    df['deltaT'].fillna(0, inplace=True)

    df['Time'] = df['Time'].dt.time
    df['Date'] = df['Date'].dt.date
    
    df['Compressor Running Time (sec)'] = np.where(df['COMP_RLY']=='On', df['deltaT'],0)
    df['Compressor Non Running Time (sec)'] = np.where(df['COMP_RLY']=='Off', df['deltaT'],0)
    df['Compressor Running Time (hrs)'] = df['Compressor Running Time (sec)']/3600
    df['Compressor Non Running Time (hrs)'] = df['Compressor Non Running Time (sec)']/3600
    
    target = 3338
    df['Target (hrs)/row'] = df['deltaT']/3600
    df['Compressor On/Day'] = 7
    df['Target CRT/Day'] = 7
    df['Compressor Off/Day'] = 0
    df['Compressor On/Day'].iloc[change_index:] = df['Compressor Running Time (hrs)'].iloc[change_index:].groupby(df['Day'].iloc[change_index:]).transform('sum')
    df['Compressor Off/Day'].iloc[change_index:] = df['Compressor Non Running Time (hrs)'].iloc[change_index:].groupby(df['Day'].iloc[change_index:]).transform('sum')
    df['Recorded CRT/Day'] = df['Target (hrs)/row'].groupby(df['Day']).transform('sum')
    df['Target CRT/Day'].iloc[change_index:] = 24
    df['Progress/Day'] = df['Compressor On/Day']/df['Target CRT/Day']
    df['Completed (hrs)']=df['Compressor Running Time (hrs)'].iloc[change_index:].sum() + old_days*7
    df['Not Completed (hrs)']=target-df['Completed (hrs)']
    df['Target (hrs)']=df['Target (hrs)/row'].iloc[change_index:].sum() + old_days*7
    df['Progress'] = df['Completed (hrs)']/target
    
    df['Target'] = target
    days_left = df.loc[0, 'Not Completed (hrs)']/24
    last_date = df['Date'].iloc[-1]
    target_date = last_date + pd.DateOffset(days=days_left)
    df['Target Date'] = target_date.to_pydatetime().date()
    df['Years Reached'] = df.loc[0, 'Completed (hrs)']*12/target
    
    df.drop(['Target (hrs)/row', 'Comb'], axis=1, inplace=True)
   
    df.to_csv(os.path.join(resultPath,fileName), index = False)    
    
    print('\n-------------------------------------------------------------------------------------------------------------------\n')
        
        
print('DATA PROCESS DONE!')
#Note to self: Maybe need to optimize the code but it works just fine (for now)