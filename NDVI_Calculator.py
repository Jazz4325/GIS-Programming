"""
NDVI Raster Generator
Generates NDVI from multispectral raster imagery (e.g., Sentinel-2, Landsat)
NDVI = (NIR - Red) / (NIR + Red)
"""

import numpy as np
import rasterio
import geopandas as gpd


def calculate_ndvi(red_band, nir_band) -> np.ndarray:
    """
    Calculate NDVI from red and near-infrared bands.
    
    Parameters:
    -----------
    red_band : numpy.ndarray
        Red band array
    nir_band : numpy.ndarray
        Near-infrared band array
        
    Returns:
    --------
    ndvi : numpy.ndarray
        NDVI values ranging from -1 to 1
    """
    # Convert to float to avoid integer division issues
    red = red_band.astype(float) 
    nir = nir_band.astype(float)
    
    # Avoid division by zero
    denominator = nir + red
    ndvi = np.where(
        denominator == 0,
        0,  # Set NDVI to 0 where denominator is 0
        (nir - red) / denominator 
    )
    
    return ndvi


def generate_ndvi_raster(input_raster_path, output_raster_path, 
                         red_band_index, nir_band_index,
                         nodata_value=-9999):
    """
    Generate NDVI raster from multispectral input raster.
    
    Parameters:
    -----------
    input_raster_path : str
        Path to input multispectral raster file
    output_raster_path : str
        Path for output NDVI raster file
    red_band_index : int
        Band index for red band (1-indexed)
    nir_band_index : int
        Band index for NIR band (1-indexed)
    nodata_value : float, default=-9999
        NoData value for output raster
        
    Returns:
    --------
    str : Path to generated NDVI raster
    """
    
    print(f"Reading input raster: {input_raster_path}")
    
    with rasterio.open(input_raster_path) as src:
        # Read metadata
        profile = src.profile.copy()
        
        # Read red and NIR bands
        print(f"Reading Red band (band {red_band_index})...")
        red = src.read(red_band_index)
        
        print(f"Reading NIR band (band {nir_band_index})...")
        nir = src.read(nir_band_index)
        
        # Handle nodata values
        if src.nodata is not None:
            mask = (red == src.nodata) | (nir == src.nodata) 
        else:
            mask = np.zeros_like(red, dtype=bool)
        
        # Calculate NDVI
        print("Calculating NDVI...")
        ndvi = calculate_ndvi(red, nir)
        
        # Apply nodata mask
        ndvi[mask] = nodata_value
        
        # Update profile for single-band output
        profile.update({
            'count': 1,
            'dtype': rasterio.float32,
            'nodata': nodata_value
        })
        
        # Write NDVI raster
        print(f"Writing NDVI raster to: {output_raster_path}")
        with rasterio.open(output_raster_path, 'w', **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)
            dst.set_band_description(1, 'NDVI')
        
        # Calculate and print statistics
        valid_ndvi = ndvi[~mask] # cookie cutter with mask
        if len(valid_ndvi) > 0:
            print("\nNDVI Statistics:")
            print(f"  Min:  {valid_ndvi.min():.4f}")
            print(f"  Max:  {valid_ndvi.max():.4f}")
            print(f"  Mean: {valid_ndvi.mean():.4f}")
            print(f"  Std:  {valid_ndvi.std():.4f}")
        
    print(f"\nNDVI raster successfully created: {output_raster_path}")
    return output_raster_path


def clip_ndvi_by_shapefile(ndvi_raster_path, shapefile_path, output_clipped_path):
    """
    Clip NDVI raster using a shapefile boundary.
    
    Parameters:
    -----------
    ndvi_raster_path : str
        Path to NDVI raster file
    shapefile_path : str
        Path to shapefile for clipping
    output_clipped_path : str
        Path for output clipped raster
    """
    from rasterio.mask import mask
    
    # Read shapefile
    gdf = gpd.read_file(shapefile_path)
    
    # Ensure CRS match
    with rasterio.open(ndvi_raster_path) as src:
        if gdf.crs != src.crs:
            print(f"Reprojecting shapefile from {gdf.crs} to {src.crs}")
            gdf = gdf.to_crs(src.crs)
        
        # Clip raster
        print("Clipping NDVI raster...")
        out_image, out_transform = mask(src, gdf.geometry, crop=True)
        out_meta = src.meta.copy()
        
        # Update metadata
        out_meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })
        
        # Write clipped raster
        with rasterio.open(output_clipped_path, "w", **out_meta) as dst:
            dst.write(out_image)
    
    print(f"Clipped NDVI raster saved to: {output_clipped_path}")
    return output_clipped_path


if __name__ == "__main__":
    # Example usage
    # Adjust these parameters based on your data
    
    # For Sentinel-2: Red is band 4, NIR is band 8
    # For Landsat 8/9: Red is band 4, NIR is band 5
    
    input_raster = "path/to/your/multispectral_image.tif"
    output_ndvi = "output_ndvi.tif"

    generate_ndvi_raster(
        input_raster_path=input_raster,
        output_raster_path=output_ndvi,
        red_band_index=4,  
        nir_band_index=5   # For Landsat 8/9
    )