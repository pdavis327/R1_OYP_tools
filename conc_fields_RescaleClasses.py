import arcpy
import os



table = (r"D:\Davis\Out_Year_Planning19\EMT\EMT.gdb\EAST_ATTRIBUTES")

#addField_Name = "FAI_ConCat"

#desc = arcpy.Describe(addField_Name)

#flds = [i.name for i in desc.fields]

#if not addField_Name in flds:
	#arcpy.AddField_management(table, addField_Name, "TEXT")

veg_res = "FAI_VEG_RAW_CLASS"
fire_risk = "FAI_FIRE_RAW_CLASS"
veg_fire = "FAI_VEG_FIRE_RAW_CLASS"


fields = [veg_res, fire_risk, veg_fire]

with arcpy.da.UpdateCursor(table, fields) as cursor:
	for row in cursor:
		row[2] = (row[0] + " & " + row[1])	
		cursor.updateRow(row)
		
