#Create a class that contains all unit info
class Info:
    def __init__(self, baseModel, icn, refrigerantCharge, operationalMode, constructionOption, category, 
                 ambientCondition, ambientTmp, voltage, tankTmp, cycles, suppWaterTmp, startDate, station, instance):
        self.baseModel = baseModel
        self.icn = icn
        self.refrigerantCharge = refrigerantCharge
        self.operationalMode = operationalMode
        self.constructionOption = constructionOption
        self.category = category
        self.ambientCondition = ambientCondition
        self.ambientTmp = ambientTmp
        self.voltage = voltage
        self.tankTmp = tankTmp
        self.cycles = cycles
        self.suppWaterTmp = suppWaterTmp
        self.startDate = startDate
        self.station = station
        self.instance = instance

    def getBaseModel(self):
        return self.baseModel
    def getIcn(self):
        return self.icn
    def getRefrigerantCharge(self):
        return self.refrigerantCharge
    def getOperationalMode(self):
        return self.operationalMode
    def getConstructionOption(self):
        return self.constructionOption
    def getCategory(self):
        return self.category
    def getAmbientCondition(self):
        return self.ambientCondition
    def getAmbientTmp(self):
        return self.ambientTmp
    def getVoltage(self):
        return self.voltage
    def getTankTmp(self):
        return self.tankTmp
    def getCycles(self):
        return self.cycles
    def getSuppWaterTmp(self):
        return self.suppWaterTmp
    def getStartDate(self):
        return self.startDate
    def getStation(self):
        return self.station
    def getInstance(self):
        return self.instance
        
info = {
    'F8' : Info ('HB40G5D', 'NL1299', 32, 'Heat Pump', 'Plus/Premium', 30, [140, 40], '240min-High/Low Cycle', 240, 125, 21, 75, '8/29/2019', 'F8', 14),
    'F10' : Info ('HB40G5D', 'NL1300', 32, 'Heat Pump', 'Plus/Premium', 30, [140, 40], '240min-High/Low Cycle', 240, 125, 21, 75, '8/29/2019', 'F10', 15),
    'C10': Info ('HB40G5D', 'NL0434', 22, 'Heat Pump', 'Builder', 30, [75], 'Existing Lab Condition', 240, 125, 12, 45, '7/8/2019', 'C10', 6),
    'C6' : Info ('HB40G5D', 'NL0435', 22, 'Heat Pump', 'Builder', 30, [75], 'Existing Lab Condition', 240, 125, 12, 45, '7/8/2019', 'C6', 4),
    'C5' : Info ('HB40G5D', 'NL1289', 22, 'Heat Pump', 'Plus/Premium', 30, [75], 'Existing Lab Condition', 240, 125, 12, 45, '7/8/2019', 'C5', 3),
    'C3' : Info ('HB40G5D', 'NL0437', 22, 'Heat Pump', 'Plus/Premium', 30, [75], 'Existing Lab Condition', 240, 125, 12, 45, '7/8/2019', 'C3', 1),
    'C9' : Info ('HB40G5D', 'NL0428', 22, 'Heat Pump', 'Plus/Premium', 30, [75], 'Existing Lab Condition', 240, 125, 12, 45, '7/17/2019', 'C9', 5),

    'F5' : Info ('HB50G5D', 'NL1296', 32, 'Heat Pump', 'Plus/Premium', 30, [120/40], '240min-High/Low Cycle', 240, 125, 21, 75, '8/28/2019', 'F5', 11),
    'F6': Info ('HB50G5D', 'NL1297', 32, 'Heat Pump', 'Plus/Premium', 30, [120/40], '240min-High/Low Cycle', 240, 125, 21, 75, '8/28/2019', 'F6', 12),
    'C4' : Info ('HB50G5D', 'NL0441', 22, 'Heat Pump', 'Builder', 30, [75], 'Existing Lab Condition', 240, 125, 12, 45, '7/8/2019', 'C4', 2),
    'C11' : Info ('HB50G5D', 'NL0442', 22, 'Heat Pump', 'Plus/Premium', 30, [75], 'Existing Lab Condition', 240, 125, 12, 45, '7/17/2019', 'C11', 7),

    'F3' : Info ('HB65G5D', 'NL1295', 28, 'Heat Pump', 'Builder', 30, [120, 40], '240min-High/Low Cycle', 187, 125, 21, 75, '8/28/2019', 'F3', 10),
    'F2' : Info ('HB65G5D', 'NL1294', 28, 'Heat Pump', 'Builder', 30, [120, 40], '240min-High/Low Cycle', 264, 125, 21, 75, '8/29/2019', 'F2', 9),

    'F11' : Info ('HB80G5D', 'NL0460', 28, 'High Demand', 'Plus', 30, [75], 'Existing Lab Condition', 240, 125, 144, 75, '8/23/2019', 'F11', 16),
    'F1' : Info ('HB80G5D', 'NL1293', 28, 'Heat Pump', 'Builder', 30, [120, 40], '240min-High/Low Cycle', 187, 125, 21, 75, '8/28/2019', 'F1', 8),
    'F7' : Info ('HB80G5D', 'NL1298', 28, 'Heat Pump', 'Builder', 30, [120, 40], '240min-High/Low Cycle', 264, 125, 21, 75, '8/29/2019', 'F7', 13)
    }

columns = {
    #'Time' : 
    #'Date' : 
    'INSTANCE' : [i for i in range(1, 17)],
    'DMDCYCLE' : ['Yes', 'No'],
    'COMP_RLY' : ['On', 'Off'],
    'HEATCTRL' : ['Off', 'Lower Element', 'Upper Element'],
    'FAN_CTRL' : ['Off', 'Low Speed', 'High Speed'],
    #'EXACTUAL' :
    #'EXVSUPER' : 
    #'AMBIENTT' : 
    #'LOHTRTMP' : 
    #'UPHTRTMP' : 
    #'EVAPTEMP' : 
    #'SUCTIONT' : 
    #'DISCTEMP' : 
    'ALARMS' : [i for i in range(0, 7)],
    #'COMPSTRK' : NO INFO?!!
    'WHTRCNFG' : ['Off', 'Energy Saver', 'Heat Pump', 'High Demand', 'Electric', 'Vacation'],
    'WHTRMODE' : ['Off: Disabled', 'Off: ECO Trip', 'Off: Temp Fail', 'Off: HiTankTemp', 'Off: No Demand',  'Electric', 'High Demand',  'Energy Saver', 'Pre-Warm Mode', 'Dry Fire Alarm', 'Heat Pump', 'Heat-Pump', 'Vacation'],
    #'WHTRSETP' : 
    'Station' : list(info.keys()),
    'Unit_Name' : [info.get(key).getIcn() for key in info.keys()],
    #'Sig' : 
    #'ALARM_01' :  
    #'Month' : 
    #'Actual Cycles' : 
    #'Heater Base Model' : [info.get(key).getBaseModel() for key in info.keys()],
    #'Operational Mode' : set([info.get(key).getOperationalMode() for key in info.keys()]),
    #'Cycles Target per Day' : set([info.get(key).getCycles() for key in info.keys()]),
    #'Cycles Target per 180 Days' : 
    #'Station/UnitName' : 
    #'Cycling Option' : ['3 (21 Cycles/Day)', '2 (12 Cycles/Day)', '1 (144 Cycles/Day)'],
    #'Week' : 
    #'Actual Cycles/Week' : 
    #'Target Cycles /Week' : 
    #'min' : 
    }
    
    
    
    
    
    