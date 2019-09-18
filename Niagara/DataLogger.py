import os
import pandas as pd
import numpy
#def del_row_with_dashes(df):
	#df.drop(df.loc[].index, inplace =True)
whtr_modes = ['Off', 'Ready',            'Running',  'Off: Low Flow',    "Off: Error", 'Burner Stage TestMfg. Test',  'Baseline Test',    'Flow Restriction' ]

for mac in os.scandir(r"C:\Niagara\Macstuffffffff"):
	df = pd.read_csv(mac.path)
	if 'WHTRMODE' in df.columns.values.tolist():
		whtr_ints = df['WHTRMODE'].copy()
		whtr_strs = []
		for mode in whtr_ints.values:
			print (mode)
			if not numpy.isnan(mode):
				whtr_strs.append(whtr_modes[int(mode)])
			else: 
				whtr_strs.append("")
		df['WHTRMODESTRINGS'] = whtr_strs
		print(whtr_strs)
	df.to_csv('c:/Niagara/MACPRP/' + '/'+mac.name)
