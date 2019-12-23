import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import Gen5Info as Info
import swifter

directory = r'C:\gen5\prp'
resultPath = r'C:\gen5\preprocessed'

print('DATA PREPROCESSING STARTED')

temps = ['AMBIENTT', 'LOHTRTMP', 'UPHTRTMP', 'EVAPTEMP', 'SUCTIONT', 'DISCTEMP']

#Cleaning/debug function
def clean(df, delete=False):
    for column in list(Info.columns.keys()):
        if column in temps:
            df[column] = pd.to_numeric(df[column], errors='coerce').dropna()
            df.reset_index(drop=True, inplace=True)
            df.drop(np.where((df[column] == 9999999.0) | (df[column] == -40.0))[0])
        else:
            trash=[value for value in df[column].unique() if value not in Info.columns.get(column)]
            trash=[value for value in trash if str(value)!='nan']
            row = [[df[df[column]==value].index[0],df[df[column]==value].index[-1]] for value in trash]
            if len(trash)!=0 and not delete:
                print(column, 'trash values: ', trash, 'row indeces: ', row)
            if delete:
                for s in row:
                    df.drop(df.index[s[0]:s[1]], inplace=True)

l1 = dict()
l2 = dict()
for param in ['AMBIENTT', 'LOHTRTMP', 'UPHTRTMP', 'EVAPTEMP', 'SUCTIONT', 'DISCTEMP']:
    l1[param] = []
    l2[param] = []

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))   
    print(fileName)
    
    df['WHTRMODE'] = df['WHTRMODE'].swifter.apply(lambda x: 'Heat Pump' if x=='Heat-Pump' else x)
    print('Cleaning Start!')
    clean(df,True)
    print('Cleaning Done!')
    
    for param in ['AMBIENTT', 'LOHTRTMP', 'UPHTRTMP', 'EVAPTEMP', 'SUCTIONT', 'DISCTEMP']:
        l1[param].append(df[param].max())
        l2[param].append(df[param].min())
    
    df.to_csv(os.path.join(resultPath,fileName), index = False)
    print('\n\n\n')

for key in l1.keys():
    print('max:', max(l1[key]), 'min:', min(l2[key]))
print('DATA PREPROCESSING DONE')