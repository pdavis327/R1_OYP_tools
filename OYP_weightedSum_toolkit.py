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

		# First parameter
		param0 = arcpy.Parameter(
		    displayName="Raster Output Name",
		    name="outname",
		    datatype= "String",
		    parameterType="Required",
		    direction="Input")

		# Second parameter
		param1 = arcpy.Parameter(
		    displayName="Output folder or geodatabase",
		    name="output_dir",
		    datatype="DEWorkspace",
		    parameterType="Required",
		    direction="Input")

		# third parameter
		param2 = arcpy.Parameter(
		    displayName="Select Rasters",
		    name="selectRasters",
		    datatype="GPRasterLayer",
		    parameterType="Required",
		    direction="Input",
		    multiValue=True)
		
		param2.columns = [["GPRasterLayer", "Raster"],["Double","Scale Factor"]]
		param2.filters[1].type = "Range"
		param2.filters[1].list = [0, 1]

		params = [param0, param1, param2]
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
		#Input user variables
		outname = parameters[0].valueAsText

		#Input second variable
		output_dir = parameters[1].valueAsText

		#Input third variable
		selectRasters = parameters[2].valueAsText

		arcpy.env.overwriteOutput = True
		
		from arcpy.sa import *  
		
		
		split_rasters = selectRasters.split(';')
		split_space = selectRasters.split(';')
		arcpy.AddMessage(selectRasters)
		#outname = os.path.join(gdb_out, ouraster_name)
		
		##User select Rasters
		#Ras1 = arcpy.mapping.ListLayers(mapdoc, "", df)[0]
		#Ras2 = arcpy.mapping.ListLayers(mapdoc, "", df)[1]
		#Ras3 = arcpy.mapping.ListLayers(mapdoc, "", df)[2]
		
		##User set layer weights 0 - 1
		#Ras1_weight = .5
		#Ras2_weight = .4
		#Ras3_weight = .3
		
		#if Ras1_weight + Ras2_weight + Ras3_weight != 1.0:
			#print ("Raster layer weights do not equal 1.0. Please rerun the tool and assign each layer weight parameter a value between 0-1, totalling 1.0 among layers.")
			#arcpy.AddMessage("Raster layer weights do not equal 1.0. Please rerun the tool and assign each layer weight parameter a value between 0-1, totalling 1.0 among layers.")
			#exit()
		
		##Perform raster algebra
		#arcpy.CheckOutExtension("Spatial")
		
		#raster_sum = ((Raster(Ras1.name) * Ras1_weight) + (Raster(Ras2.name) * Ras2_weight) + (Raster(Ras3.name) * Ras3_weight))
					  
		#raster_sum_rescale = Int(((raster_sum - raster_sum.minimum) * 100 / (raster_sum.maximum - raster_sum.minimum) + 0) + 0.5)
		
		##Save to geodatabase
		#raster_sum_rescale.save(outname)		

		#print ("Operation Complete")
		#arcpy.AddMessage("Operation Complete")

		return
