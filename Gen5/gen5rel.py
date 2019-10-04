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
			self.del_row_with_dashes(split_df)
			#print(int(split_df['INSTANCE'].values[0]) > 7)
			instance = str(i)
			for col in self.all_cols:
				if not col in split_df.columns.values.tolist():
					split_df[col] = np.nan
			split_df = split_df[self.all_cols].copy()
			print(i)
			date_str = split_df["Date"].values.tolist()[1]
			name = self.instance_names.get(instance)
			print()
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
			split_df.to_csv(k + date_str.replace('/','_') + ".csv")
		except Exception as e:
			if fileN == 'Rel_2019_8_10.csv':
				raise e
			print(fileN)
			pass
	def read_files(self, data_path, result_dir):
		#find min cols of thing
		min_cols = len(self.intended_cols)

		#find differences between directories
		fileN = data_path
		#create df
		if(fileN.endswith('csv')):
			try:
				df = pd.read_csv(fileN, low_memory = False) 
			 
				
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
			except:
				pass