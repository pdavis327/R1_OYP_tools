import arcpy
import os



table = (r"D:\Davis\Out_Year_Planning19\EMT\EMT.gdb\EAST_ATTRIBUTES")

addField_Name1 = "FAI_FOCAL_SUM"
addField_Name2 = "FAI_RESCALE_SUM"

arcpy.AddField_management(table, addField_Name1, "SHORT")
arcpy.AddField_management(table, addField_Name2, "SHORT")

fire_risk_f = "FAI_FIRE_FOCAL_CLASS"
veg_res_f = "FAI_VEG_FOCAL_CLASS"

fire_risk_r = "FAI_FIRE_RAW_CLASS"
veg_res_r = "FAI_VEG_RAW_CLASS"


#print val_dic['H']

#Value Dictionary

val_dic = {
    "3_High": 3,
    "2_Moderate": 2, 
    "1_Low": 1
}


fields = [fire_risk_f, veg_res_f, addField_Name1]

with arcpy.da.UpdateCursor(table, fields) as cursor:
	for row in cursor:
		if (row[0] in val_dic):
			fr = val_dic.get(row[0])
		if (row[1] in val_dic):
			vr = val_dic.get(row[1])
		
		
		row[2] = (fr + vr)
		
		cursor.updateRow(row)
		
fields2 = [fire_risk_r, veg_res_r, addField_Name2]
		
with arcpy.da.UpdateCursor(table, fields2) as cursor:
	for row in cursor:
		if (row[0] in val_dic):
			fr = val_dic.get(row[0])
		if (row[1] in val_dic):
			vr = val_dic.get(row[1])
		
				
		row[2] = (fr + vr)
				
		cursor.updateRow(row)