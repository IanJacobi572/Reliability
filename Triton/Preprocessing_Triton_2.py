import Preprocessing as pr
import yaml
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
import os
from set_config import set_config
from ftplib import FTP
import pandas as pd 
import numpy as np 
class Preprocessing_Triton_2_files(pr.Preprocessing_Base):
	def __init__(self,**kwargs):
		super(Preprocessing_Triton_2_files, self).__init__(**kwargs)
	def toInt(self, binary_col, df):
		if(binary_col in df.columns):
			n = []
			df[binary_col] = df[binary_col].astype(str)
			for val in df[binary_col].values:
				val = int(val, 2)
				n.append(str(val))
			df[binary_col] = pd.DataFrame(n)
	def unit_name(self, data_path, df):
		name = os.path.basename(os.path.normpath(data_path))
		name = name.split(" ")[0]
		df["Unit_Name"] = name.upper()
	def format_cols(self, cols, df, fileN, result_dir, data_path):
		df.columns = self.intended_cols
		self.unit_name(data_path, df)
		#ipdb.set_trace()
		if df.shape[0] > 1: #Ignore changing the files with only one row
			cols = df.columns
			#retrieve unit name
			self.unit_name(data_path, df)
			self.alarm_string(df)
			# Fix the Gallons Columns, Successful Ignitions, Failed Ignitions
			# ,Flame Failures, Burner Minutes
			zero = np.array([0])
			print(fileN)
			#for colu in cols_to_fix:
			#fnc.prepare_col(colu, zero)
			self.prepare_arr_of_cols(zero, df)

			self.toInt('AND3STAT', df)
			print(fileN, len(cols), cols[-1], cols[0])

			#Save only the files that contain info
			self.create_file(result_dir, fileN, df)
		else:
			print("\n\n\n*******\n", fileN, " = not considered in analysis\n because it has only 1 line of data")
	def read_files(self, data_path, result_dir, min_cols):
		file_names = self.find_different(data_path, result_dir)

		for fileN in file_names:
		#create df
			try:
				df = pd.read_csv(data_path + "\\" + fileN)      
			except Exception as e:
				continue
			self.delete_cols(df, self.del_cols)

			cols = df.columns

			if( len(cols) == min_cols):
				self.format_cols(cols, df, fileN, result_dir, data_path)

			elif(self.check_if_multiple(df)):
				self.format_multiple_cols(cols, df, fileN, result_dir, data_path, 1)
	#ipdb.set_trace()
	def main(self, data_path, result_dir):
		config_path = self.path + "/Config"
		login_path = config_path + "/login.yaml"
		path_path = config_path + "/path.yaml"
		result_dir = self.path + result_dir
		if os.path.exists(result_dir) == False:
			os.mkdir(result_dir)
		self.read_files(data_path, result_dir, self.min_cols)
