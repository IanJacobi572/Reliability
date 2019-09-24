import yaml
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
import os
import re
from datetime import datetime
from set_config import set_config
from ftplib import FTP
import pandas as pd 
from dateutil.parser import *
from num2words import num2words
import numpy as np 
from collections import OrderedDict
#class Preprocessing
    # unit name extraction
def find_intended_cols_multiple_file(data_path, path):
    col_path = path + '/config/cols.yaml'
    with os.scandir(data_path) as list_of_entries:
        print(list_of_entries)
        for entry in list_of_entries:
            if(entry.name.endswith('.csv')):
                df = pd.read_csv(data_path + '/' + entry.name)
                intended_cols  = df.columns.values.tolist()[:2] + [re.sub(r'_?[^A-Z_]+$', "", col) for col in df.columns.values.tolist()[2:]]
                intended_cols_no_dupes = list(OrderedDict.fromkeys(intended_cols))
                print(intended_cols_no_dupes)
                print(entry.name)
                if(intended_cols_no_dupes[0] == 'Time'):
                    return intended_cols_no_dupes

def find_intended_cols(data_path, path, index_of_last_col):
#if yaml doesnt exist discern intended cols from headers of a random csv
    col_path = path + '/config/cols.yaml'
    with os.scandir(data_path) as list_of_entries:
        for entry in list_of_entries:
            if(entry.name.endswith('.csv')):
                df = pd.read_csv(data_path + '/' + entry.name)
                df = df.iloc[:,:index_of_last_col]
                if(df.columns[0] == 'Time'):
                    return df.columns.values.tolist()
class from_ftp:
#retreive files from ftp server, with login, adress, and path from yaml file
    path = ""
    login_path = ""
    remote_path = ""
    path_path = ""
    def __init__(self, **kwargs):
        self.start_str = kwargs.get('start_str')
        self.path = kwargs.get('path')
        self.str_date_start = kwargs.get('str_date_start')
        self.ftp = kwargs.get("ftp")
        self.remote_path = kwargs.get("remote_path")
        if not (os.path.exists(self.path)):
            os.mkdir(self.path)
        config_path = self.path + "/Config"
        if not(os.path.exists(config_path)):
            config = set_config(config_path)
            config.setup()
        self.login_path = config_path + "/login.yaml"
        self.data_path = kwargs.get('data_path')
        self.path_path = config_path + "/path.yaml"
    #checks: file type, whether the file has the right start, and if it isnt from today
    def get_file_date(self, name):
        split = name.split("_")
        day = split[-1][:-4]
        date = parse(split[-3] + "-" + split[-2] + "-" + day)
        return date.date() 
    def filter_remote_files(self):
        relevant_files = []
        #date_start = datetime.now().date()
        now = datetime.now().date()
        #if self.str_date_start != None:
        date_start = parse(self.str_date_start).date()
        #else:
            #data_start = parse('2017-1-1').date()
        for name in self.ftp.nlst():
            if(name.startswith(self.start_str)):
                file_date = self.get_file_date(name)
                if(file_date < now and file_date >= date_start ):
                    relevant_files.append(name)
        return relevant_files
    #retrieves the files from remote server
    def retrieve_files(self):
        if(self.data_path == None):
            with open(self.path_path, 'r') as stream:
                data_dict = yaml.safe_load(stream)
            data_path = data_dict.get('File')
        else:
            data_path = self.data_path
        data_path_files = []
        h_remote_files = []

        
       
        print('BUILDING LOCAL DIR FILE LIST...')
        for file_name in os.listdir(data_path):
            data_path_files.append(file_name) # populate local dir list
        cmdcmd = 'CWD ' + self.remote_path
        self.ftp.sendcmd(cmdcmd)
        print('BUILDING REMOTE DIR FILE LIST...\n')
        h_remote_files = self.filter_remote_files()

        h_diff = sorted(list(set(h_remote_files) - set(data_path_files))) # difference between two lists

        for h in h_diff:
            with open(os.path.join(data_path,h), 'wb') as ftpfile:
                s = '0'
                print('File: ' + h)
                s = self.ftp.retrbinary('RETR ' + h, lambda d: ftpfile.write(d)) # retrieve file
                if str(s).startswith('226'): # comes from ftp status: '226 Transfer complete.'
                    print ('\nOK\n') # print 'OK' if transfer was successful
                else:
                    print (s) # if error, print retrbinary's return
    #try to login with current user info
    #try to login with current user info
    def try_login(self, username, password):
        print("Trying to login...") 
        print (username)
        try:
            self.ftp.login(username, password)
        except Exception as e:
            messagebox.showinfo("-- ERROR --", "Please enter valid infomation!", icon="warning")
    #enter user info from yaml file

    #main function, establishes shared variables, and makes sure the program can run, and all config is setup
    def ftp_sync(self):

        username = "" #mutable variable for username
        password = ""#mutable var for pwd
        with open(self.login_path, 'r') as stream:
            login_info = yaml.safe_load(stream)
            username = login_info.get("Username")
            password = login_info.get("Password")
            print(username)
        self.try_login(username, password)
        #if login is sucsessful retrieve files
        self.retrieve_files()
class Preprocessing_Base:
    # path, alarm_name, del_cols, intended_cols, expected_cols, cols_to_fix, deviation_cols, min_cols
    def __init__(self,**kwargs):
        self.path = kwargs.get('path') 
        self.from_path = kwargs.get('from_path')
        self.alarm_name = kwargs.get('alarm_name')
        self.del_cols = kwargs.get('del_cols')
        self.cols_to_fix = kwargs.get('cols_to_fix')
        self.intended_cols = kwargs.get('intended_cols')
        self.index_of_last_col = kwargs.get('index_of_last_col')
        self.deviation_cols = kwargs.get('deviation_cols')
        self.one_strs = kwargs.get("one_strs")
        self.temp_cols = kwargs.get("temp_cols")
        self.zero_strs = kwargs.get("zero_strs")
        self.binary_cols = kwargs.get("binary_cols")
    #derives unit_name from filename
   #main main driving function, starts the other two
    def main(self, data_path, result_dir):
        config_path = self.path + "/Config"
        login_path = config_path + "/login.yaml"
        path_path = config_path + "/path.yaml"
        self.read_files(data_path, result_dir)
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
            print(digits)
            if digits == [] or len(cols) == min_cols:
                if not (self.index_of_last_col == None):
                    df = self.delete_cols(df)
                print(fileN)
                try:
                    df.columns = self.intended_cols
                   # self.format_cols(cols, df, fileN, result_dir, data_path)
                except Exception as e:
                    pass

            elif(self.check_if_multiple(df, digits[-1])):
                last_int = digits[-1]
                self.format_multiple_cols(df, fileN, result_dir, data_path, 1, last_int)
        #Checks if file records multiple unique units, if it does return true
    def check_if_multiple(self, df, last_int):
        if(last_int.isdigit()):
            if(int(last_int) > 1):
                return True
    def format_multiple_cols(self, df, fileN, result_dir, data_path, i, last_int):
        for i in range(1, int(last_int)+1):
            colnames = df.columns.values.tolist()
            intended_cols_i =['Time', 'Date'] + [col + "_" + str(i) for col in self.intended_cols[2:-1]]

            #if not self.binary_cols == None:
            #intended_cols_i.append("SW_VERSN")
            #df.columns = intended_cols_i
            zero = np.array([0])
            #self.df_to_string(alarm_i, df)
            self.unit_name_multiple(data_path, df, i)
            self.create_multiple_file(df, result_dir, fileN, i, intended_cols_i, data_path)
      
    #I should probably move this into my data files instead of the module since it is the main driving fnction
    def format_cols(self, cols, df, fileN, result_dir, data_path):
        if not self.alarm_name == None:
            self.df_to_string(self.alarm_name, df)
        if df.shape[0] > 1: #Ignore changing the files with only one row
            cols = df.columns
            #retrieve unit name
            if(self.from_path == True):
                self.unit_name_from_path(data_path, df)
            else:
                self.unit_name(df.columns, fileN, df)

            # Fix the Gallons Columns, Successful Ignitions, Failed Ignitions
            # ,Flame Failures, Burner Minutes
            zero = np.array([0])
            print(fileN)
            self.prepare_arr_of_cols(zero, self.cols_to_fix, df)
            # Taking the Absolute Value of the both the Deviations for easy
            # analysis
            if not self.deviation_cols == None:
                self.take_abs_of_devs(df)
            if not self.binary_cols == None:
                self.binary_col_array(self.binary_cols, df)
            print(fileN, len(cols), cols[-1], cols[0])

            #Save only the files that contain info
            self.create_file(result_dir, fileN, df)
        else:
            print("\n\n\n*******\n", fileN, " = not considered in analysis\n because it has only 1 line of data")
    #creates seperate file from parent file with multiple different units(Reliability econet or manifold)
    def create_multiple_file(self, df, result_dir, fileN, i, intended_cols_i, data_path):
        try:
            split_df = df[intended_cols_i].copy()

            split_df.columns = self.intended_cols[:-1]
            self.del_row_with_dashes(split_df)
            #print(int(split_df['INSTANCE'].values[0]) > 7)
            zero = np.array([0])
            if not self.cols_to_fix == None:
                self.prepare_arr_of_cols(zero, self.cols_to_fix, split_df)
            if not self.temp_cols == None:
                split_df["Delta_T"] = self.delta_t(self.temp_cols, split_df)
            self.unit_name_multiple(data_path, split_df, i)
            if not self.binary_cols == None:
                self.binary_col_array(self.binary_cols, split_df)
            k = result_dir+"\\"+fileN[:-4] +"_" + str(i) +".csv"
            split_df.to_csv(k)
        except Exception as e:
            pass
    def unit_name(self, cols, file_n, df):
        if len(cols) == len(self.intended_cols):
            # Add the Unit_Names for the file_names
            unitName = file_n.split("_")[0]
            df["Unit_Name"] = unitName.upper()
        else:
            df = df.drop(df.columns[len(self.intended_cols):],axis=1)
            # Add the Unit_Names for the file_names
            unitName = file_n.split("_")[0]
            df["Unit_Name"] = unitName.upper()
        return unitName
        #//
    #sets values to string for entire column
    def df_to_string(self, column, df):
        #alarm strin
        df[column] = df[column].astype(str)
        #/
    #changes zeroes and ones to zerostr and onestr
    def binary_to_string(self, binary_col, df):
        
        if(binary_col in df.columns):
            self.df_to_string(binary_col, df)
            print(binary_col)
            if(binary_col[-2] == '_'):
                key_col = binary_col[:-2]
            else: 
                key_col = binary_col
            n = []
            for val in df[binary_col].values:
                if(val == '1'):
                    n.append(self.one_strs.get(key_col))
                elif(val == '0'):
                    n.append(self.zero_strs.get(key_col))
                elif(val == '' or val == None):
                    n.append('')
                else: 
                    n = df[binary_col]
                    break
            df[binary_col] = pd.DataFrame(n)
    #call binary to string for each col in binary cols
    def binary_col_array(self, binary_cols, df):
        for binary_col in binary_cols:
            self.binary_to_string(binary_col, df)
    #newer more useless-to-be-a-function delete cols function
    def delete_cols(self, df):
        return df.iloc[:,:self.index_of_last_col]
       #print(thisCol + "dropped")
        #/ abs value of deviations basically useless and shouldnt be in base but I dont want to restructure so here it stays
    def take_abs_of_devs(self, df):
        for dev_col in self.deviation_cols:
            df[dev_col] = pd.DataFrame(np.absolute(df[dev_col].values))
        #*/
    #creates file based on cleaned up frame
    def create_file(self, result_dir, fileN, df):
        resultFrame = df    
        if resultFrame.shape[0] > 0:
            k = result_dir+"\\"+fileN[:-4] +"_.csv"
            resultFrame.to_csv(k)
    #prepares lifetime value columns, but I didnt really understand that when I wrote it
    def prepare_col(self, name, zero, df):
        if(name in df.columns):
            if df[name].dtype == "int64" or df[name].dtype == "Float64":
                n = np.ediff1d(df[name].values)
                n = np.append(zero, n)
                n = n.clip(min=0)

                df[name] = pd.DataFrame(n)                
            elif df[name].values[0].isdigit():
                name_int = [int(x) for x in df[name].values]
                n = np.ediff1d(name_int)
                n = np.append(zero, n)
                n = n.clip(min=0)

                df[name] = pd.DataFrame(n)
    #prepares an array of lifetime value cols
    def prepare_arr_of_cols(self, zero, cols_to_fix, df):
        for col in cols_to_fix:
            self.prepare_col(col, zero, df)
    #finds files that are different between result dir and data directory, 
    #deprecated due to the amount of stuff that currently has multiple files with same name
    def find_different(self, data_path, result_dir):
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

        file_names = sorted(list(set(file_names)))
        return file_names
    #finds chang in temp from temp cols
    def delta_t(self, temp_cols, df):
        df[temp_cols["out"]] = df[temp_cols["out"]].astype(float)
        df[temp_cols["in"]] = df[temp_cols["in"]].astype(float)

        return(df[temp_cols["out"]] - df[temp_cols["in"]])
    #names a multiple unit NAMEONE and NAMETWO post split
    def unit_name_multiple(self, data_path, df, i):
        location = os.path.basename(os.path.normpath(data_path))
        name = location.split(" ")[0] + num2words(i)
    #parses unit name from data path, instead of file name
    def unit_name_from_path(self, data_path, df):
        name = os.path.basename(os.path.normpath(data_path))
        name = name.split(" ")[0]
        if not self.temp_cols == None:
            df["Delta_T"] = self.delta_t(self.temp_cols, df)

    #deletes any rows with dashes, after seperating files
    def del_row_with_dashes(self, df):
        for col in df.columns[2:]:
            df.drop(df.loc[df[col] == '---'].index, inplace =True)
   
    
    #meant to format multiple cols but would probably just end up being overwritten every single module so its abstract
   
    #another main driving function of the module, meant to loop through the new files and process them
    
   
            #ipdb.set_trace()
    
