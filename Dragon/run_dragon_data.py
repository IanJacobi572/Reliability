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
category ={
	"ICN10235":"Reliability",
	"ICN10236":"Reliability",
	"ICN10244":"Reliability",
	"ICN10213":"Reliability",
	"ICN10221":"Reliability",
	"ICN10231":"Reliability",
	"ICN10228":"Reliability",
	"ICN10248":"Reliability",
	"ICN10224":"Field",
	"ICN10234":"Field",
	"ICN10219":"Field",
	"ICN10230":"Field",
	"ICN10220":"Field"
}

typos = {
  'ICN' : 'ICN10234',
  'ICN102221' : 'ICN10221',
	'ICN10228-1':'ICN10228',
	'ICN1024':'ICN10234'
}

rename_cols={
	"CHANNEL4-1": "Comb_Temp_OM(F)",
 	"CHANNEL3-1": "Outlet_Temp_OM(F)",
 	"CHANNEL2-1": "Inlet_Temp_OM(F)",
  	"CHANNEL1-1": "Flow_Rate_OM",
  	"VLVSTATE": "Valve_State" ,
  	"BLOWRPWM": "Blower_PWM",
  	"FANSPEED": "Fan_Speed",
  	"FLAMECUR": "Flame_Curr",
  	"TANKTEMP": "Tank_Temp",
  	"FLOW_GPM": "Flow_GPM",
    "CHE_SIGN": "Comb_Cycles",
  	"INLTTEMP": "Inlet_Temp"
}
 #"Split Column by Delimiter" 
city ={
    "ICN10213":"Nuevo Laredo",
    "ICN10219":"Montgomery",
    "ICN10220":"Montgomery",
    "ICN10221":"Nuevo Laredo",
    "ICN10224":"Atlanta",
    "ICN10228":"Nuevo Laredo",
    "ICN10230":"Chicago",
    "ICN10231":"Nuevo Laredo",
    "ICN10234":"Brampton",
    "ICN10235":"Nuevo Laredo",
    "ICN10236":"Atlanta",
    "ICN10244":"Nuevo Laredo",
    "ICN10248":"Montgomery"
}

short_desc={
    "T115":"Comb H Degrad",
    "T116":"Comb H Degrad",
    "T120":"Replace Neutralizer",
    "T021":"L_Tank Sen Short",
    "T113":"Rod Flame Degraded",
    "T114":"Rod Flame Degrad",
    "A030":"Lost Flame in Heat",
   	"T105":"W_Leak Sen no_install",
    "A029.":"Ignition Fail",
    "A104":"Water Leak",
    "A025":"No Blower Feedback",
    "T122":"Anode PWR Ctrl Fail",
}
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

dragon = pr.Dragon(typos = typos, category = category, rename_cols = rename_cols, short_desc = short_desc, city = city, path = path, alarm_name = alarm_name, index_of_last_col = index_of_last_col, intended_cols = intended_cols,  cols_to_fix = cols_to_fix, deviation_cols = deviation_cols)
p = partial(dragon.main, result_dir = resultdir)
if __name__ == '__main__':
	dl = prp.from_ftp(str_date_start = '2019-6-1', path = path, remote_path=remote_path, ftp =ftp, start_str ="ICN")
	dl.ftp_sync()
	pool = Pool()
	files = [f.path for f in os.scandir(data_path)]
	print(files)
	pool.map(p, files)