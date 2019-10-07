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
	def create_file(self, result_dir, fileN, df):
		resultFrame = df    
		if resultFrame.shape[0] > 0:
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
