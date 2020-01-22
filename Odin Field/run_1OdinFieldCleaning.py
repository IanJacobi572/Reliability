import bson # depends on pymongo package
import pandas as pd
import os
import os.path, time
import datetime

directory = r'C:\Users\anes.madani\Desktop\Anes\Odin Field\bson'
result_dir = r'C:\Users\anes.madani\Desktop\Anes\Odin Field\raw'

def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in dirs:
            now = datetime.datetime.utcnow().strftime('%Y/%m/%d')
            t = time.strftime('%Y/%m/%d', time.gmtime(os.path.getmtime(root+'//'+name)))
            if name=='production' and now == t:
                r.append(os.path.join(root, name))
    return r

def read_bson(file_path):
    with open(file_path, 'rb') as infile:
        bson_data = bson.decode_all(infile.read())
    
    return pd.DataFrame(list(bson_data))
    
dirs = list_files(directory)

for dir in dirs:
    data = read_bson(os.path.join(dir, 'history.bson'))
    if 'mac_address' in data.columns:
        for fileName, df_unit in data.groupby('mac_address'):
            print(fileName)
            print('#####################################')
            if os.path.isfile(result_dir + '\\' + fileName + '.csv'):
                df = pd.read_csv(result_dir + '\\' + fileName + '.csv', low_memory = False) 
                df = pd.concat([df,df_unit], sort=False, ignore_index = True)
                df.to_csv(result_dir + '\\' + fileName + '.csv', index=False)
            else:
                df_unit.to_csv(result_dir + '\\' + fileName + '.csv', index=False)
    else:
        pass