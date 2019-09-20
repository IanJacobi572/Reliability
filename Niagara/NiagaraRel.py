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
			date = self.get_file_date(split_df["Date"].values.tolist()[1])
			split_df["Month"] = date.strftime('%B')
			split_df = split_df.rename(columns = {"INSTANCE": "Unit_Name"})
			self.df_to_string("Unit_Name", split_df)
			split_df["Unit_Name"].replace(self.instance_names, inplace = True)
			station = self.station_names.get(str(i))
			split_df["Station"] = station
			group = self.groups.get(str(i))
			split_df["Group"] = group
			split_df["Target Cycles"] = self.target_cycles.get(group)
			self.binary_to_string(self.flame_col, split_df)
			split_df["Location"] = "Nuevo Laredo"
			split_df["Category"] = "Reliability"

			split_df["Successful_Ignitions"] = self.count_non_consec_flames(split_df)
			a = (parse('2019-8-20'))
			a = a.date()
			print(date)
			print(a)
			if date == parse('2019-8-20').date():
				split_df["Successful_Ignitions"].values[0] = int(split_df["Successful_Ignitions"].values[0]) + self.diff_cycles.get(station)
				print(self.diff_cycles.get(station))
			#print(split_df['Unit_Name'].values[1])
			split_df["Delta_T"] = self.delta_t(self.temp_cols, split_df)

			k = result_dir+"\\"+fileN[:-4] +"_" + self.instance_names.get(str(i)) +".csv"
			split_df.to_csv(k)
		except Exception as e:
			pass
	def find_different(self, data_path, result_dir):
		already_processed = []    
		file_names = []
		##### Make sure to read only the csv files in directory
		#with os.scandir(result_dir) as listOfEntries:
			#for entry in listOfEntries:
				#if entry.name[-12].isdigit():
					#already_processed.append(entry.name[:-6] + ".csv")
				#else : 
					#already_processed.append(entry.name[:-5] + ".csv")
		with os.scandir(data_path) as listOfEntries:
			for entry in listOfEntries:
		# print all entries that are files
				file_names.append(entry.name)

		file_names = sorted(list(set(file_names) - set(already_processed)))
		return file_names
	#when you have a manifold, consider them seperately, and split the file in hald
	def format_multiple_cols(self, df, fileN, result_dir, data_path, i, last_dig):
		intended_cols_i = ["Time", "Date"]
		intended_cols_i = intended_cols_i + [col + "_" + str(i) for col in self.intended_cols[2:]]
		print(intended_cols_i)
		self.create_multiple_file(df, result_dir, fileN, i, intended_cols_i)
		if i < last_dig:
			i+= 1
			self.format_multiple_cols(df, fileN, result_dir, data_path, i, last_dig)
	def read_files(self, data_path, result_dir):
		file_names = self.find_different(data_path, result_dir)
		for fileN in file_names:
		#create df
			try:
				df = pd.read_csv(data_path + "\\" + fileN, low_memory = False)      
			except Exception as e:
				continue


			cols = df.columns
			colnames = df.columns.values.tolist()

			digits = re.findall("\d+", colnames[-2])
			if(int(digits[-1]) > 1):
				self.format_multiple_cols(df, fileN, result_dir, data_path, 1, int(digits[-1]))
		#ipdb.set_trace()
	def main(self, data_path, result_dir):
		self.read_files(data_path, result_dir)