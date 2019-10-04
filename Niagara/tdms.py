import pandas as pd 
import os
from multiprocessing import Pool
from nptdms import TdmsFile
def tdms_extract(entry):
    try:
        if(entry.endswith('.tdms')):
            tdms_file = TdmsFile(entry)
            for group in tdms_file.groups():
                data = tdms_file.object(group).as_dataframe()
                if group == 'Events':
                    data["TimeStamp"] = data["TimeStamp"].astype(float).values - float(data["TimeStamp"].values[0])
                if group == 'Channels':
                    data["TimeStamp (sec)"] = data["TimeStamp (sec)"].values - data["TimeStamp (sec)"].values[0]
                if not os.path.exists('C:/Niagara/UEF/' + group):
                    os.makedirs('C:/Niagara/UEF/' + group)
                name = entry.split('\\')[-1]
                data.to_csv('C:/Niagara/UEF/' +group + "/" + name[:-5] +".csv")
    except Exception as e:
        raise e
data_path = '//onerheem/whd-onerheemdfs/Data2 on WM1FSPROD02/PDP/PROJECT FOLDERS/TNK PROJECTS/Proj EC06619/R&D/Development/DOE test'
files = [f.path for f in os.scandir(data_path) if f.name.endswith('tdms')]
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir()]    
subfiles = []
for sub in subfolders:
    files = [f.path for f in os.scandir(sub) if f.path.endswith('.tdms')]
    for f in files:
        subfiles.append(f)
if __name__ == '__main__':

    pool = Pool()
    pool.map(tdms_extract, subfiles)
    pool.map(tdms_extract, files)