import numpy as np
import pandas as pd
from datetime import datetime
import os
from scipy.signal import argrelextrema
import ThorInfo as Info
from datetime import datetime
#from scipy.signal import argrelextrema

directory = r'C:\Thor\preprocessed'
resultPath = r'C:\Thor\processed'

print('DATA PROCESS STARTED')


for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))
    
    print(fileName)
    
    #Every cycle should take getCycles() and timestamp between each row of data is 30sec 
    #so getCycles()/30=X records hence X rows per cycle
    key = df.loc[1, 'Station']
    key = Info.info.get(key)
    
    #Date/Timeine Station and UnitName columns in a new column
    df['Station/UnitName']=key.getStation() + '/' + key.getIcn()
    #Addd Heater Base Model column
    df['Gallon Type'] = key.getBaseModel()
    
    print('\nSorting by date/time')
    #Sort by date then by time
    df['Date/Time'] = df['Date'] + ' ' + df['Time']
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], infer_datetime_format=True)
    df.sort_values(by=['Date/Time'], inplace=True)
    df['Time'] = pd.to_datetime(df.Time, infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df.Date, infer_datetime_format=True)
    #if len(df['Date'].unique())>0:
    #    df.sort_values(by=['Date', 'Time'], inplace=True)
    #else:
    #    df.sort_values(by=['Time'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    print('Sort by date/time complete!')
    
    df['Start Date'] = df['Date'].dt.date.iloc[0]
        
    day0 = pd.Series(pd.to_datetime(df.loc[0, 'Date'])).dt.dayofyear[0]
    df['Day'] = df['Date'].dt.dayofyear-day0+1
    
    #df['deltaT'] = df['Date/Time'].diff().dt.total_seconds()
    df['deltaT'] = df['Date/Time'].groupby(df['Day']).diff().dt.total_seconds()
    df['deltaT'].fillna(0, inplace=True)

    #df['Time'] = df['Time'].dt.time
    df['Date'] = df['Date'].dt.date
    
    df['Compressor Running Time (sec)'] = np.where(df['COMP_RLY']=='On', df['deltaT'],0)
    df['Compressor Running Time (hrs)'] = df['Compressor Running Time (sec)']/3600

    df['Compressor Non Running Time (sec)'] = np.where(df['COMP_RLY']=='Off', df['deltaT'],0)
    df['Compressor Non Running Time (hrs)'] = df['Compressor Non Running Time (sec)']/3600

    df['Compressor Not Recording Time (sec)'] = np.where(df['COMP_RLY']=='---', df['deltaT'],0)
    df['Compressor Not Recording Time (hrs)'] = df['Compressor Not Recording Time (sec)']/3600
    
    target = 2275.90

    df['Compressor On/Day'] = df['Compressor Running Time (hrs)'].groupby(df['Day']).transform('sum')

    #df['Compressor Off/Day'] = 0
    #df['Compressor Off/Day'] = df['Compressor Non Running Time (hrs)'].groupby(df['Day']).transform('sum')

    df['Compressor ---/Day'] = 0
    df['Compressor ---/Day'] = df['Compressor Not Recording Time (hrs)'].groupby(df['Day']).transform('sum')

    dayTarget = 16.3636
    df['Target (hrs)/row'] = df['deltaT']/3600
    df['Recorded Time'] = df['Target (hrs)/row'].groupby(df['Day']).transform('sum')
    df['DownTime/Day'] =24-df['Recorded Time']
    df['No Data (hrs)'] = df['DownTime/Day']+df['Compressor ---/Day']
    df['Completed (hrs)']=df['Compressor Running Time (hrs)'].sum()
    df['Not Completed (hrs)']=target-df['Completed (hrs)']

    #df['Target (hrs)']=df['Target (hrs)/row'].sum()

    df['Progress/Day'] = df['Compressor On/Day']/16.3636
    df['Progress'] = df['Completed (hrs)']/target
    
    #df['Target'] = target
    days_left = df.loc[0, 'Not Completed (hrs)']/dayTarget
    last_date = df['Date'].iloc[-1]
    target_date = last_date + pd.DateOffset(days=days_left)
    df['Target Date'] = target_date.to_pydatetime().date()
    df['Years Reached'] = df.loc[0, 'Completed (hrs)']*12/target
    
    #df['ALARM CODE'] = np.where(df['ALARMS'].str[0]=='A', df['ALARMS'].str[:4], None)
    #df['ALARM DESC'] = np.where(df['ALARMS'].str[0]=='A', df['ALARMS'].str[5:], None)
    #df['ALERT CODE'] = np.where(df['ALARMS'].str[0]=='T', df['ALARMS'].str[:4], None)
    #df['ALERT DESC'] = np.where(df['ALARMS'].str[0]=='T', df['ALARMS'].str[5:], None)
    
    df.drop(['Time', 'deltaT'], axis=1, inplace=True)
   
    df.to_csv(os.path.join(resultPath,fileName), index = False)    
    
    print('\n-------------------------------------------------------------------------------------------------------------------\n')
        
        
print('DATA PROCESS DONE!')
#Note to self: Maybe need to optimize the code but it works just fine (for now)