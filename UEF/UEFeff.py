import pandas as pd
import os
import numpy as np
from math import isclose

def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    try: 
        if isclose(array[idx], value, abs_tol=1):
            return idx
    except:
        pass
    return idx-1

def effCalc(dfC, dfE, dfV):

    xls = pd.ExcelFile('UEF analysis.xlsx')
    dfZ = pd.read_excel(xls, 'Sheet3', skiprows=6, index_col=None, usecols = 'A,B,D', names = ['T','Cp','Density'])

    idxOfFirstDraw = dfE.loc[dfE['Desc'].str.contains('Starting Draw # 1 '), 'Unnamed: 0'].values
    cutOne = cutTwo = 0
    for i in dfE['Unnamed: 0']:
        cut = dfE['Desc'].loc[dfE['Unnamed: 0']==i].values
        if 'Cut OUT' in cut[0] and cutOne==0:
            cutOne = dfE['TimeStamp'].loc[dfE['Unnamed: 0']==i].values
            cutOne = cutOne[0]
        elif 'Cut OUT' in cut[0] and i>idxOfFirstDraw[0]:
            cutTwo = dfE['TimeStamp'].loc[dfE['Unnamed: 0']==i].values
            cutTwo = cutTwo[0]
            break
    idxOne = find_nearest(dfC['TimeStamp (sec)'].values, cutOne)
    idxTwo = find_nearest(dfC['TimeStamp (sec)'].values, cutTwo)
        
        
    GasPressure = float(dfV.loc[dfV['Variable'].str.contains('Gas Pressure'), 'Value'].values)
    dfC.loc[0, 'Gas Pressure'] = GasPressure
    Barometer = max(dfC.loc[idxOne:idxTwo, 'Barometer'])
    GasTemp = max(dfC.loc[idxOne:idxTwo, 'Gas TC'])
    Correction_fact = (GasPressure*0.0735+Barometer)*520/(30*(460+GasTemp))
    dfC.loc[0, 'Correction Factor (1)'] = Correction_fact
        
        
    HHV = float(dfV.loc[dfV['Variable'].str.contains('HHV'), 'Value'].values)
    dfC.loc[0, 'High Heating Value'] = HHV
    GasConsumption = max(dfC.loc[idxOne:idxTwo, 'Gas ascf'])
    PowerConsumption = max(dfC.loc[idxOne:idxTwo, 'WattHrs'])
    Qr = GasConsumption*HHV*Correction_fact + PowerConsumption*3.412
    dfC.loc[0, 'Qr'] = Qr
        
        
    dfC['M'] = 0
    for idx in range(1,dfC.shape[0]):
        AvgTmp = round((dfC.loc[idx, 'Tin'] + dfC.loc[idx, 'Tout'])/2,1)
        density = dfZ.loc[dfZ['T']==AvgTmp, 'Density'].values[0]
        dfC.loc[idx, 'M'] = (dfC.loc[idx, 'Drawn Water (Gallons)']-dfC.loc[idx-1, 'Drawn Water (Gallons)'])*density
    

    xls = pd.ExcelFile('UEF analysis.xlsx')
    dfZ = pd.read_excel(xls, 'Sheet3', skiprows=6, index_col=None, usecols = 'A,B', names = ['T','Cp'])

    startDraw = dfE.loc[dfE['Desc'].str.contains('Starting Draw # 1 '), 'TimeStamp'].values
    endDraw = dfE.loc[dfE['Desc'].str.contains('Draw Complete'), 'TimeStamp'].values

    startDrawIdx = find_nearest(dfC['TimeStamp (sec)'].values, startDraw[0])
    endDrawIdx = find_nearest(dfC['TimeStamp (sec)'].values, endDraw[0])

    M1 = (dfC.loc[startDrawIdx:endDrawIdx, 'M']).sum()
    Tout1 = dfC.loc[startDrawIdx:endDrawIdx, 'Tout'].mean()
    Tin1 = dfC.loc[startDrawIdx:endDrawIdx, 'Tin'].mean()
    AvgTmp = round((Tout1+Tin1)/2,1)
    Cp1 = dfZ.loc[dfZ['T']==AvgTmp, 'Cp'].values[0]
    Tdelta1 = Tout1-Tin1
    dfC.loc[0,'M1']=M1    
    dfC.loc[0,'Cp1']=Cp1
    dfC.loc[0,'Tdelta1']=Tdelta1
    Recovery_eff = M1*Cp1*Tdelta1/Qr
    dfC.loc[0,'Recovery Efficiency']=Recovery_eff

        
    M=dict()
    Cp=dict()
    Tout=dict()
    Tin=dict()

    for idx in range(0, len(dfC.Draw)):
        if dfC.loc[idx, 'Draw']!=0:
            key = int(dfC.loc[idx, 'Draw'])
            M.setdefault(key,[]).append(dfC.loc[idx, 'M'])
            Cp.setdefault(key,[]).append(dfC.loc[idx, 'Drawn Water (Gallons)'])
            Tout.setdefault(key,[]).append(dfC.loc[idx, 'Tout'])
            Tin.setdefault(key,[]).append(dfC.loc[idx, 'Tin'])
        
      
    Mii=dict()
    Cpii=dict()
    Tdeltaii=dict()
    Qhwii=dict()
    Qhw67ii=dict()
    Qhwdii=dict()
            
    Qhw=0
    Qhw67=0

    for i in range(1,15):
        Mi = sum(M[i])
        AvgTmp = round((((sum(Tout[i])/len(Tout[i]))+(sum(Tin[i])/len(Tin[i]))))/2,1)
        Cpi = dfZ.loc[dfZ['T']==AvgTmp, 'Cp'].values[0]
        Tdeltai = ((sum(Tout[i])/len(Tout[i]))-(sum(Tin[i])/len(Tin[i])))
        Qhwi = Mi*Cpi*Tdeltai/Recovery_eff
        Qhw += Qhwi
        Qhw67i = Mi*Cpi*67/Recovery_eff
        Qhw67 += Qhw67i
        Qhwdi = Qhw67i-Qhwi

        Mii[i]=Mi
        Cpii[i]=Cpi
        Tdeltaii[i]=Tdeltai
        Qhwii[i]=Qhwi
        Qhw67ii[i]=Qhw67i
        Qhwdii[i]=Qhwdi
        
    Qhwd=Qhw67-Qhw
    dfC.loc[0, 'Qhwd'] = Qhwd
    Qe=max(dfC['WattHrs'])
    dfC.loc[0, 'Qe'] = Qe
    GasConsumption = max(dfC['Gas ascf'])
    Barometer = max(dfC['Barometer'])
    GasTemp = max(dfC['Gas TC'])
    Correction_fact = (GasPressure*0.0735+Barometer)*520/(30*(460+GasTemp))
    dfC.loc[0, 'Correction Factor'] = Correction_fact
    PowerConsumption = Qe
    Qf = GasConsumption*HHV*Correction_fact + PowerConsumption*3.412
    dfC.loc[0, 'Qf'] = Qf
    Qd = Qf + Qe
    dfC.loc[0, 'Qd'] = Qd
    Qdm = Qf + Qhwd
    dfC.loc[0, 'Qdm'] = Qdm


    UEF=0
    UEF1=0
    UEFii=dict()
    for i in range(1,15):
        Mi = sum(M[i])
        Cpi = round((((sum(Tout[i])/len(Tout[i]))+(sum(Tin[i])/len(Tin[i]))))/2,1)
        Cpi = dfZ.loc[dfZ['T']==AvgTmp, 'Cp'].values[0]
        UEFi = Mi*Cpi*67/Qdm
        UEF += UEFi
        if i==1 or i==5 or i==14:
            UEF1 += UEFi
        UEFii[i]=UEFi


    dfC.loc[0, 'UEF'] = round(UEF*100,2)
    dfC.loc[0, 'UEF(1-5-14)'] = round(UEF1/UEF*100,2)

      
    dfC['Mi']=0
    dfC['Cpi']=0
    dfC['Tdeltai']=0
    dfC['Qhwi']=0
    dfC['Qhw67i']=0
    dfC['Qhwdi']=0
    dfC['UEFi']=0

    for idx in range(0, len(dfC.Draw)):
        if dfC.loc[idx, 'Draw']!=0:
            key=int(dfC.loc[idx, 'Draw'])
            dfC.loc[idx, 'Mi']=Mii[key]
            dfC.loc[idx, 'Cpi']=Cpii[key]
            dfC.loc[idx, 'Tdeltai']=Tdeltaii[key]
            dfC.loc[idx, 'Qhwi']=Qhwii[key]
            dfC.loc[idx, 'Qhw67i']=Qhw67ii[key]
            dfC.loc[idx, 'Qhwdi']=Qhwdii[key]
            dfC.loc[idx, 'UEFi']=round(UEFii[key]*100,2)
   
    return dfC