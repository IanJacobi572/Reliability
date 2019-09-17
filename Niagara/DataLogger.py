import os
import pandas as pd
import numpy
#def del_row_with_dashes(df):
	#df.drop(df.loc[].index, inplace =True)

for mac in os.scandir(r"C:\Niagara\Macstuffffffff"):
	df = pd.read_csv(mac.path)
	for col in df.columns.values.tolist()[1:]:
		new_cols = ["timestamp", col]
		split_df = df[new_cols].copy()
		split_df.dropna(inplace = True)
		#del_row_with_dashes(split_df)
		if not os.path.exists('C:/Niagara/MACPRP/' + col):
			os.mkdir('C:/Niagara/MACPRP/' + col)
		split_df.to_csv('c:/Niagara/MACPRP/' + col + '/'+mac.name  + '.csv')
