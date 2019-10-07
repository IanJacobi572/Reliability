import os
import sys
sys.path.append(os.getcwd())
import Preprocessing as pr
import yaml
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
import os
import re
from datetime import datetime
from set_config import set_config
from ftplib import FTP
from num2words import num2words
import pandas as pd 
import numpy as np 
class Niagara_Field(pr.Preprocessing_Base):
	def __init__(self, **kwargs):
		super(Niagara_Field, self).__init__(**kwargs)
		self.flame_col = kwargs.get('flame_col')
		self.result_dir = kwargs.get('result_dir')
	def count_non_consec_flames(self, df):
		successful_ignitions = []
		cons = False
		for val in df[self.flame_col]:
			if(val == 'Flame Present'):
				if(cons == False):
					successful_ignitions.append('1')
					cons = True 
				else:
					successful_ignitions.append('0')
			else:
				successful_ignitions.append('0')
				cons = False
		return successful_ignitions
	def create_multiple_file(self, df, result_dir, fileN, i, intended_cols_i, data_path):
		try:
			split_df = df[intended_cols_i].copy()
			split_df.columns = self.intended_cols[:-1]
			self.del_row_with_dashes(split_df)
			zero = np.array([0])

			split_df["Current Cycles"] = 0
			split_df['Remaining Cycles'] = 0
			split_df['Expected Cycles Per Day'] = 0
			split_df['Completion Percent'] =0
			split_df["Week"] = 1
			split_df["Target For Week"] = 0
			est_date = datetime.now()
			split_df["Estimated Completion"] = est_date
			if not self.temp_cols == None:
			    split_df["Delta_T"] = self.delta_t(self.temp_cols, split_df)
			self.unit_name_multiple(data_path, split_df, i)
			self.binary_col_array(self.binary_cols, split_df)
			split_df["Cycles"] = self.count_non_consec_flames(split_df)
			split_df["Target Cycles"] = 0			
			split_df["Delta_T"] = self.delta_t(self.temp_cols, split_df)
			k = result_dir+"\\"+fileN[:-4] +"_" + str(i) +".csv"
			split_df.to_csv(k)
		except Exception as e:
			pass
	def unit_name_multiple(self, data_path, df, i):
		location = os.path.basename(os.path.normpath(data_path))
		name = location.split(" ")[0] + num2words(i)
		df["Unit_Name"] = name.upper()
		df["Station"] = name.upper()
		df["Group"] = "Field"
		df["Location"] = location.upper()
		df["Category"] = "Field"
	def unit_name_from_path(self, data_path, df):
		name = os.path.basename(os.path.normpath(data_path))
		name = name.split(" ")[0]
		df["Unit_Name"] = name.upper()
		df["Location"] = name.upper()
		df["Group"] = "Field"

		df["Station"] = name.upper()
		df["Category"] = "Field"
		if not self.temp_cols == None:
			df["Delta_T"] = self.delta_t(self.temp_cols, df)
#I should probably move this into my data files instead of the module since it is the main driving fnction
	def format_cols(self, cols, df, fileN, result_dir, data_path):
		if not self.alarm_name == None and alarm_name in df.columns:
			self.df_to_string(self.alarm_name, df)
		if df.shape[0] > 1: #Ignore changing the files with only one row
			cols = df.columns
			df = df.drop("SW_VERSN", axis=1)
			df["Current Cycles"] = 0
			df["Week"] = 1
			df["Average Cycles"] = 0

			df["Target For Week"] = 0
			df['Remaining Cycles'] = 0
			df['Expected Cycles Per Day'] = 0
			df['Completion Percent'] =0
			est_date = ''
			df["Estimated Completion"] = est_date
			#retrieve unit name
			if(self.from_path == True):
				self.unit_name_from_path(data_path, df)
			else:
				self.unit_name(df.columns, fileN, df)
			self.count_non_consec_flames(df)
			# Fix the Gallons Columns, Successful Ignitions, Failed Ignitions
			# ,Flame Failures, Burner Minutes
			zero = np.array([0])
			df["Cycles"] = self.count_non_consec_flames(df)
			df["Target Cycles"] = 0

			# Taking the Absolute Value of the both the Deviations for easy
			# analysis
			if not self.deviation_cols == None:
				self.take_abs_of_devs(df)
			if not self.binary_cols == None:
				self.binary_col_array(self.binary_cols, df)
			print(fileN, len(cols), cols[-1], cols[0])

		#Save only the files that contain info

			if not (df["Unit_Name"].values[0] == "OHIO"):
				self.create_file(result_dir, fileN, df)
		else:
			print("\n\n\n*******\n", fileN, " = not considered in analysis\n because it has only 1 line of data")
    #another main driving function of the module, meant to loop through the new files and process them
	def main(self, data_path):
		config_path = self.path + "/Config"
		login_path = config_path + "/login.yaml"
		path_path = config_path + "/path.yaml"
		self.read_files(data_path, self.result_dir)