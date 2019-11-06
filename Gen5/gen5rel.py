import yaml
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
import os
import re
from datetime import datetime
from set_config import set_config
from ftplib import FTP
import pandas as pd 
import Preprocessing as pr
from dateutil.parser import *
from num2words import num2words
import numpy as np 
from collections import OrderedDict
class Gen5_Rel(pr.Preprocessing_Base):
	def __init__(self, **kwargs):
		super(Gen5_Rel, self).__init__(**kwargs)
		self.station_names = kwargs.get('station_names')
		self.flame_col = kwargs.get('flame_col')
		self.instance_names = kwargs.get('instance_names')
		self.all_cols = kwargs.get('all_cols')

	def get_file_date(self, date):
		date = parse(date)
		return date.date()
	def create_multiple_file(self, df, result_dir, fileN, i, intended_cols_i, data_path):
		try:
			split_df = df[intended_cols_i].copy()
			split_df.columns = self.intended_cols[:-1]
		except KeyError as e:
			#print(e.args[0])
			missing = e.args[0].split('\'')
			for name in missing:
				if name in intended_cols_i:
					intended_cols_i.remove(name)
			intended_cols = [re.sub(r'_?[^A-Z_]+$', "", col) for col in intended_cols_i]
			split_df = df[intended_cols_i].copy()

			self.del_row_with_dashes(split_df)
			if split_df.shape[0] >1 and i != 25:
					#print(int(split_df['INSTANCE'].values[0]) > 7)
					instance = str(i)
					for col in self.all_cols:
						if not col in split_df.columns.values.tolist():
							split_df[col] = np.nan
					split_df = split_df[self.all_cols].copy()
					print(i)
					date_str = split_df["Date"].values.tolist()[-1]
					name = self.instance_names.get(instance)
					split_df['Unit_Name'] = name
					station = self.station_names.get(instance)
					split_df["Station"] = station
					k = result_dir+"\\" + name + "_"+ station + '\\'
					if not os.path.exists(k):
						os.makedirs(k)
						print(k)
					sig = name + "/" + date_str
					split_df.fillna('')
					#if split_df["Date"].values.tolist()[1] in df_result["Date"]:
						#print('aaaa')
					zero = np.array([0])
					if not self.binary_cols == None:
						self.binary_col_array(self.binary_cols, split_df)
					#Deprecated date check
					date = self.get_file_date(split_df["Date"].values.tolist()[-1])
					split_df["Month"] = date.strftime('%B')
					#start_date = parse('2019-7-8').date()
					split_df.to_csv(k + date_str.replace('/','_') + ".csv", index= False)
					print('Finished')
			else:
				
				if(fileN.split('\\')[-1] == "Rel_2019_11_1.csv"):
					print("empty")
	def read_files(self, data_path, result_dir):
		#find min cols of thing
		min_cols = len(self.intended_cols)
		#find differences between directories
		fileN = data_path
		#create df
		try:
			df = pd.read_csv(fileN, low_memory = False) 
		except Exception as e:
			df = []
			if(fileN.split('\\')[-1] == "Rel_2019_11_1.csv"):
				print("Not reading")
		if(len(df) > 0):
			cols = df.columns
			colnames = df.columns.values.tolist()
			digits_first = re.findall("\d+", colnames[2])
			digits_last = re.findall("\d+", colnames[-2])
			#print(colnames)
			last_int = digits_last[-1]
			first_int = digits_first[-1]
			print(first_int, last_int)
			self.format_multiple_cols(df, fileN, result_dir, data_path, first_int, last_int)     
			
	def format_multiple_cols(self, df, fileN, result_dir, data_path, first_int, last_int):
		print('f')
		for i in range(int(first_int), int(last_int)+1):
			colnames = df.columns.values.tolist()
			intended_cols_i =['Time', 'Date'] + [col + "_" + str(i) for col in self.intended_cols[2:-1]]
			zero = np.array([0])
			self.create_multiple_file(df, result_dir, fileN, i, intended_cols_i, data_path)
	  