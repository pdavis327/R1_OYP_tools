library (BAMMtools)
library (arcgisbinding)

#load arc format table
table <- arc.open("")

#grab column of interest
Attr <- table$colName

#Get jenks
breaks <- getJenksBreaks(Attr, 3)
