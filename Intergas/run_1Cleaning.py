import os
import datetime
import pandas as pd
import swifter

dir = r'C:\Users\anes.madani\Desktop\Anes\Intergas\raw'
res = 'C:/Intergas/preprocessed'

if not os.path.exists(res):
	os.makedirs(res)

pd.options.mode.chained_assignment = None

def clean(df):
    df.iloc[3,1:8] = df.iloc[2,1:8]
    df = df.iloc[3:]
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop([3,4], inplace=True)
    df.reset_index(drop=True, inplace=True)
    if type(df.TIME[0])==float:
        df.TIME = df.TIME.swifter.apply(lambda x: datetime.datetime.utcfromtimestamp((x - 25569) * 86400.0).strftime('%m/%d/%Y %I:%M:%S %p'))
    return df

for root, dirs, files in os.walk(dir):
    for f in files:
        '''if os.path.isfile(f):
            xls = pd.ExcelFile(f)
            df_unit = pd.read_csv(f)
            df = pd.read_excel(xls, usecols='A:L', index_col=None)
            df = pd.concat([df,df_unit], sort=False, ignore_index = True)
            df.to_csv(result_dir + '\\' + f + '.csv', index=False)
        else:'''
        print(f)
        #xls = pd.ExcelFile(dir+'\\'+f)
        df = pd.read_excel(dir+'\\'+f, usecols='A:L', index_col=None)
        df = clean(df)
        df.to_csv(res + '\\' + f + '.csv', index=False)