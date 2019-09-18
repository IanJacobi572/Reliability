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
			print(split_df.columns)
			split_df.columns = self.intended_cols[:-1]
			self.del_row_with_dashes(split_df)
			#print(int(split_df['INSTANCE'].values[0]) > 7)
			instance = str(int(split_df["INSTANCE"].values.tolist()[1]))

			name = self.instance_names.get(instance)
			split_df["Station"] = self.station_names.get(instance)
			split_df["Unit_Name"] = name
			print(split_df['Unit_Name'])
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
			#date = self.get_file_date(split_df["Date"].values.tolist()[1])
			#start_date = parse('2019-7-8').date()
			k = result_dir+"\\" + name +".csv"
			split_df.to_csv(k, mode = 'a')
		except Exception as e:
			print(fileN)
			pass