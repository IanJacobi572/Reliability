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
	#gets date from input date string 
	def get_file_date(self, date):
		date = parse(date)
		return date.date()
	#outpu and formatting function
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
			##print(intended_cols_i)
			intended_cols = ["Time", "Date"] + [col.rsplit('_',1)[0] for col in intended_cols_i[2:]]
			split_df = df[intended_cols_i].copy()
			split_df.columns = intended_cols
		self.del_row_with_dashes(split_df)
		if split_df.shape[0] >3 and i != 25:
				#print(int(split_df['INST
				try:
					instance = int(split_df["INSTANCE"].values.tolist()[-1])
					if not instance == int(split_df["INSTANCE"].values.tolist()[0]):
						df = df.drop([0])
						print("dropped" + fileN)
				except:
					instance = str(i)
				instance = str(instance)
				for col in self.all_cols:
					if not col in split_df.columns.values.tolist():
						split_df[col] = ' '
				split_df = split_df[self.all_cols].copy()
				#print(i)
				name = self.instance_names.get(instance)
				split_df['Unit_Name'] = name
				station = self.station_names.get(instance)
				split_df["Station"] = station
				if(name == None):
					print(instance,str(i))
				try:

					k = result_dir+"\\" + name + "_"+ station + '\\'
					if not os.path.exists(k):
						os.makedirs(k)
						#print(k)
					#if split_df["Date"].values.tolist()[1] in df_result["Date"]:
						#print('aaaa')
					zero = np.array([0])
					df.fillna('')
					if not self.binary_cols == None:
						self.binary_col_array(self.binary_cols, split_df)
					#Deprecated date check
					#print(date_str)
					date = self.get_file_date((split_df["Date"].values[-3]))
					date_str = date.strftime("%Y_%m_%d")

					split_df["Month"] = date.strftime('%B')
					#start_date = parse('2019-7-8').date()
					split_df.to_csv(k + date_str +".csv", index= False)
					print(station +' '+ date_str + ' Finished')
				except Exception as e:
					pass
	#reads input files 
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
			self.format_multiple_cols(df, fileN, result_dir, data_path, first_int, last_int)     
			
	def format_multiple_cols(self, df, fileN, result_dir, data_path, first_int, last_int):
	
		for i in range(int(first_int), int(last_int)+1):
			colnames = df.columns.values.tolist()
			intended_cols_i =['Time', 'Date'] + [col + "_" + str(i) for col in self.intended_cols[2:]]
			zero = np.array([0])
			self.create_multiple_file(df, result_dir, fileN, i, intended_cols_i, data_path)
	  