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

#define projection
in_dataset = os.path.join(output_fc, "XYCoord")
coord_sys = arcpy.SpatialReference('NAD 1983 UTM Zone 16N')


arcpy.CopyRows_management(input_data, output_fc)

#arcpy.MakeXYEventLayer_management.py

print "copying rows"

in_Table = input_data
x_Coords = "Long"
y_Coords = "Lat"
out_Layer = "Carlyle_layer"
saved_Layer = r"E:\P in GIS\Final project\Carlyle.lyr"

out_raster = "Carlyle_raster.tif"

print "Creating XY Layer"
arcpy.MakeXYEventLayer_management(in_Table, x_Coords, y_Coords, out_Layer)


outLocation = output_fc
outFeatureClass = "XYCoord"

print "Creating output feature class"

arcpy.FeatureClassToFeatureClass_conversion(out_Layer, outLocation,outFeatureClass)




out_gdb = r"E:\P in GIS\Final project\Carlyle.gdb"


print "Defining Projection"
arcpy.DefineProjection_management(in_dataset,coord_sys)


in_Feature = "TP mg/kg"
field_name_string = "TP_mg_kg"
field_name_double = "TP_mg_kg_num"

#this needs to be in_dataset
arcpy.AddField_management(in_dataset, field_name_double, "DOUBLE")


#update field from string to float
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
zField = field_name_double
cellSize = "6.49000000000115E-04"
cellPower = 2

# Execute IDW
print "executing interpolation"
outIDW = Idw(inPointFeatures, zField, cellSize, cellPower)

# Save the output
print "saving"
outIDW.save(out_raster)

#preparing files to be clipped
out_points = r"E:\P in GIS\Final project\output\Carlyle_points.shp"
arcpy.RasterToPoint_conversion(out_raster, out_points)
#clipping interpolation
clip_features = r"E:\P in GIS\Final project\carl_poly.shp"
out_Carlyle_poly = r"E:\P in GIS\Final project\output\clipped_carlyle_poly.shp"
arcpy.Clip_analysis(out_points, clip_features, out_Carlyle_poly)


