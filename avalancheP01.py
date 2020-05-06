import arcpy
import time
import sys

start = time.time()
version = sys.argv[1]
path = "C:/GIS-Projects/AvalancheNVME/"
rpath = r"C:/GIS-Projects/AvalancheNVME/"
arcpy.env.overwriteOutput = True
# toolboxLocation =r'D:\TauDEM\TauDEM5Arc\TauDEM Tools.tbx', ''

print("Clipping Raster...")
polygonForClipping = path + "Avalanche.gdb/AreaPolygon"
baseDEM = path + "DEM_Tirol_5m.tif"
clippedDEM = path + "ClippedDEM" + version + ".tif"

extentFile = arcpy.Describe(polygonForClipping)
extentOfPolygon = str(extentFile.extent.XMin) + " " + str(extentFile.extent.YMin) + " " + str(extentFile.extent.XMax) + " " + str(extentFile.extent.YMax)

arcpy.Clip_management(baseDEM, extentOfPolygon, clippedDEM, polygonForClipping, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
print("Clip Raster successful\n")

print("Removing Pits...")
# Pit Remove
arcpy.ImportToolbox(r'D:\TauDEM\TauDEM5Arc\TauDEM Tools.tbx', '')
arcpy.PitRemove(clippedDEM, None, None, 8, rpath + "ClippedDEM" + version + "fel.tif")

pitRemovedDEM = rpath + "ClippedDEM" + version + "fel.tif"
arcpy.Delete_management(clippedDEM)
print("Pit Remove successful\n")

print("Calculating Flow Direction...")
# Dinf Flow Direction
arcpy.ImportToolbox(r'D:\TauDEM\TauDEM5Arc\TauDEM Tools.tbx', '')
arcpy.DinfFlowDir(pitRemovedDEM, 8, rpath + "ClippedDEM" + version + "ang.tif", rpath + "ClippedDEM" + version + "slp.tif")

flowDirDEM = rpath + "ClippedDEM" + version + "ang.tif"
print("Flow Direction successful\n")

# Delete .slp
arcpy.Delete_management(rpath + "ClippedDEM" + version + "slp.tif")

print("Converting Raster to Points...")
# Raster to Point
arcpy.conversion.RasterToPoint(pitRemovedDEM, rpath + "Avalanche.gdb/Points" + version, "Value")

inFeatures = rpath + "Avalanche.gdb/Points" + version
print("Raster to Point successful\n")


print("Creating new Field...")
arcpy.env.workspace = path + "Avalanche.gdb"

# Create the new value field
fieldName1 = "Value"
fieldAlias = "Value"
fieldLength = 255

arcpy.AddField_management(inFeatures, fieldName1, "TEXT", field_alias=fieldAlias, field_length=fieldLength)
print("New Field created\n")

print("Setting new point values to 0...")
print("(Depending on the size of the area this might take a long time)")
# Set all new field values to 0
fc = inFeatures

cursor = arcpy.UpdateCursor(fc)
rowcount = 0

for row in cursor:
    if row.Value is None:
        row.Value = 0
        cursor.updateRow(row)
        rowcount += 1
        if rowcount % 100000 == 0:
            print(f"{rowcount} points edited")


print(f"Updated Table ({rowcount} points edited)")

end = time.time()
print(f"Elapsed time: {round((end - start) / 60,2)} min")