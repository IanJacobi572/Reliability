import numpy as np

#Create a class that contains all unit info
class Info:
    def __init__(self, baseModel, icn, refrigerantCharge, operationalMode, constructionOption, category, 
                 ambientCondition, ambientTmp, voltage, tankTmp, suppWaterTmp, cycles, startDate, teamStartDate, changedDate, station, instance):
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
        self.teamStartDate = teamStartDate
        self.changedDate = changedDate
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
    def getSuppWaterTmp(self):
        return self.suppWaterTmp
    def getCycles(self):
        return self.cycles
    def getStartDate(self):
        return self.startDate
    def getTeamStartDate(self):
        return self.teamStartDate
    def getChangedDate(self):
        return self.changedDate
    def getStation(self):
        return self.station
    def getInstance(self):
        return self.instance
        
info = {
    'D1' : Info ('HB40G5D', 'NL1301', 26, 'Energy Saver', 'Retail', 30, '(75)', 'Existing Lab Condition', 264, 125, 75, 80, '2019-9-23', '2019-9-23', '2019-10-7', 'D01', 17),
    'D2' : Info ('HB40G5D', 'NL1302', 26, 'Energy Saver', 'Builder', 15, '(75)', 'Existing Lab Condition', 264, 125, 75, 80, '2019-9-23', '2019-9-23', '2019-10-8', 'D02', 18),
    'D3' : Info ('HB40G5D', 'NL1303', 26, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 75, 80, '2019-9-23', '2019-9-23', '2019-10-8', 'D03', 19),
    'D4' : Info ('HB40G5D', 'NL1304', 26, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 75, 80, '2019-9-23', '2019-9-23', '2019-10-8', 'D04', 20),
    'F8' : Info ('HB40G5D', 'NL1299', 32, 'Energy Saver', 'Retail', 30, '(140, 40)', '60min-High-Low Cycle', 240, 125, 75, 80, '2019-8-30', '2019-8-12', '2019-10-9', 'F08', 14),
    'F10' : Info ('HB40G5D', 'NL1300', 32, 'Energy Saver', 'Retail', 30, '(140, 40)', '60min-High-Low Cycle', 240, 125, 75, 80, '2019-8-30', '2019-8-12', '2019-10-9', 'F10', 15),
    'C10': Info ('HB40G5D', 'NL0434', 22, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 45, 80, '2019-7-8', '2019-4-15', '2019-10-10', 'C10', 6),
    'C6' : Info ('HB40G5D', 'NL0435', 22, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 45, 80, '2019-7-8', '2019-7-8', '2019-10-10', 'C06', 4),
    'C5' : Info ('HB40G5D', 'NL1289', 22, 'Energy Saver', 'Retail', 30, '(75)', 'Existing Lab Condition', 240, 125, 45, 80, '2019-7-8', '2019-7-8', '2019-10-10', 'C05', 3),
    #'C3' : Info ('HB40G5D', 'NL0437', 22, 'Energy Saver', 'Retail', 30, '75', 'Existing Lab Condition', 240, 125, 45, 80, '2019-7-8', '2019-7-8', '2019-10-10', 'C03', 1),
    'C3' : Info ('HB40G5D', 'NL0458', 32, 'Energy Saver', 'Retail', 30, '(76)', 'Existing Lab Condition', 240, 125, 45, 80, '2019-10-24', '2019-10-24', '2019-10-24', 'C03', 1),
    'C9' : Info ('HB40G5D', 'NL0428', 22, 'Energy Saver', 'Retail', 30, '(75)', 'Existing Lab Condition', 240, 125, 45, 80, '2019-7-8', '2019-4-15', '2019-10-10', 'C09', 5),

    'D5' : Info ('HB50G5D', 'NL305', 26, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 75, 76.5, '2019-9-23', '2019-9-23', '2019-10-8', 'D05', 21),
    'D6' : Info ('HB50G5D', 'NL306', 26, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 75, 76.5, '2019-9-23', '2019-9-23', '2019-10-8', 'D06', 22),
    #'F5' : Info ('HB50G5D', 'NL1296', 32, 'Energy Saver', 'Retail', 30, [120-40], '60min-High-Low Cycle', 240, 125, 75, 76.5, '2019-8-28', '2019-8-12', '2019-10-9', 'F05', 11),
    #'F6': Info ('HB50G5D', 'NL1297', 32, 'Energy Saver', 'Retail', 30, [120-40], '60min-High-Low Cycle', 240, 125, 75, 76.5, '2019-8-28', '2019-8-12', '2019-10-9', 'F06', 12),
    'F5' : Info ('HB50G5D', 'NL1320', 32, 'Energy Saver', 'Retail', 30, '(120, 40)', '60min-High-Low Cycle', 240, 125, 75, 76.5, '2019-10-22', '2019-10-22', '2019-10-22', 'F05', 11),
    'F6': Info ('HB50G5D', 'NL1321', 32, 'Energy Saver', 'Retail', 30, '(120-40)', '60min-High-Low Cycle', 240, 125, 75, 76.5, '2019-10-23', '2019-10-23', '2019-10-23', 'F06', 12),
    'C4' : Info ('HB50G5D', 'NL0441', 22, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 45, 76.5, '2019-7-8', '2019-7-8', '2019-10-10', 'C04', 2),
    'C11' : Info ('HB50G5D', 'NL0442', 22, 'Energy Saver', 'Retail', 30, '(75)', 'Existing Lab Condition', 240, 125, 45, 76.5, '2019-7-18', '2019-7-8', '2019-10-10', 'C11', 7),

    'D7' : Info ('HB65G5D', 'NL307', 28, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 75, 78.5, '2019-9-23', '2019-9-23', '2019-10-8', 'D07', 23),
    'D8' : Info ('HB65G5D', 'NL308', 28, 'Energy Saver', 'Builder', 30, '(75)', 'Existing Lab Condition', 240, 125, 75, 78.5, '2019-9-23', '2019-9-23', '2019-10-8', 'D08', 24),
    'F3' : Info ('HB65G5D', 'NL1295', 28, 'Energy Saver', 'Builder', 30, '(120, 40)', '60min-High-Low Cycle', 187, 125, 75, 78.5, '2019-8-28', '2019-8-12', '2019-10-9', 'F03', 10),
    'F2' : Info ('HB65G5D', 'NL1294', 28, 'Energy Saver', 'Builder', 30, '(120, 40)', '60min-High-Low Cycle', 264, 125, 75, 78.5, '2019-8-28', '2019-8-12', '2019-10-9', 'F02', 9),

    'F11' : Info ('HB80G5D', 'NL0460', 28, 'Energy Saver', 'Plus', 30, '(75)', 'Existing Lab Condition', 240, 125, 75, 78.5, '2019-8-23', '2019-8-12', '2019-10-7', 'F11', 16),
    'F1' : Info ('HB80G5D', 'NL1293', 28, 'Energy Saver', 'Builder', 30, '(120, 40)', '60min-High-Low Cycle', 187, 125, 75, 78.5, '2019-8-28', '2019-8-12', '2019-10-9', 'F01', 8),
    'F7' : Info ('HB80G5D', 'NL1298', 28, 'Energy Saver', 'Builder', 30, '(120, 40)', '60min-High-Low Cycle', 264, 125, 75, 78.5, '2019-8-30', '2019-8-12', '2019-10-9', 'F07', 13)
    }

columns = {
    #'Time' : 
    #'Date' : 
    'INSTANCE' : [i for i in range(1, 25)],
    'DMDCYCLE' : ['Yes', 'No'],
    'COMP_RLY' : ['On', 'Off'],
    'HEATCTRL' : ['Off', 'Lower Element', 'Upper Element'],
    'FAN_CTRL' : ['Off', 'Low Speed', 'High Speed'],
    #'EXACTUAL' :
    #'EXVSUPER' : 
    'AMBIENTT' : [],
    'LOHTRTMP' : [],
    'UPHTRTMP' : [],
    'EVAPTEMP' : [],
    'SUCTIONT' : [],
    'DISCTEMP' : [],
    #'AMBIENTT' : [t for t in np.arange(-39.0, 9999999.0)],
    #'LOHTRTMP' : [t for t in np.arange(-39.0, 9999999.0)],
    #'UPHTRTMP' : [t for t in np.arange(-39.0, 9999999.0)],
    #'EVAPTEMP' : [t for t in np.arange(-39.0, 9999999.0)],
    #'SUCTIONT' : [t for t in np.arange(-39.0, 9999999.0)],
    #'DISCTEMP' : [t for t in np.arange(-39.0, 9999999.0)],
    #'ALARMS' : [i for i in range(0, 7)],
    #'ALARM_01': ['', 'A004', 'A005' , 'A006', 'A007', 'A008', 'A101', 'A102', 'A103', 'A104', 'A105', 'A106', 
    #   'A107', 'A108', 'A125', 'A126', 'A127', 'A128', 'A129', 'A130', 'A200', 'A900', 'A902', 'A903', 'A904',  
    #   'A905', 'T007', 'T009', 'T131', 'T132', 'T300', 'T901']
    #'COMPSTRK' : NO INFO?!!
    'WHTRCNFG' : ['Off', 'Energy Saver', 'Heat Pump', 'High Demand', 'Electric', 'Vacation'],
    'WHTRMODE' : ['Off: Disabled', 'Off: ECO Trip', 'Off: Temp Fail', 'Off: HiTankTemp', 'Off: No Demand',  
    'Electric', 'High Demand',  'Energy Saver', 'Pre-Warm Mode', 'Dry Fire Alarm', 'Heat Pump', 'Heat-Pump', 'Vacation'],
    #'WHTRSETP' : 
    'Station' : list(info.keys()),
    #'Unit_Name' : [info.get(key).getIcn() for key in info.keys()],
    #'Sig' : 
    #'ALARM_01' :  
    #'Month' : 
    #'Actual Cycles' : 
    #'Heater Base Model' : [info.get(key).getBaseModel() for key in info.keys()],
    #'Operational Mode' : set([info.get(key).getOperationalMode() for key in info.keys()]),
    #'Cycles Target per Day' : set([info.get(key).getCycles() for key in info.keys()]),
    #'Cycles Target per 180 Days' : 
    #'Station-UnitName' : 
    #'Cycling Option' : ['3 (21 Cycles-Day)', '2 (12 Cycles-Day)', '1 (144 Cycles-Day)'],
    #'Week' : 
    #'Actual Cycles-Week' : 
    #'Target Cycles -Week' : 
    #'min' : 
    }