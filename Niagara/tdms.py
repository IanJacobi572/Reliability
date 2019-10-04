import pandas as pd 
import os
from nptdms import TdmsFile
def tdms_extract(entry):
     if(entry.name.endswith('.tdms')):
                tdms_file = TdmsFile(entry)
                for group in tdms_file.groups():
                    data = tdms_file.object(group).as_dataframe()
                    if group == 'Events':
                        data["TimeStamp"] = data["TimeStamp"].astype(float).values - float(data["TimeStamp"].values[0])
                    if group == 'Channels':
                        data["TimeStamp (sec)"] = data["TimeStamp (sec)"].values - data["TimeStamp (sec)"].values[0]
                    if not os.path.exists('C:/Niagara/UEF/' + group):
                        os.makedirs('C:/Niagara/UEF/' + group)
                    data.to_csv('C:/Niagara/UEF/' +group + "/" + entry.name[:-5] +".csv")
data_path = '//onerheem/whd-onerheemdfs/Data2 on WM1FSPROD02/PDP/PROJECT FOLDERS/TNK PROJECTS/Proj EC06619/R&D/Development/DOE test'
files = [f for f in os.scandir(data_path) if f.name.endswith('tdms')]
for file in files:
    tdms_extract(file)
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir()]    

for sub in subfolders:
    with os.scandir(sub) as list_of_entries:
        for entry in list_of_entries:
           tdms_extract(entry)