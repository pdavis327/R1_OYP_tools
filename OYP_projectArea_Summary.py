import arcpy
import os
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.overwriteOutput = True
arcpy.env.addOutputsToMap = 0

#proj area segments
Proj_area = (r"T:\FS\NFS\R01\Project\OutYearPlanning\GIS\FY20\LayerFile\R1 Program of Work Project Areas.lyr")

#sumamry layer folder
sum_fold = (r"T:\FS\NFS\R01\Program\7140Geometronics\GIS\Project\zz_R1OutyearPlanning2019\PodAssessment\MXD\ACC_SummaryLayerFiles_Regional")

#Out Excel table path and ext. - "addresses.xls"
outTable = (r"T:\FS\NFS\R01\Program\7140Geometronics\GIS\Project\zz_R1OutyearPlanning2019\PodAssessment\Workspace\pdavis\Summary_tool_Test\outMstrTst.xls")
#add field function
def addField(feature, fieldName, fType):
	field_names = [i.name for i in arcpy.ListFields(feature)]

	if not fieldName in field_names: 
		arcpy.AddField_management(feature, fieldName, fType)		

#Populate area new feature class
def addAreaField(feature, fieldName):
	if arcpy.Describe(feature).shapeType == "Polygon":
		field_names = [i.name for i in arcpy.ListFields(feature)]

		if not fieldName in field_names: 
			arcpy.AddField_management(feature, fieldName, "Float")
			arcpy.CalculateField_management(feature, fieldName, "!SHAPE.area@ACRES!", "PYTHON_9.3")	
		else:
			arcpy.CalculateField_management(feature, fieldName, "!SHAPE.area@ACRES!", "PYTHON_9.3")	

#list all files in folder
rasters = []
vectors = []

walk = arcpy.da.Walk(sum_fold)
for dirpath,dirnames,filenames in walk:
	for filename in filenames:
		path = os.path.join(dirpath, filename)
		desc = arcpy.Describe(path)
		if desc.dataElement.dataType == "FeatureClass":
			vectors.append(path)
		else:
			rasters.append(path)


Proj = arcpy.FeatureClassToFeatureClass_conversion(Proj_area, r"in_memory", 'copy_projArea', "", 'ID "ID" true true false 255 Text 0 0 ,First,#,R1 Program of Work Project Areas,ID,-1,-1;NAME "NAME" true true false 255 Text 0 0 ,First,#,R1 Program of Work Project Areas,NAME,-1,-1;PROJECTTYP "PROJECTTYPE" true true false 4 Long 0 10 ,First,#,R1 Program of Work Project Areas,PROJECTTYPE,-1,-1;ORG "ORG" true true false 6 Text 0 0 ,First,#,R1 Program of Work Project Areas,ORG,-1,-1', '#')

Proj_copy = arcpy.MakeFeatureLayer_management(Proj, "Proj_copy")	

addAreaField(Proj_copy, "Acres")

mstr_table = arcpy.TableToTable_conversion(Proj_copy, r"in_memory", 'copy_table')

#Process Vectors 
for i in vectors:
	desc = arcpy.Describe(i)
	name = arcpy.ValidateFieldName(desc.basename, mstr_table)
	vec_feat = arcpy.FeatureClassToFeatureClass_conversion(i, r"in_memory", 'vec_feat')
	addAreaField(vec_feat, "Acr")
	vec_copy = arcpy.MakeFeatureLayer_management(vec_feat, "vec_copy",'#', '#', 'FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;STATE STATE VISIBLE NONE;ACRES_WITH ACRES_WITH VISIBLE NONE;LATEST_REV LATEST_REV VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE_AREA SHAPE_AREA VISIBLE NONE;SHAPE_LEN SHAPE_LEN VISIBLE NONE;Acr Acr VISIBLE RATIO')
	identvec = arcpy.Identity_analysis(Proj_copy, vec_copy, r"in_memory\identvec")
	identvec_stats = arcpy.Statistics_analysis(identvec, r"in_memory\identvec_stats", [["Acr", "SUM"]], 'NAME')
	arcpy.JoinField_management(mstr_table, 'NAME', identvec_stats, 'NAME', 'SUM_Acr')
	addField(mstr_table, name,  "Float")
	arcpy.CalculateField_management(mstr_table, name, '[SUM_Acr]/ [Acres]', 'VB')
	arcpy.DeleteField_management(mstr_table, 'SUM_Acr')


#Process Rasters
#get unique table vals function
def unique_values(table , field):
	with arcpy.da.SearchCursor(table, [field]) as cursor:
		return sorted({row[0] for row in cursor})

for i in rasters:
	val = unique_values(i, 'Class')
	n = 0
	while n < len(val):
		Ras = Raster(i)
		expr = "Class = '{}'".format(val[n])
		ras_sel = ExtractByAttributes(Ras, expr)	
		poly = arcpy.RasterToPolygon_conversion(ras_sel, r"in_memory\Raspoly", 'NO_SIMPLIFY', 'Class')
		vec_feat = arcpy.FeatureClassToFeatureClass_conversion(poly, r"in_memory","Raspoly2")
		vec_feat = arcpy.Dissolve_management(vec_feat, r"in_memory\Raspoly3", 'Class')
		addAreaField(vec_feat, "Acr")
		arcpy.MakeFeatureLayer_management(vec_feat, 'vec_lyr', "", "", 'FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;Class Class VISIBLE NONE;Acr Acr VISIBLE RATIO')
		identvec = arcpy.Identity_analysis(Proj_copy, 'vec_lyr', r"in_memory\identvec")
		identvec_stats = arcpy.Statistics_analysis(identvec, r"in_memory\identvec_stats", [["Acr", "SUM"]], 'NAME')
		arcpy.JoinField_management(mstr_table, 'NAME', identvec_stats, 'NAME', 'SUM_Acr')
		desc = arcpy.Describe(i)
		if "Integrated" in desc.basename:
			base = "I"
		elif "Timber" in desc.basename:
			base = "T"
		elif "Fire" in desc.basename:
			base = "F"
		elif "Vegetation" in desc.basename:
			base = "V"
		name = arcpy.ValidateFieldName(base + "_{}".format(val[n]) , mstr_table)	
		addField(mstr_table, name,  "Float")
		arcpy.CalculateField_management(mstr_table, name, '[SUM_Acr]/ [Acres]', 'VB')
		arcpy.DeleteField_management(mstr_table, 'SUM_Acr')
		n += 1	

arcpy.TableToExcel_conversion(mstr_table, outTable)


