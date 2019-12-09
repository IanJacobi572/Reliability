import pandas as pd
import os 
import csv
import re
from multiprocessing import Pool
data_path = r'C:\Anode\raw'
row = []
#for data in os.scandir(data_path):
def process(data):
	coating = {"1": 'coating','2':'no coating', '3':'no coating','4':'coating'}
	with open(data,'r') as f:
	    reader = csv.reader(f)
	    for i in range(0,4):
	    	row.append(next(reader))
	if data.endswith('.csv'):
		date = ''
		for r in row:
			if'/' in r[0]:
				date = r[0]
		dfcols= pd.read_csv(data,skiprows=6,nrows=1)
		dfcols.columns = [f.upper() for f in dfcols.columns.values]
		df = pd.read_csv(data, skiprows = 7, names = dfcols.columns, header=None, usecols = list(range(len(dfcols.columns))))
		digits = []
		df["Date"]=date
		columns = [col.replace('"','') for col in df.columns]
		df.columns = columns
		#df["TIME"] = pd.to_datetime(df["TIME"])
		for col in df.columns:
		    digits.append( re.findall("\d+", col))
		splits={1:[],2:[],3:[],4:[]}
		for dig,col in zip(digits[2:], df.columns[2:]):
		    if(len(dig)>0):
		        splits.get(int(dig[0])).append(col)
		f = [i for i in df.columns[:2]] + ["Date"]
		print(f)
		dataframes=[]
		for key in splits:
		    d = f+splits.get(key)
		    split_df = df[d].copy()
		    without_tank = f+[col[8:] for col in split_df.columns[3:]]
		    split_df.columns=without_tank
		    split_df["Tank"] = "Tank " + str(key) + " "+ coating.get(str(key))
		    print(split_df.columns)
		    dataframes.append(split_df)
		df_full=pd.concat(dataframes, ignore_index = True)
		#df_full["Date Time"] = str(date) + ' ' + str(df_full["TIME"].values[0])
		#df_full["Hour"] = pd.to_datetime(df_full["TIME"],infer_datetime_format = True).dt.hour
		k = r'C:\Anode\\data\\'+data.split('\\')[-1]
		if not os.path.exists(k):
			os.makedirs(k)
		df_full.to_csv(k, index = False)
if __name__ == '__main__':
	pool = Pool()
	data = [f.path for f in os.scandir(data_path) if f.path.endswith('.csv')]
	pool.map(process, data)