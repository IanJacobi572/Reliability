import pandas as pd
from multiprocessing import Pool
import os
def read_daq(file_path):
	try:
	#file_path = r'C:\Users\ian.jacobi\Documents\ltere\G5 NIAGARA NL1201.txt'
		file_name = file_path.split('\\')[-1]
		df= pd.read_csv(file_path, sep = '\t', skiprows =7, usecols = [0,1,2,3,4,5,6,])
		df.columns = ['Date', 'Time', 'Mean Top Flue', 'Mean Outlet Water', 'Mean Inlet Water', 'Mean Air Intake', ' Unused']
		station = file_name.split(' ')[0]
		df["Station"] = station
		df.Date = pd.to_datetime(df.Date, infer_datetime_format=True).dt.date
		start_date = df.Date.values[0]
		print(start_date)
		start_week = start_date.isocalendar()[1]
		df["Week"] = [f.isocalendar()[1] + (((f.year-start_date.year)* 52)) - (start_week ) for f in df.Date.values.tolist()]
		result_dir = 'C:/Niagara/DAQ/'
		if not os.path.exists(result_dir):
			os.mkdir(reult_dir)
		df.to_csv('C:/Niagara/DAQ/' + file_name[:-4] + '.csv')
	except Exception as e:
		raise e
if __name__ == '__main__':
	pool = Pool()
	data_path = r'\\Wn2srvrelia\RELIABILITY\Reliability DAQ Files'
	files = [f.path for f in os.scandir(data_path) if 'Niagara' in f.name]
	print(files)

	pool.map(read_daq, files)