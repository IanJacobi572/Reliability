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

missingHours = {
    'C03': 168.25,
    'C04': 431,
    'C05': 498.5,
    'C06': 498.5,
    'C09': 248,
    'C10': 515,
    'C11': 124.84,

    'D01': 146,
    'D02': 149,
    'D03': 151,
    'D04': 143,
    'D05': 150,
    'D06': 150,
    'D07': 156,
    'D08': 150,

    'F01': 85,
    'F02': 79.3,
    'F03': 61.8,
    'F05': 62.4,
    'F06': 68,
    'F07': 139.5,
    'F08': 78.37,
    'F10': 74.2,
    'F11': 140.3
}

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
    df['Gallon Type'] = key.getBaseModel()[2:4]
    
    #Add Cycling Option that has 3 different types
    #if key.getCycles()==78.5:
    #    df['Cycling Option']='3 (78.5 Cycles/Day)'
    #elif key.getCycles()==76.5:
    #    df['Cycling Option']='2 (76.5 Cycles/Day)'
    #elif key.getCycles()==80:
    #    df['Cycling Option']='1 (80 Cycles/Day)'
        
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
    
    df['Upper Element Running Time (sec)'] = np.where(df['HEATCTRL']=='Upper Element', df['deltaT'],0)
    df['Upper Element On (hrs)'] = df['Upper Element Running Time (sec)']/3600
    #df['Upper Element On/Day'] = df['Upper Element On (hrs)'].groupby(df['Day']).transform('sum')

    df['Lower Element Running Time (sec)'] = np.where(df['HEATCTRL']=='Lower Element', df['deltaT'],0)
    df['Lower Element On (hrs)'] = df['Lower Element Running Time (sec)']/3600
    #df['Lower Element On/Day'] = df['Lower Element On (hrs)'].groupby(df['Day']).transform('sum')

    df['Elements Off Time (sec)'] = np.where(df['HEATCTRL']=='Off', df['deltaT'],0)
    df['Elements Off (hrs)'] = df['Elements Off Time (sec)']/3600
    #df['Elements Off/Day'] = df['Elements Off (hrs)'].groupby(df['Day']).transform('sum')

    df['Elements Not Recording Time (sec)'] = np.where(df['HEATCTRL']==None, df['deltaT'],0)
    df['Elements Not Recording (hrs)'] = df['Elements Not Recording Time (sec)']/3600
    #df['Elements Not Recording/Day'] = df['Elements Not Recording (hrs)'].groupby(df['Day']).transform('sum')
    
    df['Upper Element On Progress (hrs)'] = df['Upper Element On (hrs)'].cumsum()
    df['Lower Element On Progress (hrs)'] = df['Lower Element On (hrs)'].cumsum()
    df['Element Off Progress (hrs)'] = df['Elements Off (hrs)'].cumsum()
    df['Elements Not Recording Progress(hrs)'] = df['Elements Not Recording (hrs)'].cumsum()
    
    df['Completed Elements (hrs)']=df['Upper Element On (hrs)'].sum() + df['Lower Element On (hrs)'].sum()
    
    target = 3338

    df['Compressor On/Day'] = 7
    df['Compressor On/Day'].iloc[change_index:] = df['Compressor Running Time (hrs)'].iloc[change_index:].groupby(df['Day'].iloc[change_index:]).transform('sum')

    #df['Compressor Off/Day'] = 0
    #df['Compressor Off/Day'].iloc[change_index:] = df['Compressor Non Running Time (hrs)'].iloc[change_index:].groupby(df['Day'].iloc[change_index:]).transform('sum')

    df['Compressor ---/Day'] = 0
    df['Compressor ---/Day'].iloc[change_index:] = df['Compressor Not Recording Time (hrs)'].iloc[change_index:].groupby(df['Day'].iloc[change_index:]).transform('sum')

    df['Target CRT/Day'] = 7
    df['Target CRT/Day'].iloc[change_index:] = 24

    df['Target (hrs)/row'] = df['deltaT']/3600
    df['Recorded Time'] = df['Target (hrs)/row'].groupby(df['Day']).transform('sum')
    df['DownTime/Day'] = 24-df['Recorded Time']
    df['No Data (hrs)'] = df['DownTime/Day']+df['Compressor ---/Day']

    df['Completed (hrs)']=df['Compressor Running Time (hrs)'].iloc[change_index:].sum() + old_days*7
    df['Completed (hrs)']= df['Completed (hrs)']+missingHours.get(key.getStation())
    df['Not Completed (hrs)']=target-df['Completed (hrs)']

    #df['Target (hrs)']=df['Target (hrs)/row'].iloc[change_index:].sum() + old_days*7

    df['Progress/Day'] = df['Compressor On/Day']/df['Target CRT/Day']
    df['Progress'] = df['Completed (hrs)']/target
    
    #df['Target'] = target
    days_left = df.loc[0, 'Not Completed (hrs)']/24
    last_date = df['Date'].iloc[-1]
    target_date = last_date + pd.DateOffset(days=days_left)
    df['Target Date'] = target_date.to_pydatetime().date()
    df['Years Reached'] = df.loc[0, 'Completed (hrs)']*12/target
    
    df['ALARM CODE'] = np.where(df['ALARM_01'].str[0]=='A', df['ALARM_01'].str[:4], None)
    df['ALARM DESC'] = np.where(df['ALARM_01'].str[0]=='A', df['ALARM_01'].str[5:], None)
    df['ALERT CODE'] = np.where(df['ALARM_01'].str[0]=='T', df['ALARM_01'].str[:4], None)
    df['ALERT DESC'] = np.where(df['ALARM_01'].str[0]=='T', df['ALARM_01'].str[5:], None)
    
    df['UPHTRTMP'] = df['UPHTRTMP'].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
    df['Element Fail'] = np.where(((df['COMP_RLY']=='On') 
                               & (df['HEATCTRL']=='Upper Element') 
                               & (df['UPHTRTMP']<120)), 'Element failure at '+ str(df['Date/Time']), False)
    
    df.drop(['Time', 'Target CRT/Day', 'deltaT', 'Day', 'Station'], axis=1, inplace=True)
   
    df.to_csv(os.path.join(resultPath,fileName), index = False)    
    
    print('\n-------------------------------------------------------------------------------------------------------------------\n')
        
        
print('DATA PROCESS DONE!')
#Note to self: Maybe need to optimize the code but it works just fine (for now)