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

	def get_file_date(self, date):
		date = parse(date)
		return date.date() 
	def create_multiple_file(self, df, result_dir, fileN, i, intended_cols_i, data_path):
		try:
			split_df = df[intended_cols_i].copy()
			split_df.columns = self.intended_cols[:-1]
			self.del_row_with_dashes(split_df)
			#print(int(split_df['INSTANCE'].values[0]) > 7)
			instance = str(int(split_df["INSTANCE"].values.tolist()[1]))

			date_str = split_df["Date"].values.tolist()[1]
			name = self.instance_names.get(instance)
			k = result_dir+"\\" + fileN[:-4] + '_' +  name +".csv"
			split_df["Station"] = self.station_names.get(instance)
			split_df["Unit_Name"] = name
			#if split_df["Date"].values.tolist()[1] in df_result["Date"]:
				#print('aaaa')
			zero = np.array([0])
			if not "ALARM_01" in split_df.columns.values.tolist():
				split_df["ALARM_01"] = ''
			if not self.cols_to_fix == None:
				self.prepare_arr_of_cols(zero, self.cols_to_fix, split_df)
			if not self.temp_cols == None:
				split_df["Delta_T"] = self.delta_t(self.temp_cols, split_df)
			if not self.binary_cols == None:
				self.binary_col_array(self.binary_cols, split_df)
			#Deprecated date check
			date = self.get_file_date(split_df["Date"].values.tolist()[1])
			split_df["Month"] = date.strftime('%B')
			#start_date = parse('2019-7-8').date()
			split_df.to_csv(k, index = False)
		except Exception as e:
			if fileN == 'Rel_2019_8_10.csv':
				raise e
			print(fileN)
			pass
	def read_files(self, data_path, result_dir):
		#find min cols of thing
		min_cols = len(self.intended_cols)

		#find differences between directories
		file_names = self.find_different(data_path, result_dir)
		for fileN in file_names:
			#create df
			try:
				df = pd.read_csv(data_path + "\\" + fileN)      
			except Exception as e:
				continue

			
			cols = df.columns
			colnames = df.columns.values.tolist()
			last_col = colnames[-12]
			digits = re.findall("\d+", colnames[-2])
			if digits == [] or len(cols) == min_cols:
				if not (self.index_of_last_col == None):
					df = self.delete_cols(df)
				try:
					df.columns = self.intended_cols
					self.format_cols(cols, df, fileN, result_dir, data_path)
				except Exception as e:
					pass

			elif(self.check_if_multiple(df, digits[-1])):
				last_int = digits[-1]
				self.format_multiple_cols(df, fileN, result_dir, data_path, 1, last_int)