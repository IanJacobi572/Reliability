import pandas as pd 
import os
from multiprocessing import Pool
from nptdms import TdmsFile
def find_different(files, subfiles):
    all_files = files+subfiles
    if not os.path.exists('C:/Niagara/UEF/Channels'):
        return all_files
    csv_files = [f.name for f in os.scandir('C:/Niagara/UEF/Channels')]
    processed = []
    for file in all_files:
        for done in csv_files:
            #print(file.split('\\')[-1][:-5], done[:-4])
            if(done[:-4] in file.split('\\')[-1][:-5]):
                #print('1')
                processed.append(file)
                break

    return	set(all_files)-set(processed)
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
        pass
data_path = '//onerheem/whd-onerheemdfs/Data2 on WM1FSPROD02/PDP/PROJECT FOLDERS/TNK PROJECTS/Proj EC06619/R&D/Development/DOE test'
#data_path = 'C:/Users/anes.madani/Desktop/Anes'
files = [f.path for f in os.scandir(data_path) if f.name.endswith('tdms')]
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir()]    
subfiles = []
for sub in subfolders:
    subf = [f.path for f in os.scandir(sub) if f.path.endswith('.tdms')]
    for f in subf:
        subfiles.append(f)
if __name__ == '__main__':
    pool = Pool()
    #print(find_different(files, subfiles))
    pool.map(tdms_extract, find_different(files, subfiles))