import os
import sys
sys.path.append(os.getcwd())
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
class Dragon(pr.Preprocessing_Base):
	def __init__(self, **kwargs):
		super(Dragon, self).__init__(**kwargs) 
		self.typos = kwargs.get('typos')
		self.type = kwargs.get('type')
		self.city = kwargs.get('city')
		self.category = kwargs.get('category')
		self.rename_cols = kwargs.get('rename_cols')
		self.short_desc = kwargs.get('short_desc')
	def unit_name(self, cols, file_n, df):
	# Add the Unit_Names for the file_name
		unitName = file_n.split("_")[0].split('\\')[-1]
		unitName = unitName.split('-')[0]
		if unitName in self.typos:
			unitName = self.typos.get(untiName)
		print(unitName)
		df["Unit_Name"] = unitName.upper()
	def split_alarms(self, df):
		groups = df.groupby('ALARMH01').groups
		df["Alarm Code"]=''
		df['Failed Attempts'] = 0
		df["Alarm Description"] = ''
		df["Short Description"]=''
		df["Alarm Time"]=''
		df["Alarm Date"]=''
		#
		for key in groups:
			idx = groups.get(key)[0]
			row = df.loc[idx].copy()
			alarm = row.ALARMH01            
			delim = ' '
			delimited = alarm.split(' ')
			#if delimited is more than one value
			if len(delimited) > 1:
				alarm_date = delimited[1]
				alarm_code = delimited[2] 
				alarm_time= parse(delimited[0]).time()
				if self.type == 'EB1':
					if alarm_code =='T105' or alarm_code=='T122':
						continue
				if(parse(row.Date.replace('/','-')) == parse(alarm_date.replace('/','-'))):
					long = delim.join(delimited[3:]).strip()
					#A029 indicates a failed attempt, rather than a regular alarm
					if alarm_code != "A029" :
						short = self.short_desc.get(alarm_code)
						row["Alarm Description"] = long
						row["Short Description"] = short
						row['Alarm Time'] = alarm_time
						row["Alarm Date"] = alarm_date
						row["Alarm Code"] = alarm_code
						df.loc[idx]=row
					else:
						df.loc[idx, 'Failed Attempts']=1

	def create_file(self, result_dir, fileN, df):
		resultFrame = df    
		if resultFrame.shape[0] > 0:
			name = df["Unit_Name"].values.tolist()[0]
			df.rename(columns=self.rename_cols, inplace = True)
			time =  pd.to_datetime(df["Time"])
			df['Hours']=time.dt.hour
			df["Heating"] = 0
			df.loc[df["CHE_BMIN"] == 1, "Heating"] = 1
			self.split_alarms(df)
			df["Location"] = self.city.get(name)
			df["Category"] = self.category.get(name)
			k = result_dir+"\\"+df['Unit_Name'].values.tolist()[0] +'_'+ df['Date'].values.tolist()[0].replace('/', '_') +"_.csv"
			resultFrame.to_csv(k)
	def read_files(self, data_path, result_dir):
		#find min cols of thing
		min_cols = len(self.intended_cols)
		#create df
		fileN = data_path
		try:
			if(fileN.endswith('csv')):
				df = pd.read_csv(fileN)    

				colnames = df.columns.values.tolist()
				last_col = colnames[-12]
				digits = re.findall("\d+", colnames[-2])
				print(digits)
				df = self.delete_cols(df)
				cols = df.columns
				print(len(cols))
				if len(cols) == 23:
					
					df.columns = self.intended_cols[:-4]
					for col in self.intended_cols[-4:]:
						print(col)
						df[col] = ''
					self.format_cols(cols, df, fileN, result_dir, data_path)
				elif len(cols) == 27:
					
					df.columns = self.intended_cols
					print(self.unit_name(cols, fileN, df))
					self.format_cols(cols, df, fileN, result_dir, data_path)
			#Checks if file records multiple unique units, if it does return true
		except Exception as e:
			pass
	def main(self, data_path, result_dir):
		self.read_files(data_path, result_dir)
