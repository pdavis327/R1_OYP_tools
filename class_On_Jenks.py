import arcpy


Attr_table = (r"D:\Davis\Out_Year_Planning19\EMT\EMT.gdb\EAST_ATTRIBUTES")

new_field_name = "FAI_ECO_RAW_CLASS"

#input breaks from R output
Low = 7.988981
Mod = 25.985663
High = 100


#desc = arcpy.Describe(Attr_table)

#flds = [i.name for i in desc.fields]

#if not new_field_name in flds:
	#arcpy.AddField_management(Attr_table, new_field_name, "TEXT")


fields = ["FAI_ECO_RAW_RESCALE", new_field_name]

with arcpy.da.UpdateCursor(Attr_table, fields) as cursor:
	for row in cursor:
		if row[0] <= Low:
			row[1] = "1_Low"
			
		elif row[0] <= Mod:
			row[1] = "2_Moderate" 
			
		else:
			row[1] = "3_High"
			
		cursor.updateRow(row)
	
	