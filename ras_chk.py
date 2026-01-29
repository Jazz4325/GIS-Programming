import rasterio
from rasterio.plot import show
import argparse
from pyproj import CRS

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input Raster Image (.tif)")

actions = parser.add_mutually_exclusive_group(required=True)
actions.add_argument("-i", "--info", action="store_true", help="Print basic information about the raster dataset.")
actions.add_argument("-p", "--plot", action="store_true", help="Plot your shapefile using matplotlib.")

args = parser.parse_args()


# Open Raster and access Metadata [rastario] , [pyproj]

with rasterio.open(args.input) as src:

    # 1. Print Raster Metadata
    if args.info:
        cell_area = abs(src.transform.a * src.transform.e)
        total_area = cell_area * src.width * src.height
        print("\n--- Raster image info ---")
        print(f"File: {args.input}")
        print(f"Number of bands: {src.count}")
        crs = src.crs
        if crs:
            print("------------------CRS------------------------")
            print(crs)
            crs = CRS.from_wkt(src.crs.to_wkt())
            print(crs.name)
        if not crs.is_projected:
            print("CRS is geographic (units are degrees)")
        if not crs:
            print("CRS: None (no CRS defined)")
        print(" ------------------Resolution------------------------")
        print(f"Pixel size: {src.res}")
        print(f"Dimensions: {src.width} x {src.height}")
        print(f"Pixel count: {src.width * src.height:,}")
        print(f"Cell area: {cell_area:.0f}")
        print(f"Total area: {total_area:,.0f}")


    # 2. Quick plot [rastario.plot]
    if args.plot:
        show(src)