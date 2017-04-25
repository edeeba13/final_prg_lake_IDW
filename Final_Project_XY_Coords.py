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
arcpy.CheckOutExtension("Spatial")
from arcpy.sa import *


env.workspace = r"E:\P in GIS\Final project"
output_fc = r"E:\P in GIS\Final project\Carlyle.gdb"
input_data = r"E:\P in GIS\Final project\ALL_LAKE_DATA_2.csv"
arcpy.CopyRows_management(input_data, output_fc)

#arcpy.MakeXYEventLayer_management.py

print "copying rows"

in_Table = input_data
x_Coords = "Long"
y_Coords = "Lat"
out_Layer = "Carlyle_layer"
saved_Layer = r"E:\P in GIS\Final project\Carlyle.lyr"

print "Creating XY Layer"
arcpy.MakeXYEventLayer_management(in_Table, x_Coords, y_Coords, out_Layer)


outLocation = r"E:\P in GIS\Final project\Carlyle.gdb"
outFeatureClass = "XYCoord"
##Changed inFeature to out_layer here

print "Creating output feature class"

arcpy.FeatureClassToFeatureClass_conversion(out_Layer, outLocation,outFeatureClass)

#define projection
in_dataset = r"E:\P in GIS\Final project\Carlyle.gdb\XYCoord"
coord_sys = arcpy.SpatialReference('NAD 1983 StatePlane Missouri East FIPS 2401 (US Feet)')
##not sure what spatial reference to use


out_gdb = r"E:\P in GIS\Final project\Carlyle.gdb"

#I looked into the issue a bit, and I found that I may need to convert my excel spreadsheet to a table in order to access the data for the interpolation-- what do you this of this?
##def importallsheets(input_data,out_gdb):
##    workbook = xlrd.open_workbook(input_data)
##    sheets = ["May vs June" for sheet in workbook.sheets()]
##    print('{} sheets found: {}'.format(len(sheets), ','.join(sheets)))
##    for sheet in sheets:
##        # The out_table is based on the input excel file name
##        # a underscore (_) separator followed by the sheet name
##        out_table = os.path.join(out_gdb,arcpy.ValidateTableName("{0}_{1}".format(os.path.basename(input_data), sheet),
##                out_gdb))
##
##        print('Converting {} to {}'.format(sheet, out_table))
##
##print "Performing the conversion"
##
##arcpy.ExcelToTable_conversion(in_excel, out_table, sheet)


print "Defining Projection"
arcpy.DefineProjection_management(in_dataset,coord_sys)


in_Feature = "TP mg/kg"
field_name = "TP_mg_kg"

arcpy.AddField_management(input_data, field_name, "LONG")

inPointFeatures = in_dataset
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



#interpolate points

##from arcgis.features.analyze_patterns import interpolate_points
##interpolated_rf = interpolate_points(rainfall, field='RAINFALL')
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