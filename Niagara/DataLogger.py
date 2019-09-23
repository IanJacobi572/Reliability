import os
import pandas as pd
import numpy as np
#def del_row_with_dashes(df):
	#df.drop(df.loc[].index, inplace =True)
whtr_modes = ['Off', 'Ready',            'Running',  'Off: Low Flow',    "Off: Error", 'Burner Stage TestMfg. Test',  'Baseline Test',    'Flow Restriction' ]

for mac in os.scandir(r"C:\Niagara\Macstuffffffff"):
	df = pd.read_csv(mac.path)
	df = df.dropna(how='all')

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
