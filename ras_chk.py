from pprint import pprint
import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt
import numpy as np


### FOR NEXT TIME ###
# Wrap saving into a function
# Add argparse



# Open Raster and access Metadata

input_raster = r"thermal.tif"
with rasterio.open(input_raster) as src:
    metadata = src.profile



    # 1. Quick plot
    
    show(src)


    # 2. Print Raster Metadata

    pprint(metadata)
    

    # 3. Save Raster as .png

    if metadata["count"] < 3:
        # Do single band logic; save as grayscale image
        pixels = src.read(1)

        # Use single band as R, G, and B values
        pixels = np.stack([pixels, pixels, pixels], axis=-1)

    else:
        # RGB logic; assume bands 1, 2, 3 are R, G, B
        pixels = src.read([1, 2, 3])

        # Reorder to (rows, cols, bands)
        pixels = pixels.transpose(1, 2, 0)

    # Normalize
    pixels = pixels.astype("float32")
    pixels = (pixels - pixels.min()) / (pixels.max() - pixels.min())

    # Export
    plt.imsave("my_file.png", pixels)