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
    #print('Gas Pressure: ', GasPressure)
    #Barometer = dfC.loc[idxOne:idxTwo, 'Barometer'].mean(axis=0)
    Barometer = max(dfC.loc[idxOne:idxTwo, 'Barometer'])
    #print('Barometer:', Barometer)
    #GasTemp = dfC.loc[idxOne:idxTwo, 'Gas TC'].mean(axis=0)
    GasTemp = max(dfC.loc[idxOne:idxTwo, 'Gas TC'])
    #print('Gas Temp:', GasTemp)
    Correction_fact = (GasPressure*0.0735+Barometer)*520/(30*(460+GasTemp))
    dfC.loc[0, 'Correction Factor (1)'] = Correction_fact
    #print('\nCF:', Correction_fact)
    
    
    HHV = float(dfV.loc[dfV['Variable'].str.contains('HHV'), 'Value'].values)
    #print('HHV:', HHV)
    #GasConsumption = dfC.loc[idxOne:idxTwo, 'Gas ascf'].mean(axis=0)
    GasConsumption = max(dfC.loc[idxOne:idxTwo, 'Gas ascf'])
    #print('Gas Consumption:', GasConsumption)
    #print('Correlation Factor:', Correction_fact)
    #PowerConsumption = dfC.loc[idxOne:idxTwo, 'WattHrs'].mean(axis=0)
    PowerConsumption = max(dfC.loc[idxOne:idxTwo, 'WattHrs'])
    #print('Power Consumption:', PowerConsumption)
    Qr = GasConsumption*HHV*Correction_fact + PowerConsumption*3.412
    dfC.loc[0, 'Qr'] = Qr
    #Qr = Qr*3412/1000 #1kWh = 3412Btu
    #print('\nQr:', Qr)
    
    dfC['Mi'] = 0
    for idx in range(1,dfC.shape[0]):
        dfC.loc[idx, 'Mi'] = (dfC.loc[idx, 'Drawn Water (Gallons)']-dfC.loc[idx-1, 'Drawn Water (Gallons)'])*8.35
        
    xls = pd.ExcelFile('UEF analysis.xlsx')
    dfZ = pd.read_excel(xls, 'Sheet3', skiprows=6, index_col=None, usecols = 'A,B', names = ['T','Cp'])

    startDraw = dfE.loc[dfE['Desc'].str.contains('Starting Draw # 1 '), 'TimeStamp'].values
    endDraw = dfE.loc[dfE['Desc'].str.contains('Draw Complete'), 'TimeStamp'].values

    startDrawIdx = find_nearest(dfC['TimeStamp (sec)'].values, startDraw[0])
    endDrawIdx = find_nearest(dfC['TimeStamp (sec)'].values, endDraw[0])

    M1 = (dfC.loc[startDrawIdx:endDrawIdx, 'Mi']).sum()
    #print('M1: ', M1)
    Tout1 = dfC.loc[startDrawIdx:endDrawIdx, 'Tout'].mean()
    Tin1 = dfC.loc[startDrawIdx:endDrawIdx, 'Tin'].mean()
    Cp1 = round((Tout1+Tin1)/2,1)
    Cp1 = dfZ.loc[dfZ['T']==Cp1, 'Cp'].values[0]
    #print('Cp1:', Cp1)
    #print('Delivery water temp:', Tout1)
    #print('Supply water temp:', Tin1)
    Tdelta1 = Tout1-Tin1
    #print('Tdelta1:', Tdelta1)
    Recovery_eff = M1*Cp1*Tdelta1/Qr
    dfC.loc[0,'Recovery Efficiency']=Recovery_eff
    #print('\nRecovery eff:', Recovery_eff)
    
    M=dict()
    Cp=dict()
    Tout=dict()
    Tin=dict()

    for idx in range(0, len(dfC.Draw)):
        if dfC.loc[idx, 'Draw']!=0:
            key = int(dfC.loc[idx, 'Draw'])
            M.setdefault(key,[]).append(dfC.loc[idx, 'Mi'])
            Cp.setdefault(key,[]).append(dfC.loc[idx, 'Drawn Water (Gallons)'])
            Tout.setdefault(key,[]).append(dfC.loc[idx, 'Tout'])
            Tin.setdefault(key,[]).append(dfC.loc[idx, 'Tin'])

    Qhw=0
    Qhw67=0

    for i in range(1,15):
        Mi = sum(M[i])
        dfC.loc[0, 'M('+str(i)+')']=Mi
        #print('Mi:', Mi)
        Cpi = round((((sum(Tout[i])/len(Tout[i]))+(sum(Tin[i])/len(Tin[i]))))/2,1)
        Cpi = dfZ.loc[dfZ['T']==Cpi, 'Cp'].values[0]
        dfC.loc[0, 'Cp('+str(i)+')']=Cpi
        #print('Cpi:', Cpi)
        Tdeltai = ((sum(Tout[i])/len(Tout[i]))-(sum(Tin[i])/len(Tin[i])))
        dfC.loc[0, 'Tdelta('+str(i)+')']=Tdeltai
        #print('Tdeltai:', Tdeltai)
        Qhwi = Mi*Cpi*Tdeltai/Recovery_eff
        Qhw += Qhwi
        dfC.loc[0, 'Qhw('+str(i)+')']=Qhwi
        Qhw67i = Mi*Cpi*67/Recovery_eff
        Qhw67 += Qhw67i
        dfC.loc[0, 'Qhw67('+str(i)+')']=Qhw67i
        Qhwdi = Qhw67i-Qhwi
        dfC.loc[0, 'Qhwd('+str(i)+')']=Qhwdi
        #print('Qhw',i,':', Mi*Cpi*Tdeltai/Recovery_eff)
        #print('Qhw67',i,':', Mi*Cpi*67/Recovery_eff)
    #print('\nQhw:', Qhw)
    #print('Qhw67:', Qhw67)
    Qhwd=Qhw67-Qhw
    dfC.loc[0, 'Qhwd'] = Qhwd
    #print('Qhwd:', Qhwd)
    Qe=max(dfC['WattHrs'])
    dfC.loc[0, 'Qe'] = Qe
    #print('Qe:', Qe)
    #print('HHV:', HHV)
    GasConsumption = max(dfC['Gas ascf'])
    #print('Gas Consumption:', GasConsumption)
    Barometer = max(dfC['Barometer'])
    #print('Barometer:', Barometer)
    GasTemp = max(dfC['Gas TC'])
    #print('Gas Temp:', GasTemp)
    Correction_fact = (GasPressure*0.0735+Barometer)*520/(30*(460+GasTemp))
    dfC.loc[0, 'Correction Factor'] = Correction_fact
    #print('Correction Factor:', Correction_fact)
    PowerConsumption = Qe
    #print('Power Consumption:', PowerConsumption)
    Qf = GasConsumption*HHV*Correction_fact + PowerConsumption*3.412
    dfC.loc[0, 'Qf'] = Qf
    #Qf = Qf*3412/1000 #1kWh = 3412Btu
    #print('Qf:', Qf)
    Qd = Qf + Qe
    dfC.loc[0, 'Qd'] = Qd
    #print('Qd:', Qd)
    #Qdm = Qd + Qhwd
    Qdm = Qf + Qhwd
    dfC.loc[0, 'Qdm'] = Qdm
    #print('Qdm:', Qdm)
    
    UEF=0
    UEF1=0
    for i in range(1,15):
        Mi = sum(M[i])
        #print('Mi:', Mi)
        Cpi = round((((sum(Tout[i])/len(Tout[i]))+(sum(Tin[i])/len(Tin[i]))))/2,1)
        Cpi = dfZ.loc[dfZ['T']==Cpi, 'Cp'].values[0]
        #print('Cpi:', Cpi)
        UEFi = Mi*Cpi*67/Qdm
        UEF += UEFi
        dfC.loc[0, 'UEF('+str(i)+')']=UEFi
        #print('UEF',i,Mi*Cpi*67/Qdm)
        if i==1 or i==5 or i==14:
            UEF1 += UEFi
            
    dfC.loc[0, 'UEF'] = UEF
    dfC.loc[0, 'UEF(1-5-14)'] = round(UEF1/UEF*100,2)
    #print('UEF:' + str(UEF))
    #print('UEF from Takashi\'s file: ' + str(round(UEF1/UEF*100,2)) + '%')
    
    return dfC
    