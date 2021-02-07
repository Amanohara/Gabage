import sys
import pandas as pd
import geopandas as gpd
import numpy as np
from fiona.crs import from_epsg
from shapely.geometry import Polygon, MultiPoint, LineString, LinearRing
import gdal
import ogr
def file_judge(data_type,data):
    if  data_type == "point" :
        output = MultiPoint(data)
    elif data_type == "line" :
        question = input("Closed? [y/n]")
        if question == "y":
            output = LinearRing(data)
        else:
            output = LineString(data)
    elif data_type == "polygon" :
        output = Polygon(data)
    else :
        print("なにかがおかしいよ")
        sys.exit(1)
    return output
#
def store_DataFrame(output,EPSG):
    # DataFrameに格納
    # 空のGeoDataFrameを作る
    newdata = gpd.GeoDataFrame()
    newdata['geometry'] = None
    newdata.loc[0, 'geometry'] = output
    newdata.crs = from_epsg(EPSG)
    return newdata    
#
def output_files(DataFrame, filetype, output_name="output"):
    if filetype == "shp":
        DataFrame.to_file(output_name + ".shp")
    elif filetype == "json":
        DataFrame.to_file(output_name + ".geojson",driver='GeoJSON')
    else:
        print("なにかがおかしいよ")
        sys.exit(1)
#
data_type = input("Point / Line / Polygon :")
filename = input("Filename :")
output_EPSG = input("output EPSG :")
output_filetype = input("shp / json :")
output_filename = input("Output Filename :")
#
data = np.loadtxt(filename, delimiter=',')
convert_data = file_judge(data_type,data)
df = store_DataFrame(convert_data,int(output_EPSG))
if output_filename == "" :
    output_files(df, output_filetype)
else:
     output_files(df, output_filetype, output_filename)