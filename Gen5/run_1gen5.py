import os
from datetime import datetime
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
import gen5rel as pr 
from multiprocessing import Pool
from functools import partial
import Preprocessing as cols
import re
from collections import OrderedDict
import os
start_time = datetime.now()
data_path = 'H:/RDDEPT/Satellite Lab/Reliability EC Folders/EC 06768 - HPWH - Khurram Sajjad/NL TESTING 2019/ECONET Data'
result_dir = 'c:/gen5/split'
if not os.path.exists(result_dir):
	os.makedirs(result_dir)
joined_dir = 'c:/gen5/prp'

flame_col = 'HEATCTRL'
del_cols = ()
path  = 'c:/gen5'
intended_cols_outside = []
intended_cols = cols.find_intended_cols_multiple_file(data_path, path)
instance_names = {
    '17':'NL1301',
    '18':'NL1302',
    '19':'NL1303',
    '20':'NL1304',
    '14':'NL1299',
	'15':'NL1300',
	'6':'NL0434',
	'4':'NL0435',
	'3':'NL1289',
	'1':'NL0437',
    #'1':'NL0458',
	'5':'NL0428',
    '21':'NL305',
    '22':'NL306',
	'11':'NL1296',
	'12':'NL1297',
    #'11':'NL1320',
	#'12':'NL1321',
	'2':'NL0441',
	'7':'NL0442',
    '23':'NL307',
    '24':'NL308',
	'10':'NL1295',
	'9':'NL1294',
	'16':'NL0460',
	'8':'NL1293',
	'13':'NL1298',
	'25':''
}
station_names = {
    '17':'D1',
    '18':'D2',
    '19':'D3',
    '20':'D4',
	'14':'F8',
	'15':'F10',
	'6':'C10',
	'4':'C6',
	'3':'C5',
	'1':'C3',
	'5':'C9',
    '21':'D5',
    '22':'D6',
	'12':'F6',
	'11':'F5',
	'2':'C4',
	'7':'C11',
    '23':'D7',
    '24':'D8',
	'10':'F3',
	'9':'F2',
	'16':'F11',
	'8':'F1',
	'13':'F7',
	'25':''
}

all_files = []
all_folders = []
for root, dirs, files in os.walk(data_path):
	for name in files:
		all_files.append(os.path.join(root, name))
		if(name == "Rel_2019_11_1.csv"):
			print("HEREH")
	for name in dirs:
		all_folders.append(os.path.join(root, name))
all_cols = [f for f in intended_cols]
#print(subfolders)
for sub in all_folders:
	intended_cols_sub = cols.find_intended_cols_multiple_file(sub, path)
	if not(intended_cols_sub == None):
		col_diff = sorted(list(set(intended_cols_sub)- set(all_cols) ))
		all_cols = all_cols + [f for f in col_diff]
all_cols = list(OrderedDict.fromkeys(all_cols))
all_cols.remove('U')
#print(all_cols)

gen_out = pr.Gen5_Rel(all_cols = all_cols,station_names = station_names,instance_names = instance_names,intended_cols= all_cols, path  = 'c:/gen5', flame_col = flame_col)
gen_out.main(data_path, result_dir)
p_out = partial(gen_out.main,result_dir = result_dir)
def join(directory):
	files = sorted([f.path for f in os.scandir(directory)], reverse = True)
	#print(files)
	df = pd.concat(([pd.read_csv(file, low_memory = False) for file in files]), ignore_index = True)
	df.to_csv(joined_dir + '/' + directory.split('\\')[-1] + '.csv', index = False)
if __name__ == '__main__':
	pool = Pool()
	pool.map(p_out, all_files)
	sub_results = [f.path for f in os.scandir(result_dir) if f.is_dir() ]
	pool.map(join,sub_results)
	pool.close()
	pool.join()
	'''for directory in sub_results:
					df = pd.concat([pd.read_csv(file, low_memory = False) for file in os.scandir(directory.path)], ignore_index = True)
					df.to_csv(joined_dir + directory.name + '.csv')'''