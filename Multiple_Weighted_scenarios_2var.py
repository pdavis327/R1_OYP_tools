import arcpy
Attr_table = (r"D:\Davis\Out_Year_Planning19\EMT\EMT.gdb\EAST_ATTRIBUTES")

scenarios_dict = {
    'Scenario':     [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        'Fire':     [14,13,12,11,10,9,8,7,6,5,4,3,2,1,0], 
        'Veg':      [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
} 

fields = ['FAI_FIRE_RAW_RESCALE', 'FAI_VEG_RES_RAW_RESCALE', "SCENARIO_RESCALE1", "SCENARIO_RESCALE2", "SCENARIO_RESCALE3", "SCENARIO_RESCALE4", "SCENARIO_RESCALE5", "SCENARIO_RESCALE6", "SCENARIO_RESCALE7", "SCENARIO_RESCALE8", "SCENARIO_RESCALE9", "SCENARIO_RESCALE10", "SCENARIO_RESCALE11", "SCENARIO_RESCALE12" , "SCENARIO_RESCALE13", "SCENARIO_RESCALE14", "SCENARIO_RESCALE15"]

with arcpy.da.UpdateCursor(Attr_table, fields) as cursor:
	for row in cursor:
		i = 0
		n = 2
		while i < len(scenarios_dict['Scenario']):
			f1 = row[0] * scenarios_dict['Fire'][i]
			v1 = row[1] * scenarios_dict['Veg'][i]
			varSum = f1 + v1	

			row[n] = varSum
			i+=1
			n+=1
			cursor.updateRow(row) 