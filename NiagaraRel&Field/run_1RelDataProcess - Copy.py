import os
import pandas as pd
import sys
from multiprocessing import Pool
import datetime
from functools import partial
from dateutil.parser import *
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
from NiagaraRel import Niagara_Reliability as nr
intended_cols = ["Time","Date","INSTANCE","TEMP__IN","TEMP_OUT","TEMPHTX1","TEMP_EXH","VOLU_CTL","FLOW_LPM","BYPRATIO","FAN__SPD","FLM_ROD1","ALARM_01"]
path = 'C:/Niagara'
data_path = r"H:\RDDEPT\Satellite Lab\Reliability EC Folders\EC06619 -NIAGARA 2018 TAKASHI\NL TESTING 2019 (November)\ECONET Data"
#data_path =  r'C:\Users\ian.jacobi\Documents\aaaa\niagra\RelData'
#data_path2 = r'C:\Users\ian.jacobi\Documents\aaaa\niagra\lf'
start_dates = {
	}
result_dir = r'C:\Niagara\prpbeforecycles'
#for file in os.scandir(result_dir):#
#	os.unlink(file.path)
binary_cols = ("FLM_ROD1", "FREEZING")
instance_names = {
'1':	'NL1322',
'2':	'NL1323',
'3':	'NL1324',
'4':	'NL1325',
'5':	'NL1326',
'6':	'NL1327',
'7':	'NL1328',
'8':	'NL1329'

}
station_names= {
	'E1'	:'1',
'E2'	:	'2',
'E3'	:	'3',
'E4'	:	'4',
'E5'	:	'5',
'E6'	:	'6',
'E7'	:	'7',
'E8'	:	'8'

}
target_cycles = {
	'1' : 14400,
	'2' : 25100,
	'3' : 14400,
	'Low Flow': 15631
}
station_names2 = {
	'2' : 'H8',
	'1' : 'H9'
}
groups =  {
}
cycles_per_day_group= {
	'1':72,
	'2':412,
	'3':72,
	'Low Flow':144
}
files = [f.path for f in os.scandir(data_path) if (f.path.endswith('.csv'))]
reliability = nr(cycles_per_day_group =cycles_per_day_group,start_dates = start_dates,n_steps = n_steps,target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups,station_names = station_names,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names, zero_strs = zero_vals	, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols)

p = partial(reliability.main,result_dir = result_dir)
if __name__ == '__main__':
	pool = Pool()
	pool.map(p, files)
	pool.map(p2,files2)
