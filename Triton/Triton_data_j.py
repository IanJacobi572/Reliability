import Preprocessing_Triton_2 as pr
import os
from ftplib import FTP
#ftp = FTP('ftp1.onerheem.com')
path = 'C:/Triton'
remote_path = '/InfinityFieldTest/DragonFieldTest'

del_cols = ("","CHANNEL5-1","CHANNEL6-1","CHANNEL7-1","CHANNEL1-2","CHANNEL2-2",
                "CHANNEL3-2","CHANNEL4-2","CHANNEL5-2","CHANNEL6-2","CHANNEL7-2", "CHANNEL2-1", "CHANNEL1-1","CHANNEL3-1","CHANNEL4-1")  
intended_cols = ("Time","Date","CHE_SIGN","CHE_FIGN","CHEFFAIL","CHE_HIOP","CHE_BMIN","GASVALVE","SW_VERSN","ALARMS","ALERTS","AND1POWR","AND2POWR","AND3POWR","ANODSTAT","AND1STAT","AND2STAT","AND3STAT","SW_VERSN.1")

expected_cols = ("Time", "Date", "CHE_SIGN", "CHE_FIGN", "CHEFFAIL", "CHE_HIOP","CHE_BMIN", "GASVALVE", "SW_VERSN", "ALARMS", "ALERTS", "AND1POWR", "AND2POWR", "AND3POWER", "ANODSTAT", "AN1DSTAT", "AND2STAT", "AND3STAT", "SW_VERSN" ,"","","","","","","","","","","","","","")
alarm_name = "ALARMS"
cols_to_fix = ("CHE_BMIN", "CHE_SIGN", "CHE_FIGN", "CHEFFAIL", "CHE_HIOP")
deviation_cols = ()
min_cols = len(intended_cols)
#dl = pr.from_ftp(path, remote_path, ftp)
#dl.ftp_sync()
data_path = "C:/Users/ian.jacobi/Documents/aaaa/Working Files/James Worthington"
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir() ]    
triton = pr.Preprocessing_Triton_2_files(path, alarm_name, del_cols, intended_cols, expected_cols, cols_to_fix, deviation_cols, min_cols)
#triton.toInt("AND3STAT")
for sub in subfolders:
	triton.main(sub, '/Preprocessing_Result_James')