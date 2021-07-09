import arcpy
import os

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Outyear Planning Weighted Sum tool"
		self.alias = ""

		# List of tool classes associated with this toolbox
		self.tools = [OYP_weightedSum]


class OYP_weightedSum(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Outyear Planning Weighted Sum"
		self.description = "Weight each layer to a proportion before summing and rescaling to 0-100"
		self.canRunInBackground = False


	def getParameterInfo(self):
		"""Define parameter definitions"""

		param0 = arcpy.Parameter(
			displayName="Raster dataset",
			name="outname",
			datatype= "DERasterDataset",
			parameterType="Required",
			direction="Output")				

		param1 = arcpy.Parameter(
		    displayName="First Raster",
		    name="Ras1",
		    datatype="GPRasterLayer",
		    parameterType="Required",
		    direction="Input")
		
		param2 = arcpy.Parameter(
		    displayName="First Raster Weight",
		    name="Ras1_weight",
		    datatype="GPDouble",
		    parameterType="Required",
		    direction="Input")
		
		param3 = arcpy.Parameter(
		    displayName="Second Raster",
		    name="Ras2",
		    datatype="GPRasterLayer",
		    parameterType="Required",
		    direction="Input")
		
		param4 = arcpy.Parameter(
		    displayName="Second Raster Weight",
		    name="Ras2_weight",
		    datatype="GPDouble",
		    parameterType="Required",
		    direction="Input")

		param5 = arcpy.Parameter(
		    displayName="Third Raster",
		    name="Ras3",
		    datatype="GPRasterLayer",
		    parameterType="Required",
		    direction="Input")	
		
		param6 = arcpy.Parameter(
		    displayName="Third Raster Weight",
		    name="Ras3_weight",
		    datatype="GPDouble",
		    parameterType="Required",
		    direction="Input")	

		param2.filter.type = "Range"
		param2.filter.list = [0, 1]
		
		param4.filter.type = "Range"
		param4.filter.list = [0, 1]
		
		param6.filter.type = "Range"
		param6.filter.list = [0, 1]		

		params = [param0, param1, param2, param3, param4, param5, param6]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def execute(self, parameters, messages):
		#Input params
		outname = parameters[0].valueAsText
		
		Ras1 = parameters[1].valueAsText	
		Ras1_weight = parameters[2].value
		
		Ras2 = parameters[3].valueAsText	
		Ras2_weight = parameters[4].value
		
		Ras3 = parameters[5].valueAsText	
		Ras3_weight = parameters[6].value

		#Perform Processing
		arcpy.env.overwriteOutput = True		
		from arcpy.sa import *  

		if Ras1_weight + Ras2_weight + Ras3_weight != 1.0:
			arcpy.AddMessage("\n***Raster layer weights do not equal 1.0. Please rerun the tool and assign each layer weight parameter a value between 0-1, totalling 1.0 among layers.***\n")
			exit()
		
		#Perform raster algebra
		arcpy.CheckOutExtension("Spatial")
		
		raster_sum = ((Raster(Ras1) * Ras1_weight) + (Raster(Ras2) * Ras2_weight) + (Raster(Ras3) * Ras3_weight))
					  
		raster_sum_rescale = Int(((raster_sum - raster_sum.minimum) * 100 / (raster_sum.maximum - raster_sum.minimum) + 0) + 0.5)
		
		#Save to geodatabase
		arcpy.CopyRaster_management(raster_sum_rescale, outname, '', "255", '', '', '', "8_BIT_UNSIGNED")
		#raster_sum_rescale.save(outname)		

		arcpy.AddMessage("Operation Complete")

		return
