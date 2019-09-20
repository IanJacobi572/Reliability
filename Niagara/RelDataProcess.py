import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from NiagaraRel import Niagara_Reliability as nr
intended_cols = ("Time","Date","INSTANCE","TEMP__IN","TEMP_OUT","TEMPHTX1","TEMP_EXH","VOLU_CTL","FLOW_GPM","BYPRATIO","FAN__SPD","FLM_ROD1","ALARM_01")
path = 'C:/Niagara'
#data_path = "//onerheem/whd-onerheemdfs/Data on BDATAPROD2/RDDEPT/Satellite Lab/Reliability EC Folders/EC06619 -NIAGARA 2018 TAKASHI/NL TESTING 2019/ECONET Data"
data_path =  r'C:\Users\ian.jacobi\Documents\ltere'
#data_path2 = "F:/Data on BDATAPROD2/RDDEPT/Satellite Lab/Reliability EC Folders/EC06619 -NIAGARA 2018 TAKASHI/NL TESTING 2019/Low flowrate test/ECONET Data"
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
	'1' : 'H8',
	'2' : 'H9'
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
	'1' : 'ICN1266',
	'2' : 'ICN1267'
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
reliability = nr(n_steps = n_steps,target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups,station_names = station_names,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names, zero_strs = zero_vals	, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols)
reliability.main(data_path, result_dir)
reliability2 = nr(target_cycles = target_cycles,diff_cycles = diff_cycles,groups = groups2, station_names = station_names2,flame_col = 'FLM_ROD1',temp_cols = temp_cols,instance_names = instance_names_2, zero_strs = zero_vals, one_strs = one_vals, path= path, intended_cols = intended_cols, binary_cols = binary_cols)
reliability2.main(data_path2, result_dir)