import arcpy
import time

start = time.time()

version = "06"


polygonForClipping = "C:/GIS-Projects/AvalancheNVME/Avalanche.gdb/AreaPolygon"
baseDEM = "C:/GIS-Projects/AvalancheNVME/DEM_Tirol_5m.tif"
clippedDEM = "C:/GIS-Projects/AvalancheNVME/ClippedDEM" + version + ".tif"

extentFile = arcpy.Describe(polygonForClipping)
extentOfPolygon = str(extentFile.extent.XMin) + " " + str(extentFile.extent.YMin) + " " + str(extentFile.extent.XMax) + " " + str(extentFile.extent.YMax)

arcpy.Clip_management(baseDEM, extentOfPolygon, clippedDEM, polygonForClipping, "0", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
print("Clip Raster successful\n")


# Pit Remove
arcpy.ImportToolbox(r'D:\TauDEM\TauDEM5Arc\TauDEM Tools.tbx','')
arcpy.PitRemove(clippedDEM, None, None, 8, r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "fel.tif")

pitRemovedDEM = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "fel.tif"
arcpy.Delete_management(clippedDEM)
print("Pit Remove successful\n")


# Dinf Flow Direction
arcpy.ImportToolbox(r'D:\TauDEM\TauDEM5Arc\TauDEM Tools.tbx','')
arcpy.DinfFlowDir(pitRemovedDEM, 8, r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "ang.tif", r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "slp.tif")

flowDirDEM = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "ang.tif"
print("Flow Direction successful\n")

# DELETE .slp
arcpy.Delete_management(r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "slp.tif")

# Raster to Point
arcpy.conversion.RasterToPoint(pitRemovedDEM, r"C:\GIS-Projects\AvalancheNVME\Avalanche.gdb\Points" + version, "Value")

inFeatures = r"C:\GIS-Projects\AvalancheNVME\Avalanche.gdb\Points" + version
print("Raster to Point successful\n")


arcpy.env.workspace = "C:/GIS-Projects/AvalancheNVME/Avalanche.gdb"

# Create the new value field
fieldName1 = "Value"
fieldAlias = "Value"
fieldLength = 255

arcpy.AddField_management(inFeatures, fieldName1, "TEXT", field_alias=fieldAlias, field_length=fieldLength)

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