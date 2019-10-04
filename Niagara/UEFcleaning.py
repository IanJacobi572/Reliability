import pandas as pd
import os

def clean(fileName, channels_dir):
    
    dfC = pd.read_csv(os.path.join(channels_dir, fileName))
    split = fileName.split(" ")
    
    
    if 'Water Mass(lbs)' in dfC.columns:
        dfC = dfC[['TimeStamp (sec)', 'Ambient TC', 'Gas TC', 'Barometer', 'Gas ascf', 'WattHrs', 
                  'Water (Gallons)', 'Watts', 'Water Flow (GPM)', 'Tin', 'Tout', 'Tank Outlet', 'Purge Valve', 
                  'Drain Valve', 'Water Mass(lbs)', 'Drawn Water (Gallons)']].copy()
    else:
        dfC = dfC[['TimeStamp (sec)', 'Ambient TC', 'Gas TC', 'Barometer', 'Gas ascf', 'WattHrs', 
              'Water (Gallons)', 'Watts', 'Water Flow (GPM)', 'Tin', 'Tout', 'Tank Outlet', 'Purge Valve', 
              'Drain Valve', 'Drawn Water (Gallons)']].copy()

    
    for index in range(0, len(split)):
        if 'ICN' in split[index]:
            dfC['Station'] = ' '.join(split[0:index])
        if 'ICN' in split[index] and len(split[index]) > 3:
            dfC['Unit Name'] = ' '.join(split[index])
        if 'ICN' in split[index] and len(split[index]) == 3:
            dfC['Unit Name'] = ' '.join(split[index:index+2])
    subsplit = split[-1:][0].split('.')[0].split('-')
    if len('-'.join(subsplit[:-1]))<6:
        dfC['Model'] = split[-2] + '-' + ''.join(subsplit[:-1])
    else: 
        dfC['Model'] = '-'.join(subsplit[:-1])
    dfC['Iteration'] = subsplit[-1]
    #print('Station:', dfC.Station.unique())
    #print('Unit Name:', dfC['Unit Name'].unique())
    #print('Model:', dfC.Model.unique())
    #print('Iteration:', dfC['Iteration'].unique())
            
    return dfC