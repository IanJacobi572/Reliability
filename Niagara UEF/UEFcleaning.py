import pandas as pd
import os

def clean(fileName, channels_dir):
    
    dfC = pd.read_csv(os.path.join(channels_dir, fileName))
    split = fileName.split(" ")
    
    dfC = dfC[['TimeStamp (sec)', 'Ambient TC', 'Gas TC', 'Barometer', 'Gas ascf', 'WattHrs', 
          'Water (Gallons)', 'Watts', 'Water Flow (GPM)', 'Tin', 'Tout', 'Tank Outlet', 'Purge Valve', 
          'Drain Valve', 'Drawn Water (Gallons)']].copy()

    
    for index in range(0, len(split)):
        if 'ICN' in split[index]:
            dfC['Station'] = ' '.join(split[0:index])
        if 'ICN' in split[index] and len(split[index]) > 3:
            name = ''.join(split[index])
            dfC['Unit Name'] = name[:3] + ' ' + name[3:]
        if 'ICN' in split[index] and len(split[index]) == 3:
            dfC['Unit Name'] = ' '.join(split[index:index+2])
    subsplit = split[-1:][0].split('.')[0].split('-')
    if len('-'.join(subsplit[:-1]))<6:
        dfC['Model'] = split[-2] + '-' + ''.join(subsplit[:-1])
    else: 
        dfC['Model'] = '-'.join(subsplit[:-1])
    dfC['Iteration'] = subsplit[-1]
    
    dfC['TimeStamp (hrs)'] = dfC['TimeStamp (sec)']/3600
            
    return dfC