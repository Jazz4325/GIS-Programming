import geopandas as gpd
import matplotlib.pyplot as plt
from pandasgui import show
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input shapefile ZIP file")

actions = parser.add_mutually_exclusive_group(required=True)
actions.add_argument("-i", "--info", action="store_true", help="Print basic information about the vector dataset.")
actions.add_argument("-p", "--plot", action="store_true", help="Plot your shapefile using matplotlib.")
actions.add_argument("-b", "--browse", action="store_true",help="Browse your shapefile's attribute table.")
actions.add_argument("-e", "--export", action="store_true",help="Export your shapefile's attributes as a .csv file.")

args = parser.parse_args()


# 1. Load Shapefile ZIP as GeoDataFrame [geopandas]

gdf = gpd.read_file(args.input)  


# 2. Display metadata about shapefile


if args.info:
    print("\n--- Vector dataset info ---")
    print(f"File: {args.input}")
    print(f"Feature count: {len(gdf)}")
    print(" ------------------CRS------------------------")
    crs = gdf.crs
    if crs:
        print("CRS code:", crs.to_string())
        print("CRS name:", crs.name)
    else:
        print("CRS: None (no CRS defined)")
    print(" ------------------Bounds------------------------")
    print("    " + "|min-x| \t |min-y| \t |max-x| \t |max-y|")
    print(gdf.total_bounds) 
    print("-------------------------------------------------")
    print("  Missing geometries:", gdf.geometry.isna().sum())
    print("  Invalid geometries:", (~gdf.is_valid).sum())


# 3. Quick plot [matplotlib]

if args.plot:
    gdf.plot()
    plt.show()


# 4. Browse Attribute Table [pandasgui]

if args.browse:
    show(gdf) 
 

# 5. Save as .csv (default saves to current working directory) [geopandas]
# -- save only specific fields --
    # fields = ["BLOCKID", "POP100", "HU100", "geometry"]
    # gdf = gdf[fields] 

if args.export:
    gdf.to_csv(args.input, index=False, encoding='utf-8')