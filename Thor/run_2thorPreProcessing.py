import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import ThorInfo as Info
import swifter

directory = r'C:\Thor\prp'
resultPath = r'C:\Thor\preprocessed'

print('DATA PREPROCESSING STARTED')

#Cleaning/debug function
def clean(df, delete):
    for column in list(Info.columns.keys()):
        trash=[value for value in df[column].unique() if value not in Info.columns.get(column)]
        trash=[value for value in trash if str(value)!='nan']
        row = [[df[df[column]==value].index[0],df[df[column]==value].index[-1]] for value in trash]
        if len(trash)!=0 and not delete:
            print(column, 'trash values: ', trash, 'row indeces: ', row)
        if delete:
            for s in row:
                df.drop(df.index[s[0]:s[1]], inplace=True)

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))   
    print(fileName)
    
    #if 'C3' in fileName or 'C4' in fileName or 'F11' in fileName:
    #    df.dropna(subset=['WHTRMODE'], inplace=True)
    #    clean(df,True)
    
    df['WHTRMODE'] = df['WHTRMODE'].swifter.apply(lambda x: 'Heat Pump' if x=='Heat-Pump' else x)
    
    df.to_csv(os.path.join(resultPath,fileName), index = False)
    print('\n\n\n')
    
print('DATA PREPROCESSING DONE')