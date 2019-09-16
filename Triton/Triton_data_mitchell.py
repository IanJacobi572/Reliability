import Preprocessing_m as pr
import os
from ftplib import FTP
#ftp = FTP('ftp1.onerheem.com')
path = 'C:/Triton'
remote_path = '/InfinityFieldTest/DragonFieldTest'

del_cols = ("","CHANNEL5-1","CHANNEL6-1","CHANNEL7-1","CHANNEL1-2","CHANNEL2-2",
                "CHANNEL3-2","CHANNEL4-2","CHANNEL5-2","CHANNEL6-2","CHANNEL7-2", "CHANNEL2-1", "CHANNEL1-1","CHANNEL3-1","CHANNEL4-1")  
intended_cols = ("Time","Date","PRODSERN","HEATCALL","TANKTEMP","FLUETEMP","INLTTEMP","VLVSTATE","FLAMECUR","FANSPEED","BLOWRPWM","S1_AIRFL","S2_INPRS","S3_EXPRS","S4_GLINE","AUXFSENS","SHUT1REQ","MODEL_ID","SHUTOPEN","SHUTCLOS","LEAKSENR","SW_VERSN")

expected_cols = ("Time", "Date", "CHE_SIGN", "CHE_FIGN", "CHEFFAIL", "CHE_HIOP","CHE_BMIN", "GASVALVE", "SW_VERSN", "ALARMS", "ALERTS", "AND1POWR", "AND2POWR", "AND3POWER", "ANODSTAT", "AN1DSTAT", "AND2STAT", "AND3STAT", "SW_VERSN" ,"","","","","","","","","","","","","","")
alarm_name = ""
cols_to_fix = ()
deviation_cols = ()
zero_strs = {
	'S1_AIRFL': 'Closed',
	'S2_INPRS':'Closed',
	'S3_EXPRS':'Closed',
	'S4_GLINE':'Closed'
}
one_strs = {
	'S1_AIRFL': 'Open',
	'S2_INPRS':'Open',
	'S3_EXPRS':'Open',
	'S4_GLINE':'Open'
}
vlvstate = "VLVSTATE"
binary_cols = ("S1_AIRFL","S2_INPRS","S3_EXPRS","FLAMECUR", "S4_GLINE")
min_cols = len(intended_cols)
#dl = pr.from_ftp(path, remote_path, ftp)
#dl.ftp_sync()
data_path = "C:/Users/ian.jacobi/Documents/aaaa/Working Files/Mitchell Naler"
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir() ]    
triton = pr.Preprocessing_Triton_1_files(from_path = True, path = path, zero_strs = zero_strs, one_strs = one_strs, del_cols = del_cols, intended_cols= intended_cols, cols_to_fix=cols_to_fix, vlvstate=vlvstate, binary_cols=binary_cols)
#triton.toInt("AND3STAT")
for sub_path in subfolders:
	triton.main(sub_path, '/Preprocessing_Result_Mitchell')
#for sub in subfolders:
	#triton.main(sub)