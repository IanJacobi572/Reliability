import Preprocessing as pr
import yaml
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
import os
from set_config import set_config
from ftplib import FTP
from num2words import num2words
import pandas as pd 
import numpy as np 
#import ipdb
class Preprocessing_Triton_1_files(pr.Preprocessing_Base):
	def __init__(self, **kwargs):
		super(Preprocessing_Triton_1_files, self).__init__(**kwargs)
		self.vlv_col = kwargs.get('vlv_col')
		self.binary_cols = kwargs.get("binary_cols")
	def unit_name_from_path(self, data_path, df):
		name = os.path.basename(os.path.normpath(data_path))
		name = name.split(" ")[0]
		df["Unit_Name"] = name.upper()
	def vlvstate_to_str(self, vlv_col, df):
		
		if(vlv_col in df.columns):
			self.df_to_string(vlv_col, df)
			n = []
			switcher = {
				'1': "",
				'2': "Standby",
				'3': "Pre-purge",
				'4': "Pre-purge",
				'5': "Heating",
				'6': "Post-Purge",
				'Standby': "Standby",
				"Pre-purge": "Pre-purge",
				"Heating" : "Heating",
				"Post-Purge": "Post-Purge",
			}
			for val in df[vlv_col].values:
				n = np.append(n, switcher.get(val))
			df[vlv_col] = pd.DataFrame(n)


	#when you have a manifold, consider them seperately, and split the file in hald
	def format_multiple_cols(self, df, fileN, result_dir, data_path, i, last_int):
		binary_cols_i = []

		vlv_col_i = "VLVSTATE_" + str(i)
		intended_cols_i = ["Time", "Date"]
		if(self.binary_cols in df.columns):
			binary_cols_i = [col +'_' +str(i) for col in self.binary_cols]
		cols_to_fix_i = [col + "_" + str(i) for col in self.cols_to_fix]
		intended_cols_i = intended_cols_i + [col + "_" + str(i) for col in self.intended_cols[2:-1]]

		zero = np.array([0])
		self.vlvstate_to_str(vlv_col_i, df)
		self.binary_col_array(binary_cols_i, df)
		self.prepare_arr_of_cols(zero, cols_to_fix_i, df)
		self.create_multiple_file(df, result_dir, fileN, i, intended_cols_i, data_path)
		if i < int(last_int):
			i+= 1
			self.format_multiple_cols(df, fileN, result_dir, data_path, i, last_int)
	def format_cols(self, cols, df, fileN, result_dir, data_path):
		df.columns = self.intended_cols
		#ipdb.set_trace()
		#self.alarm_string(df)
		if df.shape[0] > 1: #Ignore changing the files with only one row
			cols = df.columns
			#retrieve unit name
			self.unit_name(data_path, df)
			self.binary_col_array(self.binary_cols, df)
			self.vlvstate_to_str(self.vlv_col, df)
			print(fileN, len(cols), cols[-1], cols[0])

			#Save only the files that contain info
			self.create_file(result_dir, fileN, df)
		else:
			print("\n\n\n*******\n", fileN, " = not considered in analysis\n because it has only 1 line of data")
	#ipdb.set_trace()
	def read_files(self, data_path, result_dir):
		min_cols = len(self.intended_cols)
		file_names = self.find_different(data_path, result_dir)
		for fileN in file_names:
			#create df
			try:
				df = pd.read_csv(data_path + "\\" + fileN)      
			except Exception as e:
				continue
			self.delete_cols(df, self.del_cols)

			cols = df.columns
			colnames = df.columns.values.tolist()
			last_col = colnames[-12]
			last_int = last_col[-1]
			if( len(cols) == min_cols):
				self.format_cols(cols, df, fileN, result_dir, data_path)
			elif(self.check_if_multiple(df, last_int)):
				self.format_multiple_cols(df, fileN, result_dir, data_path, 1, last_int)
