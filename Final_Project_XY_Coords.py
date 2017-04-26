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


env.workspace = r"C:\Student\EMILY\final_prg"
output_fc = r"C:\Student\EMILY\test.gdb"
input_data = r"C:\Student\EMILY\final_prg\ALL_LAKE_DATA.csv"
#define projection
in_dataset = os.path.join(output_fc, "XYCoord")
coord_sys = arcpy.SpatialReference('NAD 1983 StatePlane Missouri East FIPS 2401 (US Feet)')
##not sure what spatial reference to use

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


outLocation = output_fc
outFeatureClass = "XYCoord"
##Changed inFeature to out_layer here

print "Creating output feature class"

arcpy.FeatureClassToFeatureClass_conversion(out_Layer, outLocation,outFeatureClass)




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
field_name_string = "TP_mg_kg"
field_name_double = "TP_mg_kg_num"

#this needs to be in_dataset
arcpy.AddField_management(in_dataset, field_name_double, "DOUBLE")

##------------
#update that field
fields = [field_name_string, field_name_double]

# Create update cursor for feature class
with arcpy.da.UpdateCursor(in_dataset, fields) as cursor:
    for row in cursor:
        try:
            row[1] = float(row[0])
            print('Valid Value.')
        except:
            print("Null Value.")
            row[1] = None

        cursor.updateRow(row)

inPointFeatures = in_dataset
zField = field_name_double#"TP_mg_kg"
cellSize = 2000.0
power = 2
searchRadius = RadiusVariable(10, 150000)

# Execute IDW
print "executing interpolation"
outIDW = Idw(inPointFeatures, zField, cellSize, power, searchRadius)

# Save the output
print "saving"
outIDW.save("raster1.tif")



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