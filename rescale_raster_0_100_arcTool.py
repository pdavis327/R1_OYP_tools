import arcpy


class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Rescale Raster 0-100"
		self.alias = ""

		# List of tool classes associated with this toolbox
		self.tools = [Rescale_Int]


class Rescale_Int(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Rescale Raster 0-100"
		self.description = "Rescale a raster to 0-100 and convert to 8-bit unsigned integer with NoData = 255"
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
		
		arcpy.AddMessage("\nExtracting by mask.")
		extract = ExtractByMask(in_ras, mask_snap)		
		
		#Perform raster algebra for rescale
		arcpy.AddMessage("\nRescaling data.\n")
		raster_rescale = Int(((extract - extract.minimum) * 100 / (extract.maximum - extract.minimum) + 0) + 0.5)	
		
		Rmask = Raster(mask_snap)
		#Fill in noData to 0 based on mask
		mask = Con(IsNull(Rmask),Rmask, 0)	
		lst = [mask,raster_rescale]
		rescaled_ras = arcpy.MosaicToNewRaster_management(lst, "in_memory", "rescaled_ras.img","", '8_BIT_UNSIGNED', "", '1')				
		
		#Save to geodatabase
		arcpy.CopyRaster_management(rescaled_ras, out_ras, '', '', '255', '', '', "8_BIT_UNSIGNED")		
		return
