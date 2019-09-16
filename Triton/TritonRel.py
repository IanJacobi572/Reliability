import Preprocessing as pr
import yaml
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
import os
from set_config import set_config
from ftplib import FTP
from num2words import num2words
import pandas as pd 
import numpy as np 
#import ipdb
def create_multiple_file(df, result_dir, fileN, i, intended_cols_i):
	empty = False
	split_df = df[intended_cols_i].copy()
	for col in split_df.values:
		if "---" in col:
			empty = True
	if not empty:
		k = result_dir+"\\"+fileN[:-4] +"_" + str(i) +".csv"
		split_df.to_csv(k)
	
def find_different(data_path, result_dir):
	already_processed = []    
	file_names = []
	##### Make sure to read only the csv files in directory
	with os.scandir(result_dir) as listOfEntries:
		for entry in listOfEntries:
			if entry.name[-5].isdigit():
				already_processed.append(entry.name[:-6] + ".csv")
			else : 
				already_processed.append(entry.name[:-5] + ".csv")
	with os.scandir(data_path) as listOfEntries:
		for entry in listOfEntries:
	# print all entries that are files
			if entry.is_file() and entry.name[-4:] == ".csv":
				file_names.append(entry.name)

	file_names = sorted(list(set(file_names) - set(already_processed)))
	return file_names
#when you have a manifold, consider them seperately, and split the file in hald
def format_multiple_cols(df, fileN, result_dir, data_path, i, last_col, intended_cols):
	intended_cols_i = ["Time", "Date"]
	for col in intended_cols[2:-1]:
		new_col_name = col + "_" + str(i)
		intended_cols_i.append(new_col_name)
		print(new_col_name)
	create_multiple_file(df, result_dir, fileN, i, intended_cols_i)
	if i < int(last_col[-1]):
		i+= 1
		format_multiple_cols(df, fileN, result_dir, data_path, i, last_col, intended_cols)
def read_files(data_path, result_dir, intended_cols):
	file_names = find_different(data_path, result_dir)
	for fileN in file_names:
	#create df
		try:
			df = pd.read_csv(data_path + "\\" + fileN, low_memory = False)      
		except Exception as e:
			continue


		cols = df.columns
		colnames = df.columns.values.tolist()


		last_col = colnames[-2]
		print( last_col)
		if(last_col[-1].isdigit()):
			if(int(last_col[-1]) > 1):
				format_multiple_cols(df, fileN, result_dir, data_path, 1, last_col, intended_cols)
			continue
	#ipdb.set_trace()
def main(path, data_path, result_dir, intended_cols):
	result_dir = path + result_dir
	if os.path.exists(result_dir) == False:
		os.mkdir(result_dir)
	read_files(data_path, result_dir, intended_cols)