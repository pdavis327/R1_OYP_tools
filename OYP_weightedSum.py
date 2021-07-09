import arcpy
import os

mapdoc = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mapdoc)[0]

#Background processing MUST be dissabled to use current map document
#set to always run in foreground in tool setting to override background processing.
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = 0

from arcpy.sa import *  

#output geodatabase User input string
gdb_out = (r"T:\FS\NFS\R01\Program\7140Geometronics\GIS\Workspace\pdavis\Rapid_outyear_2019\Weighted_Overlay_Tool\Weighted_Overlay_test.gdb")

#Output raster name: User input string
ouraster_name = ("outRas_test")

outname = os.path.join(gdb_out, ouraster_name)

#User select Rasters
Ras1 = arcpy.mapping.ListLayers(mapdoc, "", df)[0]
Ras2 = arcpy.mapping.ListLayers(mapdoc, "", df)[1]
Ras3 = arcpy.mapping.ListLayers(mapdoc, "", df)[2]

#User set layer weights 0 - 1
Ras1_weight = .5
Ras2_weight = .4
Ras3_weight = .3

if Ras1_weight + Ras2_weight + Ras3_weight != 1.0:
	print ("Raster layer weights do not equal 1.0. Please rerun the tool and assign each layer weight parameter a value between 0-1, totalling 1.0 among layers.")
	arcpy.AddMessage("Raster layer weights do not equal 1.0. Please rerun the tool and assign each layer weight parameter a value between 0-1, totalling 1.0 among layers.")
	exit()

#Perform raster algebra
arcpy.CheckOutExtension("Spatial")

raster_sum = ((Raster(Ras1.name) * Ras1_weight) + (Raster(Ras2.name) * Ras2_weight) + (Raster(Ras3.name) * Ras3_weight))
              
raster_sum_rescale = Int(((raster_sum - raster_sum.minimum) * 100 / (raster_sum.maximum - raster_sum.minimum) + 0) + 0.5)

#Save to geodatabase
raster_sum_rescale.save(outname)

