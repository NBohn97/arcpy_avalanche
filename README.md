# arcpy_avalanche

ArcPy script to prepare data for the 'TauDEM D-Infinity Avalanche Runout' tool.\
Requirements:\
            - ArcGIS Pro ArcPy environment\
            - TauDEM Toolbox


avalancheP01.py:\
###Input:  - Polygon of area to be analyzed.\
###Output: - DEM-Raster with pits removed\
            - D-Infinity Flow Directions Raster\
            - Point feature-class filled with value 0
          
avalancheP02.py:\
    Input:  - DEM-Raster with pits removed\
            - D-Infinity Flow Directions Raster\
            - Point feature-class filled with value 0 (Value 1 in areas where avalanches are expected)\
    Output: - Avalanche runout zone affected area Raster (slope degree)\
            - Avalanche path-distance raster
  
  
