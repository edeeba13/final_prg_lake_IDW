#-------------------------------------------------------------------------------
# Name:       Final project
# Purpose:
#
# Author:      deeba
#
# Created:     28/02/2017
# Copyright:   (c) deeba 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
arcpy.env.overwriteOutput = True
from arcpy import env
import os

env.workspace = r"E:\P in GIS\Final project"
output_fc = r"E:\P in GIS\Final project\Carlyle.gdb"
input_data = r"E:\P in GIS\Final project\ALL_LAKE_DATA"
arcpy.CopyRows_management(input_data, output_fc)

#arcpy.MakeXYEventLayer_management.py

print "copying rows"

in_Table = r"E:\P in GIS\Final project\ALL_LAKE_DATA"
x_Coords = "Long"
y_Coords = "Lat"
out_Layer = "Carlyle_layer"
saved_Layer = r"E:\P in GIS\Final project\Carlyle.lyr"

print "Creating XY Layer"
arcpy.MakeXYEventLayer_management(in_Table, x_Coords, y_Coords, out_Layer)


outLocation = r"E:\P in GIS\Final project\Carlyle.gdbb"
outFeatureClass = "XYCoord"
##Changed inFeature to out_layer here

print "Creating output feature class"

arcpy.FeatureClassToFeatureClass_conversion(out_Layer, outLocation,outFeatureClass)

#define projection
in_dataset = r"E:\P in GIS\Final project\Carlyle.gdb\XYCoord"
coord_sys = arcpy.SpatialReference('NAD 1983 StatePlane Missouri East FIPS 2401 (US Feet)')
##not sure what spatial reference to use

print "Defining Projection"

arcpy.DefineProjection_management(in_dataset,coord_sys)

import arcpy
from arcpy import env
from arcpy.sa import *


inPointFeatures = r"E:\P in GIS\Final project\Carlyle.lyr"
zField = "TP_mg_kg"
cellSize = 2000.0
power = 2
searchRadius = RadiusVariable(10, 150000)

# Execute IDW
print "executing interpolation"

outIDW = Idw(inPointFeatures, zField, cellSize, power, searchRadius)

# Save the output
print "saving"
outIDW.save("E:\P in GIS\Final project\output")

#datetime plotting
##date_values = {'date': ['2010/03', '2011/04', '2012/12', '2014/01', '2015/02'],
##               'value': [12, 23, 20, 31, 42]}
##
###transform date from string into datetime format. This is important!
##from datetime import datetime
##date_values['date'] = map(lambda x: datetime.strptime(x, '%Y/%m'), date_values['date'])
##fig = plt.figure(figsize=(10,5))
##plt.plot_date(date_values['date'], date_values['value'], 'bs-')
##plt.title('Money on Account No.1', fontsize=16)
##plt.xlabel('Month/Year', fontsize=16)
##plt.ylabel('US$', fontsize=16)