import arcpy
import time
import sys

start = time.time()
version = sys.argv[1]

print("Preparing Workspace...")
arcpy.env.workspace = "C:/GIS-Projects/AvalancheNVME/Avalanche.gdb"
arcpy.env.extent = "C:/GIS-Projects/AvalancheNVME/ClippedDEM" + version + "fel.tif"
arcpy.env.snapRaster = "C:/GIS-Projects/AvalancheNVME/ClippedDEM" + version + "fel.tif"

inFeatures = "C:/GIS-Projects/AvalancheNVME/Avalanche.gdb/Points" + version
valField = "Value"
outRaster = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "ass.tif"
assignmentType = "MOST_FREQUENT"
priorityField = ""
cellSize = 5

print("Converting Points to Raster...")
# Point to Raster
arcpy.conversion.PointToRaster(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)

pitRemoveDEM = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "fel.tif"
flowDir = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "ang.tif"
sourceGrid = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "ass.tif"

output1 = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "rz.tif"
output2 = r"C:\GIS-Projects\AvalancheNVME\ClippedDEM" + version + "dfs.tif"
print("Points converted\n")

print("Calculating avalanche runout distance")
arcpy.ImportToolbox(r'D:\TauDEM\TauDEM5Arc\TauDEM Tools.tbx','')
arcpy.DInfAvalancheRunout(pitRemoveDEM, flowDir, sourceGrid, 0.2, 20, "Flow Path", 8, output1, output2)
print("Avalanche Runout successful\n")

print("Cleaning up...")
arcpy.Delete_management(inFeatures)
arcpy.Delete_management(pitRemoveDEM)
arcpy.Delete_management(flowDir)
arcpy.Delete_management(sourceGrid)

end = time.time()
print(f"Elapsed time: {round((end - start) / 60,2)} min")
