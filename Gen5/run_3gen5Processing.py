import numpy as np
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import Gen5Info as Info

directory = r'C:\gen5\preprocessed'
resultPath = r'C:\gen5\processed'

print('DATA PROCESS STARTING')

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))   
    
    if 'F11' in fileName:
        continue
    
    print(fileName)
    
    #Every cycle should take getCycles() and timestamp between each row of data is 30sec 
    #so getCycles()/30=X records hence X rows per cycle
    key = df.loc[1, 'Station']
    key = Info.info.get(key)
    
    #TEMPORARY: Since the actual cycles were counted manually so we add a temporary column that will contain the actual cycles per row instead of hardcoded
    if key.getStation()=='C3':
        df['Actual Cycles']=1662
    elif key.getStation()=='C4':
        df['Actual Cycles']=1715
    elif key.getStation()=='C5':
        df['Actual Cycles']=1717
    elif key.getStation()=='C6':
        df['Actual Cycles']=1715
    elif key.getStation()=='C9':
        df['Actual Cycles']=1541
    elif key.getStation()=='C10':
        df['Actual Cycles']=1702
    elif key.getStation()=='C11':
        df['Actual Cycles']=1562
    elif key.getStation()=='F1':
        df['Actual Cycles']=591
    elif key.getStation()=='F2':
        df['Actual Cycles']=591
    elif key.getStation()=='F3':
        df['Actual Cycles']=582
    elif key.getStation()=='F5':
        df['Actual Cycles']=445
    elif key.getStation()=='F6':
        df['Actual Cycles']=498
    elif key.getStation()=='F7':
        df['Actual Cycles']=591
    elif key.getStation()=='F8':
        df['Actual Cycles']=579
    elif key.getStation()=='F10':
        df['Actual Cycles']=578  
    elif key.getStation()=='F11':
        df['Actual Cycles']=None    
    
    #Combine Station and UnitName columns in a new column
    df['Station/UnitName']=key.getStation() + '/' + key.getIcn()
    #Addd Heater Base Model column
    df['Heater Base Model']=key.getBaseModel()
    #Add Operational Mode column
    df['Operational Mode']=key.getOperationalMode()
    #Add Cycles Target per time column
    df['Target Cycles/Day']=key.getCycles()
    df['Target Cycles/180 Days']=key.getCycles()*180
    
    #Add Cycling Option that has 3 different types
    if key.getCycles()==21:
        df['Cycling Option']='3 (21 Cycles/Day)'
    elif key.getCycles()==12:
        df['Cycling Option']='2 (12 Cycles/Day)'
    elif key.getCycles()==144:
        df['Cycling Option']='1 (144 Cycles/Day)'
        
    print('\nSorting by date')
    #Convert Date to datetime and sort by date
    df['Date'] = pd.to_datetime(df.Date)
    df.sort_values('Date', inplace=True)
    print('Sort by date complete!')
    
    firstWeek=pd.to_datetime(key.getStartDate()).isocalendar()[1]
    #print('Start Date week: ', firstWeek)
    firstWeekRecorded=df['Date'].iloc[0].isocalendar()[1]
    #print('First week recorded: ', firstWeekRecorded-firstWeek+1)
    lastWeek=df['Date'].iloc[-1].isocalendar()[1]
    #print('Last week: ', lastWeek)
    #print('Last week recorded: ', lastWeek-firstWeek+1)
    
    #Consider the first recorded date as start date if start date is after first recorded date
    #if firstWeekRecorded<firstWeek:
    #    firstWeek=firstWeekRecorded        
    
    df.loc[0, 'Start Week']=firstWeek
    df.loc[0, 'Start Date']=key.getStartDate()
    
    numberOfWeeks=lastWeek-firstWeek+1
    numberOfCycles=df['Actual Cycles'].iloc[0]
    numberOfCyclesperDay=key.getCycles()
    #Get the week number for each row and cycles per week
    print('\nCalculating weeks')
    temp=-99
    for index, row in df.iterrows():
        currentWeek=row['Date'].isocalendar()[1] - firstWeek + 1
        if temp!=currentWeek:
        #if temp!=currentWeek and currentWeek>=0:
            temp=currentWeek
            print('week:', temp, 'from', lastWeek-firstWeek+1)
            df.loc[index, 'Week']=currentWeek
            df.loc[index, 'Actual Cycles/Week']=(numberOfCycles/numberOfWeeks)*currentWeek
            df.loc[index, 'Target Cycles/Week']=numberOfCyclesperDay*currentWeek*7 #number of cycles per day * week number * 7 days
        else:
            pass
    print('Weeks calculation complete!')
    
    
    
    n = int(key.getCycles()*0.8) #since we're supposed to have a local min in each X rows, we use 80% to be safe from noise
    
    #Get the local minimas of the appropriate parameter (LOW or UP HEATER TEMPERATURE)
    if max(df['LOHTRTMP'])-min(df['LOHTRTMP']) > max(df['UPHTRTMP'])-min(df['UPHTRTMP']):
        df['min'] = df.iloc[argrelextrema(df.LOHTRTMP.values, np.less_equal, order=n)[0]]['LOHTRTMP']
    else:
        df['min'] = df.iloc[argrelextrema(df.UPHTRTMP.values, np.less_equal, order=n)[0]]['UPHTRTMP']
      
        
    #Difference between target and actual cycles
    df['Progress by cycle number']=df['Target Cycles/180 Days']-df['Actual Cycles']
    df['Progress by percentage']=df['Actual Cycles']*100/df['Target Cycles/180 Days']

    
    df.to_csv(os.path.join(resultPath,fileName), index = False)    
    
    print('\n-------------------------------------------------------------------------------------------------------------------\n')
        
        
print('DATA PROCESS DONE!')
#Note to self: Maybe need to optimize the code but it works just fine (for now)