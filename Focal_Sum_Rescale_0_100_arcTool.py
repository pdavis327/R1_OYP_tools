import arcpy
arcpy.CheckOutExtension("Spatial")

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Focal Sum Rescale Raster 0-100"
		self.alias = ""

		# List of tool classes associated with this toolbox
		self.tools = [Focal_Sum_Rescale_Int]


class Focal_Sum_Rescale_Int(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Focal Sum Rescale Raster 0-100"
		self.description = "Performa focal sum moving window using a radius of 1600-meters, then rescale raster to 0-100 and convert to 8-bit unsigned integer with NoData = 255"
		self.canRunInBackground = False

	def getParameterInfo(self):

		param0 = arcpy.Parameter(
		    displayName="Input Raster",
		    name="in_ras",
		    datatype="GPRasterLayer",
		    parameterType="Required",
		    direction="Input")

		param1 = arcpy.Parameter(
		    displayName="Output Raster dataset",
		    name="out_ras",
		    datatype= "DERasterDataset",
		    parameterType="Required",
		    direction="Output")	

		param2 = arcpy.Parameter(
		    displayName="Mask/ Snap Raster",
		    name="mask_snap",
		    datatype= "GPRasterLayer",
		    parameterType="Required",
		    direction="Input")			

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

		#import params
		in_ras = parameters[0].valueAsText
		out_ras = parameters[1].valueAsText
		mask_snap = parameters[2].valueAsText

		#Set environments
		arcpy.env.overwriteOutput = True		
		from arcpy.sa import *  		
		arcpy.CheckOutExtension("Spatial")	
		arcpy.env.resamplingMethod = "BILINEAR"
		arcpy.env.snapRaster = mask_snap	

		#Perform Focal Sum
		arcpy.AddMessage("\nPerforming focal sum.")
		focal_sum = FocalStatistics(in_ras, "Circle 1600 MAP", "SUM")	

		arcpy.AddMessage("\nExtracting by mask.")
		focal_sum = ExtractByMask(focal_sum, mask_snap)		

		#Perform raster algebra for rescale
		arcpy.AddMessage("\nRescaling data.\n")
		raster_rescale = Int(((focal_sum - focal_sum.minimum) * 100 / (focal_sum.maximum - focal_sum.minimum) + 0) + 0.5)	
		
		Rmask = Raster(mask_snap)
		#Fill in noData to 0 based on mask
		mask = Con(IsNull(Rmask),Rmask, 0)	
		lst = [mask,raster_rescale]
		focal_sum_lg = arcpy.MosaicToNewRaster_management(lst, "in_memory", "focal_sum_lg.img","", '8_BIT_UNSIGNED', "", '1')		

		#Save to geodatabase
		arcpy.CopyRaster_management(focal_sum_lg, out_ras, '', '', '255', '', '', "8_BIT_UNSIGNED")		
		return
	
	#Con(IsNull("elevation"),0, "elevation")