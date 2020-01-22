import pandas as pd
import os

dir = r'C:\Users\anes.madani\Desktop\Anes\Odin Field\raw'
result_dir = r'C:\Users\anes.madani\Desktop\Anes\Odin Field\preprocessed'

for fileName in os.listdir(dir):
    print('File name:', fileName)
    
    df = pd.read_csv(os.path.join(dir, fileName), error_bad_lines=False)
    
    if 'ALARM_01' in df.columns:
        try:
            df = df[['timestamp', 'DISCTEMP', 'POWRWATT', 'COMP_RLY', 'FAN_CTRL', 'AMBIENTT', 'EVAPTEMP', 'EXACTUAL', 'SUCTIONT', 'ALARM_01', 
            'ALRMALRT', 'HEATCTRL', 'HOTWATER', 'UPHTRTMP', 'WHTRCNFG', 'WHTRSETP', 'LOHTRTMP', 'SHUTOFFV', 'WHTRMODE', 'HRSHIFAN', 'HRSLOFAN', 
            'HRSLOHTR', 'HRSUPHTR', 'HRS_COMP', 'SHUTCLOS', 'SHUTOPEN', 'SERIAL_N', 'UNITTYPE']].copy()
            df.to_csv(result_dir + '\\' + fileName, index = False)
        except:
            print(fileName + 'passed1')
            pass
    else:
        try:
            df = df[['timestamp', 'DISCTEMP', 'POWRWATT', 'COMP_RLY', 'FAN_CTRL', 'AMBIENTT', 'EVAPTEMP', 'EXACTUAL', 'SUCTIONT', 'ALRMALRT', 
            'HEATCTRL', 'HOTWATER', 'UPHTRTMP', 'WHTRCNFG', 'WHTRSETP', 'LOHTRTMP', 'SHUTOFFV', 'WHTRMODE', 'HRSHIFAN', 
            'HRSLOFAN', 'HRSLOHTR', 'HRSUPHTR', 'HRS_COMP', 'SHUTCLOS', 'SHUTOPEN', 'SERIAL_N', 'UNITTYPE']].copy()
            df.to_csv(result_dir + '\\' + fileName, index = False)
        except:
            print(fileName + 'passed2')
            pass