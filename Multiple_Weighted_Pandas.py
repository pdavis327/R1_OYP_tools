import pandas as pd

scenarios_dict = {
        'Scenario': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
        'Fire':     [0,0,0,2,0,0,2,4,2,7,9,7,5,5,2,3], 
        'Veg':      [0,2,4,2,7,9,7,5,5,2,0,0,0,2,0,3],
        'Econ':     [9,7,5,5,2,0,0,0,2,0,0,2,4,2,7,3]
        } 


test_scen= {
        'Scenario': [1,2,3,4,5,],
        'Fire':     [0,0,0,2,0,], 
        'Veg':      [0,2,4,2,7,],
        'Econ':     [9,7,5,5,2,]
        } 


attr_test = {
        'segment':       [1,2,3,4,5,6,7,8],
        'Fire_risk':     [2,4,6,5,2,1,4,4], 
        'Veg_risk':      [3,3,5,2,7,8,9,0],
        'Econ_risk':     [5,7,5,3,2,0,2,8]
        } 

attr_test = test_scene["Scenario1"]

scenarios = pd.DataFrame(test_scen) 

attributes = pd.DataFrame(attr_test) 


test_out = (pd.scenarios.values * attributes.values, columns=attributes.columns, index=attributes.index)


import arcpy
Attr_table = (r"")


i = 1
test = ["Phish", "Free"]
while i <=13:
    arcpy.AddField_management(Attr_table, "Scenario_{}".format(i), "TEXT")
    i+=1


fields = ['Fire_risk', 'Veg_risk', 'Econ_risk', "Scenario_1", "Scenario_1", "Scenario_1", "Scenario_1", "Scenario_1", "Scenario_1", "Scenario_1"]

# Create update cursor for feature class 
with arcpy.da.UpdateCursor(fc, fields) as cursor: