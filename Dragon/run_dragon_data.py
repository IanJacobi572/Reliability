import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())
import dragon_prp as pr
from multiprocessing import Pool
import Preprocessing as prp
from functools import partial
from ftplib import FTP
ftp = FTP('ftp1.onerheem.com')
index_of_last_col = 27
path = 'C:/Dragon'
remote_path = '/InfinityFieldTest/DragonFieldTest'
resultdir = path + '/Preprocessing_Result'
data_path = 'C:/dragon/DragonFieldTest' 
#intended_cols = prp.find_intended_cols(data_path, path, index_of_last_col)
intended_cols = ["Time", "Date", "CHE_SIGN", "CHE_FIGN", "CHEFFAIL", "CHE_BMIN",
                 "CHE_GALS", "INLTTEMP", "FLOW_GPM", "TANKTEMP", "FLAMECUR", "FANSPEED",
                 "BLOWRPWM", "AND1POWR", "AND2POWR", "AND1CURR", "AND2CURR", "ALARMH01",
                 "ALARMS", "CHE_BPDV", "CHE_FCDV", "VLVSTATE", "SW_VERSN", "CHANNEL1-1",
                 "CHANNEL2-1", "CHANNEL3-1", "CHANNEL4-1"]
print(intended_cols[-4:])
alarm_name = "ALARMH01"
cols_to_fix = ("CHE_BMIN", "CHE_GALS", "CHE_SIGN", "CHE_FIGN", "CHEFFAIL")
deviation_cols = ("CHE_BPDV", "CHE_FCDV")
min_cols = 27

dragon = pr.Dragon(path = path, alarm_name = alarm_name, index_of_last_col = index_of_last_col, intended_cols = intended_cols,  cols_to_fix = cols_to_fix, deviation_cols = deviation_cols)
p = partial(dragon.main, result_dir = resultdir)
if __name__ == '__main__':
	dl = prp.from_ftp(str_date_start = '2019-6-1', path = path, remote_path=remote_path, ftp =ftp, start_str ="ICN")
	dl.ftp_sync()
	pool = Pool()
	files = [f.path for f in os.scandir(data_path)]
	print(files)
	pool.map(p, files)