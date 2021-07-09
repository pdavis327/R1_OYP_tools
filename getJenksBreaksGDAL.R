library (BAMMtools)
library (sf)

dsn <- ("T:\\FS\\NFS\\R01\\Program\\7140Geometronics\\GIS\\Project\\zz_R1OutyearPlanning2019\\PodAssessment\\Data\\NID_VMap_Zonals.gdb")
layer <- "NORTHERN_ID_ATTRIBUTES"

table = st_read(dsn,layer)

breaks <- getJenksBreaks(table$FAI_FIRE_RAW_RESCALE, 3)