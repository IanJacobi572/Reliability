
import Preprocessing as pr
import yaml
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
import os
import re
from datetime import datetime

from dateutil.parser import *

from set_config import set_config
from ftplib import FTP
from num2words import num2words
import pandas as pd 
import numpy as np 
class Niagara_Reliability(pr.Preprocessing_Base):
	def __init__(self, **kwargs):
		super(Niagara_Reliability, self).__init__(**kwargs)
		self.flame_col = kwargs.get('flame_col')
		self.station_names = kwargs.get('station_names')
		self.diff_cycles = kwargs.get('diff_cycles')
		self.target_cycles = kwargs.get('target_cycles')
		self.groups = kwargs.get('groups')
		self.start_weeks = kwargs.get('start_dates')
		self.cycles_per_day_per_group = kwargs.get('cycles_per_day_group')
		self.instance_names = kwargs.get('instance_names')
	#import ipdb
	def get_file_date(self, date):
		date = parse(date)
		return date.date() 
	def count_non_consec_flames(self, df):
		sucsesful_ignitions = []
		cons = False

		for val in df[self.flame_col]:
			if(val == 'Flame Present'):
				if(cons == False):
					sucsesful_ignitions.append('1')
					cons = True 
				else:
					sucsesful_ignitions.append('0')
			else:
				sucsesful_ignitions.append('0')
				cons = False
		return sucsesful_ignitions

	def create_multiple_file(self, df, result_dir, fileN, i, intended_cols_i):
		empty = False
		try:
			print(fileN)
			try:
				split_df = df[intended_cols_i].copy()
			except Exception as e:
				intended_cols_1_june = ["Time","Date","TEMP__IN_1","TEMP_OUT_1","TEMPHTX1_1","TEMP_EXH_1","VOLU_CTL_1","FLOW_GPM_1","BYPRATIO_1","FAN__SPD_1","FLM_ROD1_1","ALARM_01_1"]
				intended_cols_i = [re.sub('1$', str(i), col) for col in intended_cols_1_june]
				
				split_df = df[intended_cols_i].copy()
			self.del_row_with_dashes(split_df)
			print(intended_cols_i)
			split_df.columns = intended_cols_i[:2] + [re.sub(r'_?[^A-Z_]+$', "", col) for col in intended_cols_i[2:]]
			
			split_df["INSTANCE"] = i
			for col in self.intended_cols:
				if not col in split_df.columns.values.tolist():
					split_df[col] = ''
			split_df = split_df[self.intended_cols].copy()
			date = self.get_file_date(split_df["Date"].values.tolist()[-1])
			print(i)
			print(date)
			split_df["Month"] = date.strftime('%B')
			split_df['Unit_Name'] = self.instance_names.get(str(i))
			station = self.station_names.get(str(i))
			split_df["Station"] = station
			group = self.groups.get(str(i))
			week =date.isocalendar()[1] - self.start_weeks.get(station)
			split_df["Group"] = group
			target = self.target_cycles.get(group)
			target_for_week = self.cycles_per_day_per_group.get(group) * 7 * week
			split_df["Target Cycles"] = target
			split_df["Target Cycles of Week"] = target_for_week
			self.binary_to_string(self.flame_col, split_df)
			split_df["Location"] = "Nuevo Laredo"
			split_df["Category"] = "Reliability"
			split_df["Cycles"] = self.count_non_consec_flames(split_df)
			split_df["Week"] =  week
			#print(split_df['Unit_Name'].values[1])
			split_df["Delta_T"] = self.delta_t(self.temp_cols, split_df)
			k = result_dir+"\\"+ self.instance_names.get(str(i))
			if not os.path.exists(k):
				os.mkdir(k)
			split_df.to_csv(k+'/'+date.strftime('%Y-%m-%d')+'.csv', index = False)
												
		except Exception as e:
			pass
	def get_date_from_name(self, name):
		split = name.split("_")
		day = split[-1][:-4]
		print(split)
		date = parse(split[-3] + "-" + split[-2] + "-" + day)
		return date.date() 
	def find_different(self, data_path, result_dir):
		already_processed = []    
		file_names = []
		file_dates = []
		with os.scandir(data_path) as listOfEntries:
			for entry in listOfEntries:
				if entry.name.endswith('.csv'):
					file_names.append(entry.name)
					file_dates.append(self.get_date_from_name(entry.name))

		file_names = [x for _,x in sorted(zip(file_dates, file_names))]
		print(file_names)
		return file_names
	#when you have a manifold, consider them seperately, and split the file in hald
	def format_multiple_cols(self, df, fileN, result_dir, data_path, i, last_dig):
		for i in range(1, int(last_dig)+1):
			intended_cols_i = ["Time", "Date"]
			intended_cols_i = intended_cols_i + [col + "_" + str(i) for col in self.intended_cols[2:]]
			print(intended_cols_i)
			name = self.instance_names.get(str(i))
			
			self.create_multiple_file( df, result_dir, fileN, i, intended_cols_i )
	def read_files(self, data_path, result_dir):
		fileN = data_path
		if fileN.endswith('.csv'):
			df = pd.read_csv(data_path, low_memory = False)

			cols = df.columns
			colnames = df.columns.values.tolist()

			digits = re.findall("\d+", colnames[-2])
			if(int(digits[-1]) > 1):
				self.format_multiple_cols(df, fileN, result_dir, data_path, 1, int(digits[-1]))
		#ipdb.set_trace()
	def main(self, data_path, result_dir):
		self.read_files(data_path, result_dir)


