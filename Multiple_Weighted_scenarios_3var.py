import arcpy
Attr_table = (r"T:\FS\NFS\R01\Program\7140Geometronics\GIS\Project\zz_R1OutyearPlanning2019\PodAssessment\Data\NID_VMap_Zonals.gdb\NID_Attributes")

scenarios_dict = {
    'Scenario':     [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
        'Fire':     [0,0,0,2,0,0,2,4,2,7,9,7,5,5,2,3], 
        'Veg':      [0,2,4,2,7,9,7,5,5,2,0,0,0,2,0,3],
        'Econ':     [9,7,5,5,2,0,0,0,2,0,0,2,4,2,7,3]
} 

i = 1
while i <=16:
	arcpy.AddField_management(Attr_table, "Scenario_{}".format(i), "TEXT")
	i+=1

fields = ['FAI_FIRE_RISK', 'FAI_VEG_RES', 'FAI_TIM_ECO', "Scenario_1", "Scenario_2", "Scenario_3", "Scenario_4", "Scenario_5", "Scenario_6", "Scenario_7", "Scenario_8", "Scenario_9", "Scenario_10", "Scenario_11", "Scenario_12" , "Scenario_13", "Scenario_14", "Scenario_15", "Scenario_16"]

with arcpy.da.UpdateCursor(Attr_table, fields) as cursor:
	for row in cursor:
		i = 0
		n = 3
		while i < len(scenarios_dict['Scenario']):
			f1 = row[0] * scenarios_dict['Fire'][i]
			v1 = row[1] * scenarios_dict['Veg'][i]
			e1 = row[2] * scenarios_dict['Econ'][i]
			varSum = f1 + v1 + e1	

			row[n] = varSum
			i+=1
			n+=1
			cursor.updateRow(row) 