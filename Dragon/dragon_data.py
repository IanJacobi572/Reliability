import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
import Preprocessing as pr

from ftplib import FTP
ftp = FTP('ftp1.onerheem.com')
index_of_last_col = 27
path = 'C:/Dragon'
remote_path = '/InfinityFieldTest/DragonFieldTest'
resultdir = path + '/Preprocessing_Result'
data_path = 'C:/dragon/DragonFieldTest'
del_cols = ("CHANNEL5-1","CHANNEL6-1","CHANNEL7-1","CHANNEL1-2","CHANNEL2-2",
                
            "CHANNEL3-2","CHANNEL4-2","CHANNEL5-2","CHANNEL6-2","CHANNEL7-2","del")  
intended_cols = pr.find_intended_cols(data_path, path, index_of_last_col)
expected_cols = ("Time", "Date", "CHE_SIGN", "CHE_FIGN", "CHEFFAIL", "CHE_BMIN",
                 "CHE_GALS", "INLTTEMP", "FLOW_GPM", "TANKTEMP", "FLAMECUR", "FANSPEED",
                 "BLOWRPWM", "AND1POWR", "AND2POWR", "AND1CURR", "AND2CURR", "ALARMH01",
                 "ALARMS", "CHE_BPDV", "CHE_FCDV", "VLVSTATE", "SW_VERSN", "CHANNEL1-1",
                 "CHANNEL2-1", "CHANNEL3-1", "CHANNEL4-1","CHANNEL5-1",
                 "CHANNEL6-1", "CHANNEL7-1", "CHANNEL1-2","CHANNEL2-2",
                 "CHANNEL3-2", "CHANNEL4-2", "CHANNEL5-2","CHANNEL6-2", "CHANNEL7-2") 
alarm_name = "ALARMH01"
cols_to_fix = ("CHE_BMIN", "CHE_GALS", "CHE_SIGN", "CHE_FIGN", "CHEFFAIL")
deviation_cols = ("CHE_BPDV", "CHE_FCDV")
min_cols = 27
dl = pr.from_ftp(str_date_start = '2019-6-1', path = path, remote_path=remote_path, ftp =ftp, start_str ="ICN")
dl.ftp_sync()
dragon = pr.Preprocessing_Base(path = path, alarm_name = alarm_name, index_of_last_col = index_of_last_col, intended_cols = intended_cols, expected_cols = expected_cols, cols_to_fix = cols_to_fix, deviation_cols = deviation_cols)
dragon.main(data_path, resultdir)