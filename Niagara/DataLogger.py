import os
import pandas as pd
import numpy as np
class Mac_Dicts: 
	def __init__(self, owner, location,something, unit_name, recirc ):
		self.owner = owner
		self.location = location
		self.something = something
		self.unit_name = unit_name 
		self.recirc = recirc
	def get_owner():
		return owner
	def get_location():
		return location
	def get_something():
		return something
	def get_unit_name():
		return unit_name
	def get_recirc():
		return recirc
#def del_row_with_dashes(df):
	#df.drop(df.loc[].index, inplace =True)
whtr_modes = ['Off', 'Ready',            'Running',  'Off: Low Flow',    "Off: Error", 'Burner Stage TestMfg. Test',  'Baseline Test',    'Flow Restriction' ]
mac_dict = {
	'DC-F5-05-77-F2-DA': Mac_Dicts('Matt Smith',	'CO',	'125',	'ICN10201',		'Non-Recirc'),
	'DC-F5-05-77-F2-E7': Mac_Dicts('Medhavin P', 'GA',	'0',	'ICN10198',		'Non-Recirc'),
	'DC-F5-05-77-F2-E5': Mac_Dicts('Jonathan D',	'TX',	'ND',	'ICN10197', 'Non-Recirc'),
	'DC-F5-05-78-67-D0': Mac_Dicts('Ron V',	'Ontario',	'50',	'ICN10286',	'Recirculation'),
	'DC-F5-05-78-67-E2': Mac_Dicts('Stacy S',	'GA',	'25',	'ICN10285',	'Recirculation'),
	'DC-F5-05-77-F2-E3': Mac_Dicts('Karthik M',	'CA',	'50',	'ICN10284',	'Recirculation'),
	'DC-F5-05-78-25-D2': Mac_Dicts('Paul G',	'Ontario',	'50',	'ICN10206',	'Non-Recirc'),
	'DC-F5-05-78-63-4C': Mac_Dicts('Mark B',	'CT',	'ND',	'ICN10402',	'Recirculation'),
	'DC-F5-05-78-25-D1':Mac_Dicts('James G','IL',	'ND',	'ICN10279',	'Recirculation'),
	'DC-F5-05-78-67-E7':Mac_Dicts('Rick Y',	'MD',	'ND',	'ICN10288',	'Recirculation'),
	'DC-F5-05-78-67-DA':Mac_Dicts('Alexander D',	'WA',	'50',	'ICN10282',	'Recirculation'),
	'DC-F5-05-77-F2-C0':Mac_Dicts( 'Adam C',	'WA',	'85',	'ICN10409',	'Recirculation'),
	'DC-F5-05-77-F2-D5' :Mac_Dicts('Todd T',	'KY',	'ND',	'ICN10407',	'Recirculation'),
	'DC-F5-05-78-63-45':Mac_Dicts( 'Chris M','FL',	'ND',	'W261906701','Non-Recirc'),
	'DC-F5-05-77-F2-E9':Mac_Dicts('Shawn S',	'FL',	'ND',	'W261906699','Non-Recirc'),
	'DC-F5-05-78-67-D8': Mac_Dicts('Justin V','Ontario', 'ND','W261906697','Recirculation')
}

for mac in os.scandir(r"C:\Niagara\Macstuffffffff"):
	df = pd.read_csv(mac.path)
	df = df.dropna(how='all')
	print((mac.name[:-9]))
	try:
		
		df["Unit_name"] = mac_dict.get(mac.name[:-9]).get_unit_name()
	except Exception as e:
		continue
		raise e
	zero = np.array([0])
	name = 'MGASKBTU'
	if name in df.columns.values.tolist():
		gas = df[name].copy()
		gas = gas.dropna()
		n = np.ediff1d(gas)
		n = np.append(zero, n)
		gas = pd.DataFrame(data = n, index = gas.index)
		gas.columns = ['Gas Used']
		df['Gas Used']= gas
	if 'WHTRMODE' in df.columns.values.tolist():
		whtr_ints = df['WHTRMODE'].copy()
		whtr_strs = []
		for mode in whtr_ints.values:
			#print (mode)
			if not np.isnan(mode):
				whtr_strs.append(whtr_modes[int(mode)])
			else: 
				whtr_strs.append("Off")
		df['WHTRMODESTRINGS'] = whtr_strs
	df.to_csv('c:/Niagara/MACPRP/' + '/'+mac.name)




