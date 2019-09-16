import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import Gen5Info as Info

directory = r'C:\gen5\prp'
resultPath = r'C:\gen5\withCycles'

for fileName in os.listdir(directory):

    #Load dataset
    df = pd.read_csv(os.path.join(directory,fileName))   
    print(fileName)
    
    #Find the local minimas
    #Every cycle should take getCycles() and timestamp between each row of data is 30sec 
    #so getCycles()/30=X records hence X rows per cycle
    key = df.loc[1, 'Station']
    key = Info.info.get(key)
    n = int(key.getCycles()*0.8) #since we're supposed to have a local min in each X rows, we use 80% to be safe from noise
    try:
        df['min'] = df.iloc[argrelextrema(df.LOHTRTMP.values, np.less_equal, order=n)[0]]['LOHTRTMP']
    except:
        continue


    #Find the local minimas
    #Every cycle should take 2hrs and timestamp between each row of data is 30sec 
    #so 7200/30=240records hence 240rows per cycle
    #n=200 #since we're supposed to have a local min in each 240, we use 200 to be safe from noise
    #df['min'] = df.iloc[argrelextrema(df.LOHTRTMP.values, np.less_equal, order=n)[0]]['LOHTRTMP']
    #df['max'] = df.iloc[argrelextrema(df.LOHTRTMP.values, np.greater_equal, order=n)[0]]['LOHTRTMP']

    #Visualization
    '''plt.scatter(df.index, df['min'], c='r')
    #plt.scatter(df.index, df['max'], c='g')
    plt.plot(df.index, df['LOHTRTMP'])
    plt.show()'''

    #Assign the cycle number if in cycle otherwise 0
    count=1
    df['Cycle Number']=0
    for i in range(df.shape[0]):
        if np.isnan(float(df.loc[i, 'min'])):
            df.loc[i, 'min'] = 0
        if i>0 and df.loc[i-1,'min']!=0 and df.loc[i,'min']!=0:
            df.loc[i,'min'] = 0
        #BUG: some values are string instead of float which causes an error, need cleaning
        try:
            if df.loc[i, 'LOHTRTMP']>df.loc[i, 'min']:
                df.loc[i, 'Cycle Number']=count
                if i>1 and df.loc[i-1,'Cycle Number']==0:
                    count+=1
        except:
            continue
    noCycles=max(df['Cycle Number'].unique())
    #print(noCycles)
    
    df.to_csv(os.path.join(resultPath,fileName), index = False)    
        
#Note to self: Maybe need to optimize the code but it works just fine (for now)