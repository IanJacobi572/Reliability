import pandas as pd
import os
import numpy as np
from math import isclose
import re
import UEFcleaning as c
import UEFevents as e
import UEFeff as f
from multiprocessing import Pool

def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    try: 
        if isclose(array[idx], value, abs_tol=1):
            return idx
    except:
        pass
    return idx-1

events_dir = r'C:\Niagara\UEF\Events'
channels_dir = r'C:\Niagara\UEF\Channels'
variables_dir = r'C:\Niagara\UEF\Variables'
resultPath = r'C:\Niagara\Preprocessing_UEF'
#resultPath = r'C:\Niagara\Takashi_Preprocessing_UEF'
events = ['Purge', 'Draw', 'Cut']
startings = ['Starting Purge', 'Starting Draw', 'Cut IN']
endings = ['Ending Purge', 'Draw Complete', 'Cut OUT']
ICNs = [10289, 10493, 10494, 10636, 10638, 10637, 10792]

for fileName in os.listdir(channels_dir):
    print('File name:', fileName)
    
    for elm in ICNs:
        if str(elm) in fileName:
            #Skip files with a lot of missing data
            df = pd.read_csv(os.path.join(channels_dir, fileName))
            if df.shape[0]<1000 or fileName=='ST4 ICN 10493 RTGH-S11iS1-6928.SM22014.csv':
                continue
            
            #files = [f.path for f in os.scandir(data_path) if (f.path.endswith('.csv'))]
            #files2 = [f.path for f in os.scandir(data_path2) if (f.path.endswith('.csv'))]
            #reliability = nr(cycles_per_day_group =cycles_per_day_group,start_dates = start_dates,n_steps = n_steps,target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups,station_names = station_names,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names, zero_strs = zero_vals	, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols)
            #reliability2 = nr(cycles_per_day_group = cycles_per_day_group,start_dates = start_dates,target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups2, station_names = station_names2,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names_2, zero_strs = zero_vals, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols)
            #p = partial(reliability.main,result_dir = result_dir)
            #p2 = partial(reliability2.main,result_dir = result_dir)
            #pool = Pool()
            #pool.map(p, files)
            #pool.map(p2,files2)
            #Select and add useful columns
            #dfC = Pool.map(c.clean, (fileName, channels_dir))
            #print(dfC.columns)
            #break
            dfC = c.clean(fileName, channels_dir)
            dfE = pd.read_csv(os.path.join(events_dir, fileName))
            dfV = pd.read_csv(os.path.join(variables_dir, fileName))
            
            #Create a new column for each event with the number of the event
            dfC = e.splitOnEvents(dfC, dfE, events, startings, endings)
            
            #Calculate efficiency
            dfC = f.effCalc(dfC, dfE, dfV)
            
            dfC.to_csv(os.path.join(resultPath,fileName), index = False)
            print('\n\n\n\n')
        else:
            continue