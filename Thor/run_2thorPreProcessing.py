import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import ThorInfo as Info
import swifter

directory = r'C:\Thor\prp'
resultPath = r'C:\Thor\preprocessed'

delete = True

print('DATA PREPROCESSING STARTED')

temps = ['AMBIENTT', 'LOHTRTMP', 'UPHTRTMP', 'EVAPTEMP', 'SUCTIONT', 'DISCTEMP']

#Cleaning/debug function
def clean(df, delete=False):
    df.replace(r'^\s+$', np.nan, regex=True, inplace=True)
    df.dropna(thresh=5, inplace=True)
    for column in list(Info.columns.keys()):
        if column in temps and delete:
            df[column] = pd.to_numeric(df[column], errors='coerce').dropna()
            df.reset_index(drop=True, inplace=True)
            df.drop(np.where((df[column] == 9999999.0) | (df[column] == -40.0))[0], inplace=True)
            df.reset_index(drop=True, inplace=True)
        elif column not in temps:
            trash=[value for value in df[column].unique() if value not in Info.columns.get(column)]
            trash=[value for value in trash if str(value)!='nan']
            if len(trash)>0 and delete:
                print(column, trash)
                df.drop(np.where(df[column] == value for value in trash)[0], inplace=True)
                df.reset_index(drop=True, inplace=True)

l1 = dict()
l2 = dict()
for param in temps:
    l1[param] = []
    l2[param] = []

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))   
    print(fileName)
    df['WHTRMODE'] = df['WHTRMODE'].swifter.apply(lambda x: 'Energy Saver' if x=='Energy-Saver' else x)
    df['WHTRMODE'] = df['WHTRMODE'].swifter.apply(lambda x: 'Heat Pump' if x=='Heat-Pump' else x)
    print('Cleaning Start!')
    clean(df,delete)
    print('Cleaning Done!')
    
    if delete:
        for param in temps:
            l1[param].append(df[param].max())
            l2[param].append(df[param].min())
    
    df.to_csv(os.path.join(resultPath,fileName), index = False)
    print('\n\n\n')

if delete:
    for key in l1.keys():
        print('max:', max(l1[key]), 'min:', min(l2[key]))

print('DATA PREPROCESSING DONE')