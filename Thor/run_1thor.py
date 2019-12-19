import os
from datetime import datetime
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
import thor5rel as pr 
from multiprocessing import Pool
from functools import partial
import Preprocessing as cols
import re
from collections import OrderedDict
import os
start_time = datetime.now()
data_path = 'c:/Thor/raw'
result_dir = 'c:/Thor/split'
if not os.path.exists(result_dir):
	os.makedirs(result_dir)
joined_dir = 'c:/Thor/prp'
if not os.path.exists(joined_dir):
	os.makedirs(joined_dir)

flame_col = 'HEATCTRL'
del_cols = ()
path  = 'c:/Thor'
intended_cols_outside = []
intended_cols = cols.find_intended_cols_multiple_file(data_path, path)
instance_names = {
	'1':'10879',
	'2':'10986',
	'3':'10987',
	'4':'10988'
}
station_names = {
	'1':'MGM 4',
	'2':'MGM 3',
	'3':'MGM 1',
	'4':'MGM 2'
}



def join(directory):
	files = sorted([f.path for f in os.scandir(directory)], reverse = True)
	print(files)
	df = pd.concat(([pd.read_csv(file, low_memory = False) for file in files]), ignore_index = True)
	df.to_csv(joined_dir + '/' + directory.split('\\')[-1] + '.csv', index = False)
'''def check_for_repeats(files):
	for file in files:
		for done in os.scandir(joined_dir):
			if()'''
if __name__ == '__main__':
	all_files = []
	all_folders = []
	for root, dirs, files in os.walk(data_path):
		for name in files:
			all_files.append(os.path.join(root, name))
			
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

	gen_out = pr.Gen5_Rel(all_cols = all_cols,station_names = station_names,instance_names = instance_names,intended_cols= all_cols, path  = 'c:/Thor', flame_col = flame_col)
	gen_out.main(data_path, result_dir)
	p_out = partial(gen_out.main,result_dir = result_dir)
	pool = Pool()
	pool.map(p_out, all_files)
	sub_results = [f.path for f in os.scandir(result_dir) if f.is_dir() ]
	pool.close()
	pool.join()
	pool2 = Pool()
	pool2.map(join,sub_results)
	pool2.close()
	pool2.join()
	'''for directory in sub_results:
					df = pd.concat([pd.read_csv(file, low_memory = False) for file in os.scandir(directory.path)], ignore_index = True)
					df.to_csv(joined_dir + directory.name + '.csv')'''