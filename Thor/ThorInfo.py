#Create a class that contains all unit info
class Info:
    def __init__(self, baseModel, icn, category, ambientCondition, ambientTmp, voltage, tankTmp, suppWaterTmp, cycles, station, instance):
        self.baseModel = baseModel
        self.icn = icn
        self.category = category
        self.ambientCondition = ambientCondition
        self.ambientTmp = ambientTmp
        self.voltage = voltage
        self.tankTmp = tankTmp
        self.cycles = cycles
        self.suppWaterTmp = suppWaterTmp
        self.station = station
        self.instance = instance

    def getBaseModel(self):
        return self.baseModel
    def getIcn(self):
        return self.icn
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
    def getStation(self):
        return self.station
    def getInstance(self):
        return self.instance
        
info = {
    'MGM 1' : Info ('65', '10879', 5 , [75], 'Existing Lab Condition', 120, 125, 75, 65, 'MGM 1', 1),
    'MGM 2' : Info ('65', '10986', 5, [75], 'Existing Lab Condition', 120, 125, 75, 65, 'MGM 2', 2),
    'MGM 3' : Info ('80', '10987', 5, [75], 'Existing Lab Condition', 120, 125, 75, 80, 'MGM 3', 3),
    'MGM 4' : Info ('80', '10988', 5, [75], 'Existing Lab Condition', 120, 125, 75, 80, 'MGM 4', 4)    
    #'C4' : Info ('HB50G5D', 'NL0441', 22, 'Energy Saver', 'Builder', 30, [75], 'Existing Lab Condition', 240, 125, 45, 76.5, '2019-7-8', '2019-7-8', '2019-10-10', 'C04', 2),
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
    'Unit_Name' : [info.get(key).getIcn() for key in info.keys()],
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