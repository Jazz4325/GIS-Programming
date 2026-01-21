import geopandas as gpd
import matplotlib.pyplot as plt
from pandasgui import show
import argparse

parser = argparse.ArgumentParser()
actions = parser.add_mutually_exclusive_group()
actions.add_argument("-p", "--plot", action="store_true", help="Plot your shapefile using matplotlib.")
actions.add_argument("-b", "--browse", action="store_true",help="Browse your shapefile's attribute table.")
actions.add_argument("-e", "--export", action="store_true",help="Export your shapefile's attributes as a .csv file.")
parser.add_argument("input", help="Input shapefile ZIP file")
args = parser.parse_args()


# 1. Load Shapefile ZIP as GeoDataFrame [geopandas]

gdf = gpd.read_file(args.input)  


# 2. Quick plot [matplotlib]

if args.plot:
    gdf.plot()
    plt.show()


# 3. Browse Attribute Table - (THIS IS GOATED) [pandasgui]

if args.browse:
    show(gdf) 


# 4. Save as .csv (default saves to current working directory) [geopandas]
# -- save only specific fields --
    # fields = ["BLOCKID", "POP100", "HU100", "geometry"]
    # gdf = gdf[fields] 

if args.export:
    gdf.to_csv(args.input, index=False, encoding='utf-8')