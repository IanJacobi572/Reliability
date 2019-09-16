import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
import Preprocessing_Niagara_Field as pr
import os
#lifetime_val_cols = ("IGN_FIGN", "IGN_FFLM", "WTR_USED", "GAS_KBTU")
binary_cols = ("FLM_ROD1", "FREEZING")
zero_vals = {
	"FLM_ROD1": "Flame Not Present",
	"FREEZING" : "Not Freezing"
}
one_vals = {
	"FLM_ROD1":"Flame Present",
	"FREEZING" :"Freezing"
}
intended_cols = ("Time","Date","TEMP__IN","TEMP_OUT","TEMPHTX1","TEMP_EXH","VOLU_CTL","FLOW_GPM","BYPRATIO","FAN__SPD","WTR_USED","GAS_KBTU","FLM_ROD1","RCIRPUMP","FREEZING","IGN_FIGN","IGN_FFLM","MANINCNM","TOTLFLOW","ALARM_01","SENSFFFB","SW_VERSN")

path = 'C:/Niagara'
data_path = 'C:/Niagara/FieldTest'
result_dir = 'c:/niagara/prp'
subfolders = [f.path for f in os.scandir(data_path) if f.is_dir() ]    
temp_cols = {
	"in": "TEMP__IN",
	"out": "TEMP_OUT"
}
niagara = pr.Niagara_Field(flame_col = 'FLM_ROD1',temp_cols = temp_cols, from_path = True, intended_cols = intended_cols, path = path, binary_cols = binary_cols, zero_strs = zero_vals, one_strs = one_vals)
for sub in subfolders:
	niagara.main(sub, result_dir)