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


    dfC['Draw no']=(dfC['Drain Valve'].diff()==1).cumsum()
    dfC['Draw no']=np.where(dfC['Drain Valve']==0,0,dfC['Draw no'])

    dfC['Purge no']=(dfC['Purge Valve'].diff()==1).cumsum()
    dfC['Purge no']=np.where(dfC['Purge Valve']==0,0,dfC['Purge no'])

    #Extracting indeces from CUT OUT before Draw 1 start to CUT OUT after Draw 1 start
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
        
        
    #Calculating Correction Factor 1
    GasPressure = float(dfV.loc[dfV['Variable'].str.contains('Gas Pressure'), 'Value'].values)
    dfC.loc[0, 'Gas Pressure'] = GasPressure
    Barometer1 = dfC.loc[dfC['Draw no']==1, 'Barometer'].mean()
    GasTemp1 = dfC.loc[dfC['Draw no']==1, 'Gas TC'].mean()
    Correction_fact1 = (GasPressure*0.0735+Barometer1)*519.67/(30*(459.67+GasTemp1))
    dfC.loc[0, 'Correction Factor (1)'] = Correction_fact1

    #Calculating Correction Factor
    Barometer = dfC['Barometer'].mean() #3rd digit wrong
    GasTemp = dfC['Gas TC'].mean()
    Correction_fact = (GasPressure*0.0735+Barometer)*520/(30*(460+GasTemp))
    dfC.loc[0, 'Correction Factor'] = Correction_fact
           
            
    #Calculating Qr (Q1)
    idx1 = dfC.index[dfC['Draw no']==1][0]
    idx2 = dfC.index[dfC['Draw no']==2][0]

    GasConsumption1 = max(dfC.loc[idx1:idx2, 'Gas ascf'])
    HHV = float(dfV.loc[dfV['Variable'].str.contains('HHV'), 'Value'].values)
    dfC.loc[0, 'High Heating Value'] = HHV
    GasMeterCorrection = float(dfV.loc[dfV['Variable'].str.contains('GP Correction Factor '), 'Value'].values[0])
    PowerConsumption1 = dfC.loc[idx1:idxTwo, 'WattHrs'].max()
    Qr = GasConsumption1*HHV*Correction_fact1*GasMeterCorrection + PowerConsumption1*3.412
    dfC.loc[0, 'Qr'] = Qr
    

    #Calculating Qf
    GasConsumption = dfC['Gas ascf'].max()
    Qe=max(dfC['WattHrs'])
    dfC.loc[0, 'Qe'] = Qe
    PowerConsumption = Qe
    Qf = GasConsumption*HHV*Correction_fact*GasMeterCorrection + PowerConsumption*3.412
    dfC.loc[0, 'Qf'] = Qf

    #Creating water mass column
    for idx in range(1,dfC['Draw no'].max()+1):
        if idx==1:
            t1 = dfC.loc[dfC['Draw no']==idx, 'TimeStamp (sec)'].iloc[0]
            tempIdx1 = find_nearest(dfC['TimeStamp (sec)'].values, t1+5)
            idx2 = dfC.index[dfC['Draw no']==idx][-1]
            Mass = dfC.loc[idx2, 'Drawn Water (Gallons)']
            Tout = round((dfC.loc[tempIdx1:idx2, 'Tout']).mean(),1)
            Density = dfZ.loc[dfZ['T']==Tout, 'Density'].values[0]
            dfC.loc[idx, 'Mass Water'] = Mass*Density
        else:
            t1 = dfC.loc[dfC['Draw no']==idx, 'TimeStamp (sec)'].iloc[0]
            tempIdx1 = find_nearest(dfC['TimeStamp (sec)'].values, t1+5)
            idx1 = dfC.index[dfC['Draw no']==idx-1][-1]
            idx2 = dfC.index[dfC['Draw no']==idx][-1]
            Mass = dfC.loc[idx2, 'Drawn Water (Gallons)']-dfC.loc[idx1, 'Drawn Water (Gallons)']
            Tout = round(dfC.loc[tempIdx1:idx2, 'Tout'].mean(),1)
            Density = dfZ.loc[dfZ['T']==Tout, 'Density'].values[0]
            dfC.loc[idx, 'Mass Water'] = Mass*Density


    #Calculating Recovery Efficiency
    t1 = dfC.loc[dfC['Draw no']==1, 'TimeStamp (sec)'].iloc[0]
    idx1 = find_nearest(dfC['TimeStamp (sec)'].values, t1+5)
    idx2 = dfC.index[dfC['Draw no']==1][-1]
    Tin1 = dfC.loc[idx1:idx2, 'Tin'].mean()
    Tout1 = dfC.loc[idx1:idx2, 'Tout'].mean()
    M1 = dfC.loc[1, 'Mass Water']
    AvgTmp = round((Tout1+Tin1)/2,1)
    Cp1 = dfZ.loc[dfZ['T']==AvgTmp, 'Cp'].values[0]
    Tdelta1 = Tout1-Tin1
    Recovery_eff = M1*Cp1*Tdelta1/Qr
    
    dfC.loc[0,'M1']=M1
    dfC.loc[0,'Tdelta1']=Tdelta1
    dfC.loc[0,'Cp1']=Cp1
    dfC.loc[0,'Recovery Efficiency']=Recovery_eff

    
    #Calculate the following equations:
    #Qhw67i = Mi*Cpi*67/Recovery Efficiency
    #Qhwi = Mi*Cpi*Tdeltai/Recovery Efficiency
    #Qhwdi = Qhw67i-Qhwi
    Mii=dict()
    Cpii=dict()
    Tdeltaii=dict()
    Qhwii=dict()
    Qhw67ii=dict()
    Qhwdii=dict()
            
    Qhw=0
    Qhw67=0

    for i in range(1,dfC['Draw no'].max()+1):
        Mi = dfC.loc[i, 'Mass Water']
        t1 = dfC.loc[dfC['Draw no']==i, 'TimeStamp (sec)'].iloc[0]
        idx1 = find_nearest(dfC['TimeStamp (sec)'].values, t1+5)
        idx2 = dfC.index[dfC['Draw no']==i][-1]
        AvgTmp = round((dfC.loc[idx1:idx2, 'Tout'].mean()+dfC.loc[idx1:idx2, 'Tin'].mean())/2,1)
        Cpi = dfZ.loc[dfZ['T']==AvgTmp, 'Cp'].values[0]
        dfC.loc[0, 'Cp('+str(i)+')']=Cpi        
        Tdeltai = dfC.loc[idx1:idx2, 'Tout'].mean()-dfC.loc[idx1:idx2, 'Tin'].mean()
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
    Qd = Qf + Qe
    dfC.loc[0, 'Qd'] = Qd
    Qdm = Qf + Qhwd
    dfC.loc[0, 'Qdm'] = Qdm

    
    UEF=0
    UEF1=0
    UEF2=0
    UEFii=dict()
    for i in range(1,dfC['Draw no'].max()+1):
        Mi = dfC.loc[i, 'Mass Water']
        AvgTmp = round((dfC.loc[idx1:idx2, 'Tout'].mean()+dfC.loc[idx1:idx2, 'Tin'].mean())/2,1)
        Cpi = dfZ.loc[dfZ['T']==AvgTmp, 'Cp'].values[0]
        dfC.loc[0, 'Cp('+str(i)+')']=Cpi        
        UEFi = Mi*Cpi*67/Qdm
        UEF += UEFi
        if i==1 or i==5 or i==14:
            UEF1 += UEFi
        if i==1 or i==5 or i==14 or i==4 or i==6:
            UEF2 += UEFi
        UEFii[i]=UEFi

    dfC.loc[0, 'UEF'] = UEF
    dfC.loc[0, 'UEF(1-5-14)'] = UEF1/UEF
    dfC.loc[0, 'UEF(1-5-14-4-6)'] = UEF2/UEF

    
    #Creating columns of parameters per draw
    dfC['Mi']=0
    dfC['Cpi']=0
    dfC['Tdeltai']=0
    dfC['Qhwi']=0
    dfC['Qhw67i']=0
    dfC['Qhwdi']=0
    dfC['UEFi']=0

    for idx in range(0, len(dfC.Draw)):
        if dfC.loc[idx, 'Draw no']!=0:
            key=int(dfC.loc[idx, 'Draw no'])
            dfC.loc[idx, 'Mi']=Mii[key]
            dfC.loc[idx, 'Cpi']=Cpii[key]
            dfC.loc[idx, 'Tdeltai']=Tdeltaii[key]
            dfC.loc[idx, 'Qhwi']=Qhwii[key]
            dfC.loc[idx, 'Qhw67i']=Qhw67ii[key]
            dfC.loc[idx, 'Qhwdi']=Qhwdii[key]
            dfC.loc[idx, 'UEFi']=round(UEFii[key],4)
   
    return dfC