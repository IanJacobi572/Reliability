import pandas as pd
import os


def preProcess(df, split):
    
    for index in range(0, len(split)):
        if 'ICN' in split[index]:
            df['Station'] = ' '.join(split[0:index])
        if 'ICN' in split[index] and len(split[index]) > 3:
            df['Unit Name'] = ' '.join(split[index])
        if 'ICN' in split[index] and len(split[index]) == 3:
            df['Unit Name'] = ' '.join(split[index:index+2])
    subsplit = split[-1:][0].split('.')[0].split('-')
    if len('-'.join(subsplit[:-1]))<6:
        df['Model'] = split[-2] + '-' + ''.join(subsplit[:-1])
    else: 
        df['Model'] = '-'.join(subsplit[:-1])
    df['Iteration'] = subsplit[-1]
    print('Station:', df.Station.unique())
    print('Unit Name:', df['Unit Name'].unique())
    print('Model:', df.Model.unique())
    print('Iteration:', df['Iteration'].unique())
            
    return df