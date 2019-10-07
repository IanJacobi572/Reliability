import os
import pandas as pd
import sys
import datetime
from multiprocessing import Process, Pool
from dateutil.parser import *
import threading
from math import ceil
sys.path.append(os.path.dirname(os.getcwd()))
from NiagaraRel import Niagara_Reliability as nr
intended_cols = ["Time","Date","INSTANCE","TEMP__IN","TEMP_OUT","TEMPHTX1","TEMP_EXH","VOLU_CTL","FLOW_GPM","BYPRATIO","FAN__SPD","FLM_ROD1","ALARM_01"]
path = 'C:/Niagara'
data_path = "//onerheem/whd-onerheemdfs/Data on BDATAPROD2/RDDEPT/Satellite Lab/Reliability EC Folders/EC06619 -NIAGARA 2018 TAKASHI/NL TESTING 2019/ECONET Data"
#data_path =  r'C:\Users\ian.jacobi\Documents\aaaa\niagra\RelData'
data_path2 = "F:/Data on BDATAPROD2/RDDEPT/Satellite Lab/Reliability EC Folders/EC06619 -NIAGARA 2018 TAKASHI/NL TESTING 2019/Low flowrate test/ECONET Data"
#data_path2 = r'C:\Users\ian.jacobi\Documents\aaaa\niagra\lf'
start_dates = {
	'G9' : datetime.date(2019, 4, 4).isocalendar()[1],
	'G12' : datetime.date(2019, 4, 4).isocalendar()[1],
	'G15' : datetime.date(2019, 5, 7).isocalendar()[1],
	'G14' : datetime.date(2019, 5, 9).isocalendar()[1] ,
	'G13': datetime.date(2019, 5, 6).isocalendar()[1],
	'H10' :datetime.date(2019, 7, 13).isocalendar()[1],
	'G7' :datetime.date(2019, 4, 3).isocalendar()[1],
	'G5' :datetime.date(2019, 4, 3).isocalendar()[1],
	'G6' :datetime.date(2019, 4, 3).isocalendar()[1],
	'G3' :datetime.date(2019, 4, 3).isocalendar()[1],
	'G4' :datetime.date(2019, 4, 3).isocalendar()[1],
	'E8' :datetime.date(2019, 4, 3).isocalendar()[1],
	'E9' :datetime.date(2019, 4, 3).isocalendar()[1],
	'G2' :datetime.date(2019, 5,15).isocalendar()[1],
	'H8': datetime.date(2019, 8, 12).isocalendar()[1],
	'H9': datetime.date(2019, 8, 2).isocalendar()[1]
	
}
result_dir = r'C:\Niagara\prpbeforecycles'
for file in os.scandir(result_dir):
	if file.name.startswith('R'):
		os.unlink(file.path)
binary_cols = ("FLM_ROD1", "FREEZING")
instance_names = {
	'1':"NL1283",
	'2':"NL1281",
	'3':"NL1280",
	'4':"NL1278",
	'5':"NL1276",
	'6':"NL1275",
	'7':"NL1274",
	'8':"NL1273",
	'9':"NL1272",
	'10':"NL1271",
	'11':"NL1268",
	'12':"NL1269",
	'13':"NL1270",
	'14':"NL1287"
}
n_steps = {
	'1': 420,
	'2': 10,
	'3': 42,
	'Low Flow': 25
}
station_names= {
	'1':"E9",
	'2':"E8",
	'3':"G12",
	'4':"G9",
	'5':"G7",
	'6':"G6",
	'7':"G5",
	'8':"G4",
	'9':"G3",
	'10':"G13",
	'11':"G14",
	'12':"G15",
	'13':"H10",
	'14':"G2"
}
target_cycles = {
	'1' : 14400,
	'2' : 25100,
	'3' : 14400,
	'Low Flow': 61320
}
diff_cycles = {
	'G9' : 11360,
	'G12' : 15647,
	'G15' : 20110,
	'G14' : 18536 ,
	'G13': 20564,
	'H10' :18684,
	'G7' :2747,
	'G5' :2683,
	'G6' :2737,
	'G3' :2672,
	'G4' :2749,
	'E8' :3071,
	'E9' :4387,
	'G2' :1055,
	'H8': 154,
	'H9': 333
}
station_names2 = {
	'2' : 'H8',
	'1' : 'H9'
}
groups =  {
	'1':"1",
	'2':"1",
	'3':"2",
	'4':"2",
	'5':"3",
	'6':"3",
	'7':"3",
	'8':"3",
	'9':"3",
	'10':"2",
	'11':"2",
	'12':"2",
	'13':"2",
	'14':"3"
}
instance_names_2 = {
	'2' : 'ICN1266',
	'1' : 'ICN1267'
}
groups2 = {
	'1':'Low Flow',
	'2': 'Low Flow'
}
zero_vals = {
	"FLM_ROD1": "Flame Not Present",
	"FREEZING" : "Not Freezing"
}
one_vals = {
	"FLM_ROD1":"Flame Present",
	"FREEZING" :"Freezing"
}

temp_cols = {
	"in": "TEMP__IN",
	"out": "TEMP_OUT"
}
cycles_per_day_group= {
	'1':72,
	'2':412,
	'3':72,
	'Low Flow':144
}
t = []
r =[]
reliability = nr(result_dir = result_dir,cycles_per_day_group =cycles_per_day_group,start_dates = start_dates,n_steps = n_steps,target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups,station_names = station_names,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names, zero_strs = zero_vals	, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols)
#reliability.main(data_path, result_dir)
files = [f for f in os.scandir(data_path)]
paths = [path.path for path in files]
begend = []
if(__name__ == '__main__'):
	try:
		pool = Pool()
		da_map = pool.map(reliability.main, paths)
	finally:
		pool.close()
		pool.join()
		for df_array in da_map:
			try:
				for df in df_array:
					print(df['Unit_Name'].values.tolist()[0])
					k = result_dir+'/'+df['Unit_Name'].values.tolist()[0]+ '.csv'
					if(os.path.exists(k)):
						print('a')
						df.to_csv(k, mode = 'a', header = False, index = False)
					else: 
						df.to_csv(k, mode = 'a', index = False)
			except:
				pass
'''for i in range(1, 17):
for df in da_map:
	k = result_dir+df['Unit Name'].values.tolist()[1]+ '.csv'
	df.to_csv(k)
	r.append(nr(cycles_per_day_group =cycles_per_day_group,start_dates = start_dates,n_steps = n_steps,target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups,station_names = station_names,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names, zero_strs = zero_vals	, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols))
	starting = i-1
	start = len(files)* starting
	start = ceil(start/16 )
	end = len(files) * i 
	end = ceil(end/16)
	begend.append(paths[start:end])
	#t.append(Process(target = r[i-1].main(paths[start:end], result_dir, i), name = str(i)))
	#Process(target = r[i-1].main(paths[start:end], result_dir, i), name = str(i)).start()
	#print('a2')'''
#print(threading.active_count())
#t[0].start()
#t[1].start()
#t[2].start()
#reliability2 = nr(cycles_per_day_group = cycles_per_day_group,start_dates = start_dates,target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups2, station_names = station_names2,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names_2, zero_strs = zero_vals, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols)
#reliability2.main(data_path2, result_dir)
'''for file in os.scandir(result_dir):
	df = pd.read_csv(file.path, low_memory = False, parse_dates = ["Date"])
	i = str(int(df["INSTANCE"].values.tolist()[0]))
	week1 = df['Date'].values.tolist()[0].date.isocalender()[1]
	week = [f.date.isocalender()[1] - week1 for f in df['Date'].values.tolist()]

	if not df['Group'].values.tolist()[0] == 'Low Flow':
		group = groups.get((i))
		print(i)
		df = df.append({'Date' : '','Cycles' : diff_cycles.get(station_names.get(i))}, ignore_index = True)
		target = target_cycles.get(group)
	else:
		df = df.append({'Date' : '', 'Cycles' : int(diff_cycles.get(station_names2.get(str(i))))}, ignore_index = True)
		group = groups2.get(str(i))
		target = target_cycles.get(group)
	running_count = df['Cycles'].cumsum()
	print(running_count)
	remaining = target - running_count.values.tolist()[-1]
	df["Current Cycles"] = running_count
	df['Remaining Cycles'] = remaining
	df['Expected Cycles Per Day'] = cycles_per_day_group.get(group)
	days_left = remaining/cycles_per_day_group.get(group)
	date = (str(df["Date"].values.tolist()[-2]))
	print(date)
	date = parse(date)
	est_date = df["Date"].values.tolist()[-3] + datetime.timedelta(days = int(days_left))
	df["Estimated Completion"] = est_date
	df.to_csv(file.path, index = False)'''