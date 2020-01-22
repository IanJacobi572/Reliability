import numpy as np
import pandas as pd
from datetime import datetime
import os
from scipy.signal import argrelextrema
#import OdinFieldInfo as Info
from datetime import datetime
#from scipy.signal import argrelextrema

directory = r'C:\Users\anes.madani\Desktop\Anes\Odin Field\preprocessed'
resultPath = r'C:\Users\anes.madani\Desktop\Anes\Odin Field\processed'

print('DATA PROCESS STARTED')

'''{
"mac_address": "80-91-33-8A-DC-69",
"lat": 29.9064813,
"long": -81.3405168,
"user": "noremorse@ruccinet.com"
},
{
"mac_address": "DC-F5-05-D4-22-0B",
"lat": 84.9999755,
"long": -135.000628,
"user": "santa.claus@gmail.com"
},
{
"mac_address": "80-91-33-8A-A9-11",
"lat": 32.3904547,
"long": -86.2760567,
"user": "brandon_testing@rheem.com"
},

{
"mac_address": "80-91-33-8A-88-59",
"lat": 32.3904547,
"long": -86.2760567,
"user": "david.i.vega@rheem.com"
},
{
"mac_address": "80-91-33-8A-96-4F",
"lat": 84.9999755,
"long": -135.000628,
"user": "santa.claus@gmail.com"
},'''

longitude = {
    'DC-67': -82.7436426,
    '80-A6': -82.0319862,
    '6D-A6': -84.3180902,
    'AC-8D': -84.1851038,
    '71-8A': -86.2760567,
    '6D-92': -112.3766632,
    '6D-98': -120.7048673,
    '6D-B0': -81.3874635,
    '75-2E': -112.8398411,
    '75-31': -81.4670145,
    '75-4D': -81.7434531,
    '84-91': -112.8398411,
    '80-9F': -112.1062192,
    '80-98': -135.000628,
    '80-99': -111.7602131,
    '80-B2': -112.4227968,
    '88-39': -81.4078258,
    '8C-28': -83.7499943,
    '88-45': -121.3591972,
    'A5-BB': -122.6604498,
    'A6-01': -122.3533578,
    'AC-71': -81.454795,
    'CA-66': -81.0979757,
    'FD-9D': -86.2760567,
    'DC-64': 72.5138113,
    '8C-31': -84.3180902,
    'AC-7D': -81.4387894
    }
    
lattitude = {
    'DC-67': 39.4697139,
    '80-A6': 28.9227819,
    '6D-A6': 34.0650491,
    'AC-8D': 33.9786427,
    '71-8A': 32.3904547,
    '6D-92': 33.6029836, 
    '6D-98': 40.4093139,
    '6D-B0': 28.325943,
    '75-2E': 33.2497937,
    '75-31': 28.7320841,
    '75-4D': 30.4839112,
    '84-91': 33.2497937,
    '80-9F': 33.6310652,
    '80-98': 84.9999755,
    '80-99': 33.6763818,
    '80-B2': 33.606364,
    '88-39': 28.4449206,
    '8C-28': 33.7981525,
    '88-45': 38.6249298,
    'A5-BB': 38.2519662,
    'A6-01': 45.2984874,
    'AC-71': 28.6254478,
    'CA-66': 29.0998953,
    'FD-9D': 32.3904547,
    'DC-64': 23.017738,
    '8C-31': 34.0650491,
    'AC-7D': 28.481151
    }

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))
    
    print(fileName)
    
    df['UnitName']=fileName[12:17]
    
    df['Longitude']=longitude[fileName[12:17]]
    df['Lattitude']=lattitude[fileName[12:17]]
        
    print('Sorting Start')
    df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True)
    df.sort_values(by=['timestamp'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    #df['Date'] = df['timestamp'].dt.date    
    print('Sorting Done')
    
    day0 = pd.Series(pd.to_datetime(df.loc[0, 'timestamp'])).dt.dayofyear[0]
    df['Day'] = df['timestamp'].dt.dayofyear-day0+1
    
    df['deltaT'] = df['timestamp'].groupby(df['Day']).diff().dt.total_seconds()
    df['deltaT'].fillna(0, inplace=True)
    
    df['Compressor Running Time (sec)'] = np.where(df['COMP_RLY']==1.0, df['deltaT'],0)
    df['Compressor Running Time (hrs)'] = df['Compressor Running Time (sec)']/3600

    df['Compressor Non Running Time (sec)'] = np.where(df['COMP_RLY']==0.0, df['deltaT'],0)
    df['Compressor Non Running Time (hrs)'] = df['Compressor Non Running Time (sec)']/3600

    df['Compressor Not Recording Time (sec)'] = np.where((df['COMP_RLY']!=1.0) & (df['COMP_RLY']!=0.0), df['deltaT'],0)
    df['Compressor Not Recording Time (hrs)'] = df['Compressor Not Recording Time (sec)']/3600
    
    df['Upper Element Running Time (sec)'] = np.where(df['HEATCTRL']==2, df['deltaT'],0)
    df['Upper Element On (hrs)'] = df['Upper Element Running Time (sec)']/3600
    #df['Upper Element On/Day'] = df['Upper Element On (hrs)'].groupby(df['Day']).transform('sum')

    df['Elements Off Time (sec)'] = np.where(df['HEATCTRL']==0, df['deltaT'],0)
    df['Elements Off (hrs)'] = df['Elements Off Time (sec)']/3600
    #df['Elements Off/Day'] = df['Elements Off (hrs)'].groupby(df['Day']).transform('sum')

    df['Elements Not Recording Time (sec)'] = np.where(df['HEATCTRL']==None, df['deltaT'],0)
    df['Elements Not Recording (hrs)'] = df['Elements Not Recording Time (sec)']/3600
    #df['Elements Not Recording/Day'] = df['Elements Not Recording (hrs)'].groupby(df['Day']).transform('sum')
    
    df['Upper Element On Progress (hrs)'] = df['Upper Element On (hrs)'].cumsum()
    df['Element Off Progress (hrs)'] = df['Elements Off (hrs)'].cumsum()
    df['Elements Not Recording Progress(hrs)'] = df['Elements Not Recording (hrs)'].cumsum()
    df['Elements Cycle'] = np.where((df['HEATCTRL']==2) & ((df['HEATCTRL'].shift()==1) | (df['HEATCTRL'].shift()==0)), 1,0)
    
    #df['Completed Elements (hrs)']=df['Upper Element On (hrs)'].sum()
    

    
    #df['Compressor On/Day'] = df['Compressor Running Time (hrs)'].groupby(df['Day']).transform('sum')
    #df['Compressor ---/Day'] = 0
    #df['Compressor ---/Day'] = df['Compressor Not Recording Time (hrs)'].groupby(df['Day']).transform('sum')
    df['Target (hrs)/row'] = df['deltaT']/3600
    df['Recorded Time'] = df['Target (hrs)/row'].groupby(df['Day']).transform('sum')
    df['DownTime/Day'] =24-df['Recorded Time']
    #df['No Data (hrs)'] = df['DownTime/Day']+df['Compressor ---/Day']
    #df['Completed (hrs)']=df['Compressor Running Time (hrs)'].sum()
    
    #print(df['Elements Cycle'].unique())
    
    df.drop(['deltaT', 'Day'], axis=1, inplace=True)
   
    df.to_csv(os.path.join(resultPath,fileName), index = False)    
    
    print('\n-------------------------------------------------------------------------------------------------------------------\n')
        
        
print('DATA PROCESS DONE!')
#Note to self: Maybe need to optimize the code but it works just fine (for now)