import os
import pandas as pd
import sys
import numpy as np
import datetime
from dateutil.parser import *
sys.path.append(os.path.dirname(os.getcwd()))
from NiagaraRel import Niagara_Reliability as nr
intended_cols = ("Time","Date","INSTANCE","TEMP__IN","TEMP_OUT","TEMPHTX1","TEMP_EXH","VOLU_CTL","FLOW_GPM","BYPRATIO","FAN__SPD","FLM_ROD1","ALARM_01")
path = 'C:/Niagara'
data_path = r"C:\Niagara\prpbeforecycles"
#data_path =  r'C:\Users\ian.jacobi\Documents\aaaa\niagra\RelData'
data_path2 = "F:/Data on BDATAPROD2/RDDEPT/Satellite Lab/Reliability EC Folders/EC06619 -NIAGARA 2018 TAKASHI/NL TESTING 2019/Low flowrate test/ECONET Data"
#data_path2 = r'C:\Users\ian.jacobi\Documents\aaaa\niagra\lf'

result_dir = path + '/prp/'
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
for file in os.scandir(data_path):
	df = pd.read_csv(file.path, low_memory = False)
	i = str(int(df["INSTANCE"].values.tolist()[0]))
	#print(parse(str(df['Date'].values.tolist()[0])).date().isocalendar())
	#week1 = parse(df['Date'].values.tolist()[0]).date().isocalendar()[1]
	#week = [parse(f).date().isocalendar()[1] - week1 for f in df['Date'].values.tolist() if type(f) is str]
	df["Date"] = pd.to_datetime(df.Date, format = '%Y-%M-%d')
	df["Time"] = pd.to_datetime(df.Time, format = '%H:%M:%S')
	#df.sort_values(by = "Date", inplace = True)
	#print(df['Cycles'].unique())
	date = (str(df["Date"].values.tolist()[-2]))
	print(date)
	if not df['Group'].values.tolist()[0] == 'Low Flow':
		group = groups.get((i))
		station = station_names.get(str(i))
		name = instance_names.get(str(i))
		print(i)
		df = df.append({'Date' : '','Unit_Name' : name, 'Station' : station, 'Group' : group, 'Cycles' : diff_cycles.get(station_names.get(i))}, ignore_index = True)
		target = target_cycles.get(group)
	else:
		station = station_names2.get(str(i))
		name = instance_names_2.get(str(i))
		group = groups2.get(str(i))
		df = df.append({'Date' : '','Unit_Name' : name, 'Station' : station, 'Group' : group,  'Cycles' : int(diff_cycles.get(station))}, ignore_index = True)
		target = target_cycles.get(group)
	running_count = df['Cycles'].cumsum()
	print(running_count)
	start_of_week = [df.index[np.searchsorted(df.A,f)] for f in df.A.unique()]
	for i in len(start_of_week):
		previous_sum = df.iloc[0:start_of_week[i]].sum()
		target_for_week = previous_sum + cycles_per_day_group.get(group)*7
		df.iloc[start_of_week[i-1]:start_of_week[i], 'Target For Week'] = target_for_week
	 
	remaining = target - running_count.values.tolist()[-1]
	df["Current Cycles"] = running_count
	df['Remaining Cycles'] = remaining
	df['Expected Cycles Per Day'] = cycles_per_day_group.get(group)
	df['Completion Percent'] = running_count.values.tolist()[-1]/target
	days_left = remaining/cycles_per_day_group.get(group)
	date = (date)
	est_date = (df["Date"].values.tolist()[-3]) + datetime.timedelta(days = int(days_left))
	df["Estimated Completion"] = est_date
	df.to_csv(result_dir + '/' + file.name + '.csv', index = False)