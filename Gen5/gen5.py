import os
from datetime import datetime
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.getcwd()))
import gen5rel as pr 
from multiprocessing import Pool
from functools import partial
import Preprocessing as cols
import re
from collections import OrderedDict
import os
start_time = datetime.now()
data_path = 'F:/Data on BDATAPROD2/RDDEPT/Satellite Lab/Reliability EC Folders/EC 06768 - HPWH - Khurram Sajjad/NL TESTING 2019/ECONET Data'
result_dir = 'c:/gen5/split'
if not os.path.exists(result_dir):
	os.mkdir(result_dir)
joined_dir = 'c:/gen5/prp'

flame_col = 'HEATCTRL'
del_cols = ()
path  = 'c:/gen5'
intended_cols_outside = []
intended_cols = cols.find_intended_cols_multiple_file(data_path, path)
print(intended_cols)
instance_names = {
	'14':'NL1299',
	'15':'NL1300',
	'6':'NL0434',
	'4':'NL0435',
	'3':'NL1289',
	'1':'NL0437',
	'5':'NL0428',
	'11':'NL1296',
	'12':'NL1297',
	'2':'NL0441',
	'7':'NL0442',
	'10':'NL1295',
	'9':'NL1294',
	'16':'NL0460',
	'8':'NL1293',
	'13':'NL1298'
}
station_names = {
	'14':'F8',
	'15':'F10',
	'6':'C10',
	'4':'C6',
	'3':'C5',
	'1':'C3',
	'5':'C9',
	'12':'F6',
	'11':'F5',
	'2':'C4',
	'7':'C11',
	'10':'F3',
	'9':'F2',
	'16':'F11',
	'8':'F1',
	'13':'F7'
}
all_cols = [f for f in intended_cols]
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir() ]
for sub in subfolders:
	subfolders = subfolders + [f.path for f in os.scandir(sub) if f.is_dir() ]
for sub in subfolders:
	subfolders = subfolders + [f.path for f in os.scandir(sub) if f.is_dir() ]
print(subfolders)
for sub in subfolders:
	intended_cols_sub = cols.find_intended_cols_multiple_file(sub, path)
	if not(intended_cols_sub == None):
		col_diff = sorted(list(set(intended_cols_sub)- set(all_cols) ))
		print(col_diff)
		all_cols = all_cols + [f for f in col_diff]
all_cols = list(OrderedDict.fromkeys(all_cols))
all_cols.remove('U')
print(all_cols)

gen_out = pr.Gen5_Rel(all_cols = all_cols,station_names = station_names,instance_names = instance_names,intended_cols= intended_cols, path  = 'c:/gen5', flame_col = flame_col)
gen_out.main(data_path, result_dir)
p_out = partial(gen_out.main,result_dir = result_dir)
def join(directory):
	df = pd.concat([pd.read_csv(file, low_memory = False) for file in os.scandir(directory)], ignore_index = True)
	df.to_csv(joined_dir + '/' + directory.split('\\')[-1] + '.csv', index = False)
if __name__ == '__main__':
	pool = Pool()
	for sub in subfolders:	
		intended_cols_sub = cols.find_intended_cols_multiple_file(sub, path)
		if not(intended_cols_sub == None):
			gen_sub = pr.Gen5_Rel(all_cols = all_cols,station_names = station_names, instance_names = instance_names, intended_cols = intended_cols_sub, path = path, flame_col = flame_col)
			
			p_sub= partial(gen_sub.main,result_dir = result_dir)
			pool.map(p_sub, [f.path for f in os.scandir(sub)])
	pool.map(p_out,  [f.path for f in os.scandir(data_path)])
	sub_results = [f.path for f in os.scandir(result_dir) if f.is_dir() ]
	pool.map(join,sub_results)
	pool.close()
	pool.join()
	'''for directory in sub_results:
					df = pd.concat([pd.read_csv(file, low_memory = False) for file in os.scandir(directory.path)], ignore_index = True)
					df.to_csv(joined_dir + directory.name + '.csv')'''
